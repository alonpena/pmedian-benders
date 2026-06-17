/* phase2.c — Fase 2: maestro MIP + lazy callback (Etapa 6).
 * Variables: y_j binarias (idx j), theta_i continuas >=0 (idx M+i).
 * En cada solucion entera el callback corre el separador (Alg.1) y agrega los
 * cortes (ec.20) violados con GRBcblazy (via solver_cb_add_lazy).
 */
#include "phase2.h"
#include "separation.h"
#include "solver.h"
#include <stdio.h>
#include <stdlib.h>

#define P2_TOL 1e-6

typedef struct {
    const SortSites *ss;
    int     N, M;
    double *sol;     /* buffer tamano M+N (solucion entera del callback) */
    int    *ind;     /* buffer tamano M+1 */
    double *val;
    long    ncuts;
    SolverCB *cb;    /* contexto vivo durante el callback */
} P2Ctx;

/* sink de separacion: agrega corte perezoso theta_i + sum coef y >= rhs */
static void p2_add_lazy(int client, const Cut *cut, void *user) {
    P2Ctx *c = user;
    int len = cut->len + 1;
    c->ind[0] = c->M + client;
    c->val[0] = 1.0;
    for (int t = 0; t < cut->len; t++) { c->ind[t + 1] = cut->ind[t]; c->val[t + 1] = cut->val[t]; }
    solver_cb_add_lazy(c->cb, len, c->ind, c->val, '>', cut->rhs);
    c->ncuts++;
}

static void p2_lazy_fn(SolverCB *cb, void *user) {
    P2Ctx *c = user;
    c->cb = cb;
    solver_cb_get_solution(cb, c->sol);            /* [y(0..M-1), theta(0..N-1)] */
    const double *ybar = c->sol;
    const double *thetabar = c->sol + c->M;
    separation_all(c->ss, ybar, thetabar, P2_TOL, p2_add_lazy, c);
}

Phase2Result phase2_run(const Instance *inst, const SortSites *ss, int verbose) {
    int N = inst->N, M = inst->M;
    Solver *s = solver_create(verbose ? 0 : 1);

    solver_add_vars(s, M, 0.0, 1.0, 'B', NULL);     /* y binarias */
    double *one = malloc(N * sizeof(double));
    for (int i = 0; i < N; i++) one[i] = 1.0;
    solver_add_vars(s, N, 0.0, 1e100, 'C', one);    /* theta */
    free(one);
    solver_set_minimize(s);

    int *yidx = malloc(M * sizeof(int));
    double *yval = malloc(M * sizeof(double));
    for (int j = 0; j < M; j++) { yidx[j] = j; yval[j] = 1.0; }
    solver_add_constr(s, M, yidx, yval, '=', (double)inst->p);
    free(yidx); free(yval);

    /* gaps ajustados (brief 4.2): probar optimalidad exacta */
    solver_set_dbl_param(s, "MIPGap", 1e-10);

    P2Ctx ctx = { ss, N, M, malloc((M + N) * sizeof(double)),
                  malloc((M + 1) * sizeof(int)), malloc((M + 1) * sizeof(double)), 0, NULL };

    solver_enable_lazy(s);
    solver_set_lazy_callback(s, p2_lazy_fn, &ctx);
    solver_optimize(s);

    Phase2Result res;
    res.objval = solver_objval(s);
    res.ncuts  = ctx.ncuts;
    res.nodes  = solver_node_count(s);
    res.open_set = malloc(inst->p * sizeof(int));
    double *y = malloc(M * sizeof(double));
    solver_get_x(s, 0, M, y);
    int k = 0;
    for (int j = 0; j < M && k < inst->p; j++) if (y[j] > 0.5) res.open_set[k++] = j;
    while (k < inst->p) res.open_set[k++] = 0;  /* relleno defensivo */
    free(y);

    free(ctx.sol); free(ctx.ind); free(ctx.val);
    solver_destroy(s);
    return res;
}
