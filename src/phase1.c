/* phase1.c — Fase 1: maestro LP + loop separar/agregar/redondear (Etapa 5).
 * Sigue el Algoritmo 3 (brief 9.1). Variables del maestro:
 *   y_j  (j=0..M-1)   continuas en [0,1]   indice = j
 *   theta_i (i=0..N-1) continuas >= 0       indice = M + i
 * Objetivo: min sum theta_i.  Restriccion: sum y_j = p.
 */
#include "phase1.h"
#include "separation.h"
#include "heuristic.h"
#include "solver.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define P1_TOL 1e-6
#define P1_MAXIT 100000

typedef struct {
    Solver *s;
    int     M;
    long    ncuts;
    int     added_this_iter;
    int    *ind;     /* buffer reusable tamano M+1 */
    double *val;
} P1Ctx;

/* sink: agrega el corte (ec.20)  theta_i + sum coef_j y_j >= rhs  al maestro */
static void p1_add_cut(int client, const Cut *cut, void *user) {
    P1Ctx *c = user;
    int len = cut->len + 1;
    c->ind[0] = c->M + client;   /* theta_i */
    c->val[0] = 1.0;
    for (int t = 0; t < cut->len; t++) {
        c->ind[t + 1] = cut->ind[t];
        c->val[t + 1] = cut->val[t];
    }
    solver_add_constr(c->s, len, c->ind, c->val, '>', cut->rhs);
    c->ncuts++;
    c->added_this_iter++;
}

Phase1Result phase1_run(const Instance *inst, const SortSites *ss, int verbose) {
    int N = inst->N, M = inst->M;
    Solver *s = solver_create(1);

    /* y continuas [0,1] obj 0 ; theta continuas [0,inf) obj 1 */
    solver_add_vars(s, M, 0.0, 1.0, 'C', NULL);
    double *one = malloc(N * sizeof(double));
    for (int i = 0; i < N; i++) one[i] = 1.0;
    solver_add_vars(s, N, 0.0, 1e100, 'C', one);
    free(one);
    solver_set_minimize(s);

    /* sum y_j = p */
    int *yidx = malloc(M * sizeof(int));
    double *yval = malloc(M * sizeof(double));
    for (int j = 0; j < M; j++) { yidx[j] = j; yval[j] = 1.0; }
    solver_add_constr(s, M, yidx, yval, '=', (double)inst->p);
    free(yidx); free(yval);

    double *ybar    = malloc(M * sizeof(double));
    double *thetabar = calloc(N, sizeof(double));
    for (int j = 0; j < M; j++) ybar[j] = (double)inst->p / M;  /* arranque uniforme */

    P1Ctx ctx = { s, M, 0, 0, malloc((M + 1) * sizeof(int)), malloc((M + 1) * sizeof(double)) };

    Phase1Result res = { 0.0, INFINITY, malloc(inst->p * sizeof(int)), 0, 0 };
    int *roundset = malloc(inst->p * sizeof(int));

    int iter = 0;
    while (iter < P1_MAXIT) {
        iter++;
        ctx.added_this_iter = 0;
        separation_all(ss, ybar, thetabar, P1_TOL, p1_add_cut, &ctx);

        double ub = rounding_heuristic(inst, ybar, roundset);
        if (ub < res.UB1) {
            res.UB1 = ub;
            for (int t = 0; t < inst->p; t++) res.best_set[t] = roundset[t];
        }
        if (verbose)
            printf("[F1] iter=%d LB1=%.4f UB1=%.1f cuts+=%d total=%ld\n",
                   iter, res.LB1, res.UB1, ctx.added_this_iter, ctx.ncuts);

        if (ctx.added_this_iter == 0) break;   /* no hay cortes violados => fin */

        solver_optimize(s);
        res.LB1 = solver_objval(s);
        solver_get_x(s, 0, M, ybar);
        solver_get_x(s, M, N, thetabar);
    }

    res.iters = iter;
    res.ncuts = ctx.ncuts;
    free(ctx.ind); free(ctx.val);
    free(ybar); free(thetabar); free(roundset);
    solver_destroy(s);
    return res;
}
