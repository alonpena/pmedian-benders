/* phase2.h — Fase 2: branch-and-Benders-cut con callback de lazy constraints
 * (brief 9.2, Etapa 6). */
#ifndef PMP_PHASE2_H
#define PMP_PHASE2_H

#include "instance.h"
#include "sortsites.h"
#include "cutpool.h"

typedef struct {
    double  objval;     /* optimo probado */
    int    *open_set;   /* tamano p */
    long    ncuts;      /* cortes perezosos agregados en el callback */
    long    nsep;       /* invocaciones del separador (callbacks MIPSOL) */
    long    nwarm;      /* cortes precargados desde el pool de Fase 1 */
    double  nodes;      /* nodos del B&B */
} Phase2Result;

/* Corre Fase 2. El llamador libera result.open_set.
 * warm != NULL => precarga ese pool de cortes (warm-start, metodo del paper);
 * warm == NULL => arranque limpio (solo callback). */
Phase2Result phase2_run(const Instance *inst, const SortSites *ss, int verbose,
                        const CutPool *warm);

#endif
