/* heuristic.h — heuristica de redondeo (brief seccion 9.1).
 * Abre los p sitios con mayor ȳ_j y evalua exacto. Reemplaza a PopStar (Pareto cut). */
#ifndef PMP_HEURISTIC_H
#define PMP_HEURISTIC_H

#include "instance.h"

/* Devuelve UB (objetivo exacto) y escribe el conjunto abierto (tamano p) en out_set. */
double rounding_heuristic(const Instance *inst, const double *ybar, int *out_set);

#endif
