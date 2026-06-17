/* sortsites.h — matriz S: para cada cliente, sitios ordenados por cercania.
 *
 * Etapa 3. Brief seccion 7.8: S (N x M) se construye una vez en O(NM log M).
 * S[i*M + r] = r-esimo sitio mas cercano al cliente i.
 * Dord[i*M + r] = distancia de ese r-esimo sitio (no decreciente en r).
 */
#ifndef PMP_SORTSITES_H
#define PMP_SORTSITES_H

#include "instance.h"

typedef struct {
    int   N, M;
    int  *S;      /* N*M: sitios ordenados por cercania por cliente */
    long *Dord;   /* N*M: distancias ordenadas correspondientes */
} SortSites;

SortSites *sortsites_build(const Instance *inst);
void sortsites_free(SortSites *ss);

#endif
