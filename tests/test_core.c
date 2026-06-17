/* test_core.c — pruebas de Etapas 1-4 (instancia, distancias, oraculo, S, separacion).
 *
 * Uso: test_core <instancia.pmp> [p]
 * Si la instancia es toy1 (N=4) verifica valores a mano. Para cualquier instancia
 * chequea las invariantes clave: separacion(integer y*) == eval(y*) y validez de
 * cortes (ningun corte recorta el optimo). Devuelve 0 si todo pasa, 1 si falla.
 */
#include "../src/instance.h"
#include "../src/sortsites.h"
#include "../src/separation.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static int failures = 0;
#define CHECK(cond, msg) do { \
    if (cond) { printf("  ok   %s\n", msg); } \
    else { printf("  FAIL %s\n", msg); failures++; } } while (0)

/* recolector de cortes para el test de validez */
typedef struct { Cut *cuts; int n, cap; } CutBag;

static void bag_sink(int client, const Cut *cut, void *user) {
    CutBag *b = user;
    if (b->n == b->cap) { b->cap = b->cap ? b->cap * 2 : 64; b->cuts = realloc(b->cuts, b->cap * sizeof(Cut)); }
    Cut c; c.client = client; c.rhs = cut->rhs; c.len = cut->len;
    c.ind = malloc(cut->len * sizeof(int));
    c.val = malloc(cut->len * sizeof(double));
    memcpy(c.ind, cut->ind, cut->len * sizeof(int));
    memcpy(c.val, cut->val, cut->len * sizeof(double));
    b->cuts[b->n++] = c;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "uso: test_core <instancia.pmp> [p]\n"); return 2; }
    int p_override = (argc >= 3) ? atoi(argv[2]) : -1;
    Instance *inst = instance_load(argv[1], p_override);
    if (!inst) { fprintf(stderr, "fallo al cargar\n"); return 2; }

    printf("== Etapa 1: instancia ==\n");
    printf("  N=%d M=%d p=%d  (%s)\n", inst->N, inst->M, inst->p,
           inst->has_coords ? "coords" : "matriz");

    if (inst->N == 4 && inst->has_coords) {  /* toy1: distancias a mano */
        printf("== toy: distancias ==\n");
        CHECK(instance_dist(inst,0,1)==3, "d(0,1)=3");
        CHECK(instance_dist(inst,0,2)==4, "d(0,2)=4");
        CHECK(instance_dist(inst,0,3)==5, "d(0,3)=5");
        CHECK(instance_dist(inst,1,2)==5, "d(1,2)=5");
        CHECK(instance_dist(inst,1,3)==4, "d(1,3)=4");
        CHECK(instance_dist(inst,2,3)==3, "d(2,3)=3");
    }

    printf("== Etapa 2: fuerza bruta (oraculo) ==\n");
    int *best = malloc(inst->p * sizeof(int));
    double opt = -1;
    int do_brute = (inst->M <= 24);
    if (do_brute) {
        opt = instance_brute_force(inst, best);
        printf("  opt=%.1f set={", opt);
        for (int t = 0; t < inst->p; t++) printf("%s%d", t?",":"", best[t]);
        printf("}\n");
        if (inst->N == 4) CHECK(fabs(opt - 6.0) < 1e-9, "toy opt = 6");
    } else {
        printf("  (M=%d grande: brute omitido)\n", inst->M);
    }

    printf("== Etapa 3: matriz S ==\n");
    SortSites *ss = sortsites_build(inst);
    printf("  S[cliente 0] (primeros <=6): ");
    for (int r = 0; r < ss->M && r < 6; r++) printf("%d(%ld) ", ss->S[r], ss->Dord[r]);
    printf("\n");
    if (inst->N == 4 && inst->has_coords) {
        /* cliente 0: dist a 0,1,2,3 = 0,3,4,5 -> S = 0,1,2,3 */
        int okS = ss->S[0]==0 && ss->S[1]==1 && ss->S[2]==2 && ss->S[3]==3;
        CHECK(okS, "toy S[0] = [0,1,2,3]");
        CHECK(ss->Dord[0]==0 && ss->Dord[1]==3 && ss->Dord[2]==4 && ss->Dord[3]==5,
              "toy Dord[0] = [0,3,4,5]");
    }

    printf("== Etapa 4: separacion ==\n");
    /* integer y* a partir del optimo de fuerza bruta (si existe) */
    double *ybar = calloc(inst->M, sizeof(double));
    if (do_brute) {
        for (int t = 0; t < inst->p; t++) ybar[best[t]] = 1.0;
        double UB = separation_all(ss, ybar, NULL, 0.0, NULL, NULL);
        printf("  sum OPT(SP_i) en y* = %.1f ; eval(y*) = %.1f\n",
               UB, instance_eval_open_set(inst, best, inst->p));
        CHECK(fabs(UB - opt) < 1e-9, "separacion(y*) == optimo (cortes exactos en enteros)");

        /* validez: cortes desde un punto fraccionario uniforme no deben recortar y* */
        double *yfrac = malloc(inst->M * sizeof(double));
        for (int j = 0; j < inst->M; j++) yfrac[j] = (double)inst->p / inst->M;
        double *thetazero = calloc(inst->N, sizeof(double));
        CutBag bag = {0};
        separation_all(ss, yfrac, thetazero, 1e-9, bag_sink, &bag);
        /* distancia real de cada cliente bajo y* */
        int valid = 1;
        for (int c = 0; c < bag.n; c++) {
            Cut *cu = &bag.cuts[c];
            int i = cu->client;
            long di = instance_dist(inst, i, best[0]);
            for (int t = 1; t < inst->p; t++) { long d = instance_dist(inst, i, best[t]); if (d < di) di = d; }
            double lb = cu->rhs;
            for (int t = 0; t < cu->len; t++) lb -= cu->val[t] * ybar[cu->ind[t]];
            if (lb > di + 1e-6) { valid = 0; printf("  corte invalido cliente %d: lb=%.3f > dist=%ld\n", i, lb, di); }
        }
        printf("  cortes generados desde y fraccionario: %d\n", bag.n);
        CHECK(valid, "ningun corte recorta el optimo y*");
        for (int c = 0; c < bag.n; c++) { free(bag.cuts[c].ind); free(bag.cuts[c].val); }
        free(bag.cuts); free(yfrac); free(thetazero);
    } else {
        printf("  (sin oraculo brute; ver cross-check vs prototipo)\n");
    }

    /* dump separacion total para cross-check externo: UB en y uniforme */
    double *yuni = malloc(inst->M * sizeof(double));
    for (int j = 0; j < inst->M; j++) yuni[j] = (double)inst->p / inst->M;
    double UBuni = separation_all(ss, yuni, NULL, 0.0, NULL, NULL);
    printf("  [xcheck] sum OPT(SP_i) en y=p/M uniforme: %.6f\n", UBuni);
    free(yuni);

    free(ybar); free(best);
    sortsites_free(ss);
    instance_free(inst);
    printf(failures ? "\nRESULT: FAIL (%d)\n" : "\nRESULT: PASS\n", failures);
    return failures ? 1 : 0;
}
