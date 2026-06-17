/* sortsites.c — construccion de la matriz S (Etapa 3). */
#include "sortsites.h"
#include <stdlib.h>

typedef struct { long d; int site; } Pair;

static int cmp_pair(const void *a, const void *b) {
    const Pair *pa = a, *pb = b;
    if (pa->d < pb->d) return -1;
    if (pa->d > pb->d) return 1;
    return pa->site - pb->site;   /* desempate estable por indice de sitio */
}

SortSites *sortsites_build(const Instance *inst) {
    int N = inst->N, M = inst->M;
    SortSites *ss = malloc(sizeof(SortSites));
    ss->N = N; ss->M = M;
    ss->S    = malloc((size_t)N * M * sizeof(int));
    ss->Dord = malloc((size_t)N * M * sizeof(long));
    Pair *buf = malloc((size_t)M * sizeof(Pair));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            buf[j].d = instance_dist(inst, i, j);
            buf[j].site = j;
        }
        qsort(buf, M, sizeof(Pair), cmp_pair);
        for (int r = 0; r < M; r++) {
            ss->S[(size_t)i * M + r]    = buf[r].site;
            ss->Dord[(size_t)i * M + r] = buf[r].d;
        }
    }
    free(buf);
    return ss;
}

void sortsites_free(SortSites *ss) {
    if (!ss) return;
    free(ss->S); free(ss->Dord); free(ss);
}
