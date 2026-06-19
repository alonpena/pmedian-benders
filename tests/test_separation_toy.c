/* test_separation_toy.c — arnes de verificacion del separador contra numeros
 * derivados A MANO (toy1, p=2, sitios abiertos = {0,1}).
 *
 * Escenario (ver docs/AUDIT.md): ȳ = {1,1,0,0}. El separador debe producir
 * EXACTAMENTE, por cliente:
 *   cliente 0: k̃=0, OPT(SP)=0, corte: theta_0 >= 0
 *   cliente 1: k̃=0, OPT(SP)=0, corte: theta_1 >= 0
 *   cliente 2: k̃=2, OPT(SP)=4, corte: theta_2 >= 4 - 4*y_2 - 1*y_3
 *   cliente 3: k̃=2, OPT(SP)=4, corte: theta_3 >= 4 - 4*y_3 - 1*y_2
 * Comparaciones exactas en enteros. Si algo discrepa: imprime esperado-vs-real
 * y FALLA (no se ajusta la formula para forzar la coincidencia).
 *
 * Uso: test_separation_toy [instancia.pmp]   (default instances/toy/toy1.pmp)
 */
#include "../src/instance.h"
#include "../src/sortsites.h"
#include "../src/separation.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static int failures = 0;

/* compara entero esperado vs real; si difiere, lo reporta y suma falla */
static void expect_int(const char *what, int client, long got, long want) {
    if (got == want) {
        printf("  ok   cliente %d: %s = %ld\n", client, what, want);
    } else {
        printf("  FAIL cliente %d: %s esperado=%ld real=%ld\n", client, what, want, got);
        failures++;
    }
}

/* escenario esperado por cliente: k̃, opt(const=rhs), y mapa sitio->coef */
typedef struct { int ktilde; long rhs; int n; int site[2]; long coef[2]; } Expect;

int main(int argc, char **argv) {
    const char *path = (argc >= 2) ? argv[1] : "instances/toy/toy1.pmp";
    Instance *inst = instance_load(path, 2);   /* p = 2 */
    if (!inst) { fprintf(stderr, "fallo al cargar %s\n", path); return 2; }
    if (inst->N != 4 || !inst->has_coords) {
        fprintf(stderr, "este arnes asume toy1 (N=4, coords); recibido N=%d\n", inst->N);
        instance_free(inst); return 2;
    }
    SortSites *ss = sortsites_build(inst);

    /* ȳ = {1,1,0,0}: sitios 0 y 1 abiertos */
    double ybar[4] = {1.0, 1.0, 0.0, 0.0};

    /* derivado a mano (ver cabecera) */
    Expect exp[4] = {
        { 0, 0, 0, {0, 0}, {0, 0} },                 /* cliente 0 */
        { 0, 0, 0, {0, 0}, {0, 0} },                 /* cliente 1 */
        { 2, 4, 2, {2, 3}, {4, 1} },                 /* cliente 2 */
        { 2, 4, 2, {3, 2}, {4, 1} },                 /* cliente 3 */
    };

    printf("== Verificacion del separador vs derivacion a mano (toy1, ȳ={1,1,0,0}) ==\n");
    Cut cut;
    cut.ind = malloc((size_t)inst->M * sizeof(int));
    cut.val = malloc((size_t)inst->M * sizeof(double));

    for (int i = 0; i < 4; i++) {
        int kt = separation_k_tilde(ss, i, ybar);
        double opt = separation_client(ss, i, ybar, &cut);

        expect_int("k̃", i, kt, exp[i].ktilde);
        /* opt y rhs son enteros en este escenario: compara exacto via redondeo seguro */
        expect_int("OPT(SP)", i, (long)llround(opt), exp[i].rhs);
        expect_int("constante (rhs)", i, (long)llround(cut.rhs), exp[i].rhs);
        expect_int("num coeficientes", i, cut.len, exp[i].n);

        /* coeficientes order-independent: cada (sitio,coef) esperado debe existir */
        for (int e = 0; e < exp[i].n; e++) {
            int found = 0; long gotc = -1;
            for (int t = 0; t < cut.len; t++) {
                if (cut.ind[t] == exp[i].site[e]) { found = 1; gotc = (long)llround(cut.val[t]); break; }
            }
            if (!found) {
                printf("  FAIL cliente %d: falta coef para y_%d\n", i, exp[i].site[e]);
                failures++;
            } else {
                char w[32]; snprintf(w, sizeof w, "coef y_%d", exp[i].site[e]);
                expect_int(w, i, gotc, exp[i].coef[e]);
            }
        }
        /* no debe haber coeficientes extra (len ya chequeado, pero validamos sitios) */
        for (int t = 0; t < cut.len; t++) {
            int ok = 0;
            for (int e = 0; e < exp[i].n; e++) if (cut.ind[t] == exp[i].site[e]) ok = 1;
            if (!ok) { printf("  FAIL cliente %d: coef inesperado y_%d=%.0f\n", i, cut.ind[t], cut.val[t]); failures++; }
        }
    }

    free(cut.ind); free(cut.val);
    sortsites_free(ss);
    instance_free(inst);
    printf(failures ? "\nRESULT: FAIL (%d)\n" : "\nRESULT: PASS\n", failures);
    return failures ? 1 : 0;
}
