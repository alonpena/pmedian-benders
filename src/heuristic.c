/* heuristic.c — heuristica de redondeo (Etapa 5). */
#include "heuristic.h"
#include <stdlib.h>

static const double *g_ybar;   /* para el comparador de qsort */
static int cmp_desc_y(const void *a, const void *b) {
    int ja = *(const int *)a, jb = *(const int *)b;
    double da = g_ybar[ja], db = g_ybar[jb];
    if (da > db) return -1;
    if (da < db) return 1;
    return ja - jb;
}

double rounding_heuristic(const Instance *inst, const double *ybar, int *out_set) {
    int M = inst->M;
    int *idx = malloc(M * sizeof(int));
    for (int j = 0; j < M; j++) idx[j] = j;
    g_ybar = ybar;
    qsort(idx, M, sizeof(int), cmp_desc_y);
    for (int t = 0; t < inst->p; t++) out_set[t] = idx[t];
    free(idx);
    return instance_eval_open_set(inst, out_set, inst->p);
}
