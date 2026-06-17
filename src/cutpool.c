/* cutpool.c — implementacion del almacen de cortes. */
#include "cutpool.h"
#include <stdlib.h>
#include <string.h>

CutPool *cutpool_create(void) {
    CutPool *p = calloc(1, sizeof(CutPool));
    return p;
}

void cutpool_add(CutPool *p, int client, double rhs, int len, const int *ind, const double *val) {
    if (p->n == p->cap) {
        p->cap = p->cap ? p->cap * 2 : 256;
        p->cuts = realloc(p->cuts, p->cap * sizeof(Cut));
    }
    Cut *c = &p->cuts[p->n++];
    c->client = client;
    c->rhs = rhs;
    c->len = len;
    c->ind = malloc((len ? len : 1) * sizeof(int));
    c->val = malloc((len ? len : 1) * sizeof(double));
    if (len) {
        memcpy(c->ind, ind, len * sizeof(int));
        memcpy(c->val, val, len * sizeof(double));
    }
}

void cutpool_free(CutPool *p) {
    if (!p) return;
    for (int i = 0; i < p->n; i++) { free(p->cuts[i].ind); free(p->cuts[i].val); }
    free(p->cuts);
    free(p);
}
