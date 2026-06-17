/* separation.c — Algoritmos 1 y 2, ecuaciones 17-20 (Etapa 4). */
#include "separation.h"
#include <stdlib.h>

#define SEP_EPS 1e-9

/* Algoritmo 2 (brief seccion 7.7): recorre los sitios del cliente del mas
 * cercano al mas lejano usando S, acumulando ȳ hasta cubrir 1, y cuenta los
 * saltos de radio (incremento estricto de distancia). O(M). */
int separation_k_tilde(const SortSites *ss, int i, const double *ybar) {
    int M = ss->M;
    const int  *S = &ss->S[(size_t)i * M];
    const long *D = &ss->Dord[(size_t)i * M];
    int k_tilde = 0;
    int r = 0;
    double val = 1.0 - ybar[S[0]];
    while (val > SEP_EPS && r < M - 1) {
        if (D[r + 1] > D[r]) k_tilde++;   /* salto de radio (empates = mismo radio) */
        r++;
        val -= ybar[S[r]];
    }
    return k_tilde;
}

double separation_client(const SortSites *ss, int i, const double *ybar, Cut *cut) {
    int M = ss->M;
    const int  *S = &ss->S[(size_t)i * M];
    const long *D = &ss->Dord[(size_t)i * M];

    /* repetir el recorrido del Alg.2 reteniendo r (posicion del 1er sitio cubierto) */
    int k_tilde = 0;
    int r = 0;
    double val = 1.0 - ybar[S[0]];
    while (val > SEP_EPS && r < M - 1) {
        if (D[r + 1] > D[r]) k_tilde++;
        r++;
        val -= ybar[S[r]];
    }

    if (cut) cut->client = i;

    if (k_tilde == 0) {
        /* ya hay (fraccion de) sitio en el radio minimo => OPT = D^1_i */
        double opt = (double)D[0];
        if (cut) { cut->rhs = opt; cut->len = 0; }
        return opt;
    }

    /* D^{k̃+1}_i = distancia del primer radio cubierto = D[r] */
    double D_next = (double)D[r];
    double acc = 0.0;
    int len = 0;
    /* sitios S[0..r-1] tienen distancia < D_next (radios <= k̃) */
    for (int t = 0; t < r; t++) {
        int j = S[t];
        double coef = D_next - (double)D[t];   /* (D^{k̃+1}_i - d_ij) >= 0 */
        acc += coef * ybar[j];
        if (cut) { cut->ind[len] = j; cut->val[len] = coef; }
        len++;
    }
    if (cut) { cut->rhs = D_next; cut->len = len; }
    return D_next - acc;   /* ec.18 */
}

double separation_all(const SortSites *ss, const double *ybar,
                      const double *thetabar, double tol,
                      cut_sink cb, void *user) {
    int M = ss->M;
    double UB = 0.0;
    Cut cut;
    cut.ind = malloc((size_t)M * sizeof(int));
    cut.val = malloc((size_t)M * sizeof(double));
    for (int i = 0; i < ss->N; i++) {
        double opt = separation_client(ss, i, ybar, &cut);
        UB += opt;
        if (thetabar && cb && thetabar[i] < opt - tol)
            cb(i, &cut, user);
    }
    free(cut.ind); free(cut.val);
    return UB;
}
