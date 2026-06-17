/* solver_gurobi.c — backend Gurobi de la capa solver.h.
 *
 * Firmas verificadas contra docs/SOLVER_NOTES.md (gurobi_c.h instalado, v12.0.0).
 * Compilar con -DUSE_GUROBI -I$GUROBI_HOME/include -L$GUROBI_HOME/lib -lgurobiXXX.
 */
#include "solver.h"
#include <stdio.h>
#include <stdlib.h>
#include "gurobi_c.h"

struct Solver {
    GRBenv   *env;
    GRBmodel *model;
    int       nvars;
    int       need_update;
    solver_lazy_fn lazy_fn;
    void          *lazy_user;
};

struct SolverCB {
    Solver *s;
    void   *cbdata;
};

static void die(Solver *s, const char *ctx) {
    fprintf(stderr, "Gurobi error en %s: %s\n", ctx,
            s && s->env ? GRBgeterrormsg(s->env) : "(sin env)");
    exit(1);
}

Solver *solver_create(int silent) {
    Solver *s = calloc(1, sizeof(Solver));
    if (GRBloadenv(&s->env, NULL)) die(s, "loadenv");
    GRBsetintparam(s->env, GRB_INT_PAR_OUTPUTFLAG, silent ? 0 : 1);
    if (GRBnewmodel(s->env, &s->model, "pmp", 0, NULL, NULL, NULL, NULL, NULL))
        die(s, "newmodel");
    return s;
}

void solver_destroy(Solver *s) {
    if (!s) return;
    if (s->model) GRBfreemodel(s->model);
    if (s->env) GRBfreeenv(s->env);
    free(s);
}

static void ensure_update(Solver *s) {
    if (s->need_update) { GRBupdatemodel(s->model); s->need_update = 0; }
}

int solver_add_vars(Solver *s, int n, double lb, double ub, char vtype, const double *obj) {
    int base = s->nvars;
    for (int k = 0; k < n; k++) {
        double o = obj ? obj[k] : 0.0;
        if (GRBaddvar(s->model, 0, NULL, NULL, o, lb, ub, vtype, NULL))
            die(s, "addvar");
    }
    s->nvars += n;
    s->need_update = 1;
    return base;
}

void solver_add_constr(Solver *s, int len, const int *ind, const double *val,
                       char sense, double rhs) {
    ensure_update(s);
    /* GRBaddconstr toma int* no const; copiar para respetar la firma const de la API */
    int *ci = malloc((len ? len : 1) * sizeof(int));
    double *cv = malloc((len ? len : 1) * sizeof(double));
    for (int k = 0; k < len; k++) { ci[k] = ind[k]; cv[k] = val[k]; }
    if (GRBaddconstr(s->model, len, ci, cv, sense, rhs, NULL)) die(s, "addconstr");
    free(ci); free(cv);
    s->need_update = 1;
}

void solver_set_minimize(Solver *s) {
    if (GRBsetintattr(s->model, GRB_INT_ATTR_MODELSENSE, GRB_MINIMIZE))
        die(s, "modelsense");
    s->need_update = 1;
}

void solver_set_int_param(Solver *s, const char *name, int v) {
    if (GRBsetintparam(GRBgetenv(s->model), name, v)) die(s, "setintparam");
}
void solver_set_dbl_param(Solver *s, const char *name, double v) {
    if (GRBsetdblparam(GRBgetenv(s->model), name, v)) die(s, "setdblparam");
}

int solver_optimize(Solver *s) {
    ensure_update(s);
    if (GRBoptimize(s->model)) die(s, "optimize");
    int st; GRBgetintattr(s->model, GRB_INT_ATTR_STATUS, &st);
    return st == GRB_OPTIMAL ? 0 : st;
}

double solver_objval(Solver *s) {
    double v; if (GRBgetdblattr(s->model, GRB_DBL_ATTR_OBJVAL, &v)) die(s, "objval");
    return v;
}

double solver_node_count(Solver *s) {
    double v; if (GRBgetdblattr(s->model, GRB_DBL_ATTR_NODECOUNT, &v)) return 0;
    return v;
}

void solver_get_x(Solver *s, int start, int len, double *out) {
    if (GRBgetdblattrarray(s->model, GRB_DBL_ATTR_X, start, len, out)) die(s, "getx");
}

int solver_num_vars(Solver *s) { return s->nvars; }

/* --- lazy callback --- */
static int __stdcall grb_cb(GRBmodel *model, void *cbdata, int where, void *usrdata) {
    (void)model;
    Solver *s = usrdata;
    if (where == GRB_CB_MIPSOL && s->lazy_fn) {
        SolverCB cb = { s, cbdata };
        s->lazy_fn(&cb, s->lazy_user);
    }
    return 0;
}

void solver_enable_lazy(Solver *s) {
    if (GRBsetintparam(GRBgetenv(s->model), GRB_INT_PAR_LAZYCONSTRAINTS, 1))
        die(s, "lazyparam");
}

void solver_set_lazy_callback(Solver *s, solver_lazy_fn fn, void *user) {
    s->lazy_fn = fn; s->lazy_user = user;
    if (GRBsetcallbackfunc(s->model, grb_cb, s)) die(s, "setcallback");
}

void solver_cb_get_solution(SolverCB *cb, double *out) {
    if (GRBcbget(cb->cbdata, GRB_CB_MIPSOL, GRB_CB_MIPSOL_SOL, out))
        die(cb->s, "cbget");
}

void solver_cb_add_lazy(SolverCB *cb, int len, const int *ind, const double *val,
                        char sense, double rhs) {
    if (GRBcblazy(cb->cbdata, len, ind, val, sense, rhs)) die(cb->s, "cblazy");
}
