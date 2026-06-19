/* main.c — CLI del solver pMP Benders.
 *
 * Uso: pmedian <instancia.pmp> [--p P] [--mode phase1|full] [-v] [--opt V]
 *   --mode phase1 : solo Fase 1 (relajacion LP + redondeo) -> LB1, UB1
 *   --mode full   : Fase 1 + Fase 2 (branch-and-Benders-cut exacto)
 *   --opt V       : optimo conocido (para reportar gap/estado en el CSV)
 * Registra una fila en results/benchmark.csv.
 */
#include "instance.h"
#include "sortsites.h"
#include "separation.h"
#include "phase1.h"
#include "phase2.h"
#include "cutpool.h"
#include "logging.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* --dump-cuts: dado un conjunto de sitios abiertos, imprime para cada cliente
 * la linea  i=<i> ktilde=<k> opt=<v> cut: theta_i >= <const> [ - <coef>*y_<j> ...]
 * Es la prueba legible de que el separador concuerda con la derivacion a mano y
 * con el oraculo Python. No resuelve nada: solo separa en el ȳ dado. */
static int dump_cuts(Instance *inst, SortSites *ss, const int *open, int nopen) {
    double *ybar = calloc((size_t)inst->M, sizeof(double));
    for (int t = 0; t < nopen; t++) {
        if (open[t] < 0 || open[t] >= inst->M) {
            fprintf(stderr, "sitio %d fuera de rango [0,%d)\n", open[t], inst->M);
            free(ybar); return 2;
        }
        ybar[open[t]] = 1.0;
    }
    printf("dump-cuts: abiertos = {");
    for (int t = 0; t < nopen; t++) printf("%s%d", t?",":"", open[t]);
    printf("}\n");
    Cut cut;
    cut.ind = malloc((size_t)inst->M * sizeof(int));
    cut.val = malloc((size_t)inst->M * sizeof(double));
    for (int i = 0; i < inst->N; i++) {
        int kt = separation_k_tilde(ss, i, ybar);
        double opt = separation_client(ss, i, ybar, &cut);
        printf("i=%d ktilde=%d opt=%g cut: theta_%d >= %g", i, kt, opt, i, cut.rhs);
        for (int t = 0; t < cut.len; t++)
            printf(" - %g*y_%d", cut.val[t], cut.ind[t]);
        printf("\n");
    }
    free(cut.ind); free(cut.val); free(ybar);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "uso: %s <instancia.pmp> [--p P] [--mode phase1|full] [-v] [--opt V]\n", argv[0]);
        return 2;
    }
    const char *path = argv[1];
    int p_override = -1, verbose = 0, coldstart = 0;
    const char *mode = "full";
    double opt_known = NAN;
    int dump = 0, ndump = 0;
    int *dumpsites = malloc((size_t)argc * sizeof(int));
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--p") && i + 1 < argc) p_override = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--mode") && i + 1 < argc) mode = argv[++i];
        else if (!strcmp(argv[i], "-v")) verbose = 1;
        else if (!strcmp(argv[i], "--opt") && i + 1 < argc) opt_known = atof(argv[++i]);
        else if (!strcmp(argv[i], "--coldstart")) coldstart = 1;   /* Fase 2 sin warm-start */
        else if (!strcmp(argv[i], "--dump-cuts")) {
            dump = 1;   /* el resto de args son indices de sitios abiertos */
            for (int j = i + 1; j < argc; j++) dumpsites[ndump++] = atoi(argv[j]);
            break;
        }
    }

    Instance *inst = instance_load(path, p_override);
    if (!inst) return 2;
    printf("Instancia %s: N=%d M=%d p=%d (%s)\n", path, inst->N, inst->M, inst->p,
           inst->has_coords ? "coords" : "matriz");

    double t_s = wall_seconds();
    SortSites *ss = sortsites_build(inst);
    double t_S = wall_seconds() - t_s;
    printf("Matriz S construida en %.3f s\n", t_S);

    if (dump) {
        int rc = dump_cuts(inst, ss, dumpsites, ndump);
        free(dumpsites); sortsites_free(ss); instance_free(inst);
        return rc;
    }

    double LB1 = 0, UB1 = 0, T1 = 0, nodes = 0, Ttot = 0;
    long iter = 0;
    char optbuf[32] = "NA";
    char status[16] = "ok";
    if (!isnan(opt_known)) snprintf(optbuf, sizeof optbuf, "%.0f", opt_known);

    CutPool *pool = coldstart ? NULL : cutpool_create();
    double t0 = wall_seconds();
    Phase1Result r1 = phase1_run(inst, ss, verbose, pool);
    T1 = wall_seconds() - t0;
    LB1 = r1.LB1; UB1 = r1.UB1; iter = r1.iters;
    printf("[Fase 1] LB1=%.4f UB1=%.1f iter=%d cuts=%ld T1=%.3f s\n",
           r1.LB1, r1.UB1, r1.iters, r1.ncuts, T1);

    double finalval = UB1;
    if (!strcmp(mode, "full")) {
        double t2 = wall_seconds();
        Phase2Result r2 = phase2_run(inst, ss, verbose, pool);
        double T2 = wall_seconds() - t2;
        nodes = r2.nodes;
        finalval = r2.objval;
        printf("[Fase 2] opt=%.1f cuts=%ld nodes=%.0f T2=%.3f s start=%s set={",
               r2.objval, r2.ncuts, r2.nodes, T2, coldstart ? "cold" : "warm");
        for (int t = 0; t < inst->p; t++) printf("%s%d", t?",":"", r2.open_set[t]);
        printf("}\n");
        /* PRUEBA DE CALLBACK (branch-and-Benders-cut): separaciones, cortes lazy, nodos */
        printf("[CALLBACK] warm_cuts=%ld  separaciones(MIPSOL)=%ld  cortes_lazy=%ld  nodos_B&B=%.0f\n",
               r2.nwarm, r2.nsep, r2.ncuts, r2.nodes);
        if (r2.ncuts == 0)
            printf("[CALLBACK][WARN] cortes_lazy=0 => NO es branch-and-Benders-cut!\n");
        if (!isnan(opt_known))
            strcpy(status, fabs(r2.objval - opt_known) < 0.5 ? "OPTIMAL_MATCH" : "MISMATCH");

        /* log de prueba por corrida */
        system("mkdir -p results/logs");
        const char *bn = strrchr(path, '/'); bn = bn ? bn + 1 : path;
        char logpath[512];
        snprintf(logpath, sizeof logpath, "results/logs/%s_p%d_%s.log", bn, inst->p, mode);
        FILE *lf = fopen(logpath, "w");
        if (lf) {
            fprintf(lf, "instance=%s N=%d M=%d p=%d backend=gurobi mode=%s\n",
                    bn, inst->N, inst->M, inst->p, mode);
            fprintf(lf, "phase1 LB1=%.4f UB1=%.4f iter=%d cuts=%ld T1=%.3f\n",
                    r1.LB1, r1.UB1, r1.iters, r1.ncuts, T1);
            fprintf(lf, "phase2 opt=%.4f T2=%.3f start=%s warm_cuts=%ld\n",
                    r2.objval, T2, coldstart ? "cold" : "warm", r2.nwarm);
            fprintf(lf, "CALLBACK_PROOF separation_calls=%ld lazy_cuts=%ld bb_nodes=%.0f\n",
                    r2.nsep, r2.ncuts, r2.nodes);
            fprintf(lf, "is_branch_and_benders_cut=%s\n", r2.ncuts > 0 ? "YES" : "NO");
            fprintf(lf, "opt_known=%s status=%s gap=%.6f\n",
                    optbuf, status, (finalval>0)?(finalval-LB1)/finalval:0.0);
            fclose(lf);
            printf("[CALLBACK] log -> %s\n", logpath);
        }
        free(r2.open_set);
    }
    Ttot = wall_seconds() - t0;

    double gap = (finalval > 0) ? (finalval - LB1) / finalval : 0.0;

    /* asegurar carpeta de resultados existe (best-effort) */
    system("mkdir -p results");
    const char *base = strrchr(path, '/'); base = base ? base + 1 : path;
    csv_append("results/benchmark.csv", base, inst->N, inst->M, inst->p,
               "gurobi", mode, LB1, UB1, T1, gap, iter, nodes, Ttot, optbuf, status);

    free(r1.best_set);
    free(dumpsites);
    if (pool) cutpool_free(pool);
    sortsites_free(ss);
    instance_free(inst);
    return 0;
}
