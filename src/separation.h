/* separation.h — separacion O(NM): Algoritmos 1 y 2, ecuaciones 17-20.
 *
 * Etapa 4. Brief seccion 7. El subproblema dual tiene forma cerrada, asi que el
 * corte se separa en O(M) por cliente sin resolver ningun LP.
 */
#ifndef PMP_SEPARATION_H
#define PMP_SEPARATION_H

#include "instance.h"
#include "sortsites.h"

/* Corte de Benders (ec.20) para un cliente i, en forma:
 *      theta_i + sum_{t<len} val[t] * y[ind[t]] >= rhs
 * len = 0 cuando k̃_i = 0 (solo theta_i >= rhs = D^1_i).
 * ind/val deben venir preasignados con capacidad >= M. */
typedef struct {
    int     client;
    double  rhs;
    int     len;
    int    *ind;
    double *val;
} Cut;

/* Algoritmo 2: indice k̃_i en O(M) para el cliente i dado ȳ (tamano M). */
int separation_k_tilde(const SortSites *ss, int i, const double *ybar);

/* Separacion del cliente i. Devuelve OPT(SP_i) (ec.18) y, si cut != NULL,
 * llena el corte (ec.20). No decide violacion (eso lo hace el llamador). */
double separation_client(const SortSites *ss, int i, const double *ybar, Cut *cut);

/* Algoritmo 1: separa todos los clientes. Devuelve UB = sum_i OPT(SP_i).
 * Si thetabar != NULL y cb != NULL, invoca cb(client, cut, user) por cada corte
 * VIOLADO (thetabar[i] < OPT - tol). El Cut pasado al callback es temporal. */
typedef void (*cut_sink)(int client, const Cut *cut, void *user);

double separation_all(const SortSites *ss, const double *ybar,
                      const double *thetabar, double tol,
                      cut_sink cb, void *user);

#endif
