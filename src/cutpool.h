/* cutpool.h — almacen de cortes de Benders, para pasar el pool de Fase 1 a Fase 2
 * (warm-start, el metodo real del paper, brief 9.2). */
#ifndef PMP_CUTPOOL_H
#define PMP_CUTPOOL_H

#include "separation.h"

typedef struct {
    Cut *cuts;   /* cada Cut posee copias propias de ind/val */
    int  n, cap;
} CutPool;

CutPool *cutpool_create(void);
/* agrega una copia profunda del corte (client + rhs + ind/val) */
void cutpool_add(CutPool *p, int client, double rhs, int len, const int *ind, const double *val);
void cutpool_free(CutPool *p);

#endif
