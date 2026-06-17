/* phase1.h — Fase 1: maestro LP + loop de cortes + redondeo (brief 9.1, Etapa 5). */
#ifndef PMP_PHASE1_H
#define PMP_PHASE1_H

#include "instance.h"
#include "sortsites.h"
#include "cutpool.h"

typedef struct {
    double LB1;       /* cota inferior = relajacion LP del maestro */
    double UB1;       /* mejor cota superior (redondeo) */
    int   *best_set;  /* tamano p: mejor conjunto entero hallado */
    int    iters;     /* iteraciones del loop de separacion */
    long   ncuts;     /* cortes agregados en total */
} Phase1Result;

/* Corre Fase 1. El llamador libera result.best_set.
 * Si out_pool != NULL, acumula ahi el pool de cortes generados (para warm-start). */
Phase1Result phase1_run(const Instance *inst, const SortSites *ss, int verbose,
                        CutPool *out_pool);

#endif
