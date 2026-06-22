/* logging.c — implementacion de utilidades de tiempo, CSV y trazas. */
#include "logging.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

struct GapTrace {
    FILE *f;
};

double wall_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

void csv_append(const char *path, const char *instance, int N, int M, int p,
                const char *backend, const char *mode,
                double LB1, double UB1, double T1, double gap,
                long iter, double nodes, double Ttot,
                const char *opt_known, const char *status) {
    FILE *f = fopen(path, "r");
    int exists = 0;
    if (f) { exists = 1; fclose(f); }
    f = fopen(path, "a");
    if (!f) return;
    if (!exists)
        fprintf(f, "instance,N,M,p,backend,mode,LB1,UB1,T1,gap,iter,nodes,Ttot,opt_known,status\n");
    fprintf(f, "%s,%d,%d,%d,%s,%s,%.4f,%.4f,%.3f,%.6f,%ld,%.0f,%.3f,%s,%s\n",
            instance, N, M, p, backend, mode, LB1, UB1, T1, gap, iter, nodes, Ttot,
            opt_known, status);
    fclose(f);
}

static void print_num(FILE *f, double v) {
    if (isfinite(v)) fprintf(f, "%.6f", v);
    else fprintf(f, "NA");
}

GapTrace *gap_trace_open(const char *path) {
    if (!path || !*path) return NULL;
    FILE *probe = fopen(path, "r");
    int exists = 0;
    if (probe) { exists = 1; fclose(probe); }

    FILE *f = fopen(path, "a");
    if (!f) return NULL;
    if (!exists) {
        fprintf(f, "phase,iteration,elapsed_time,LB,UB,gap,cuts_added,lazy_cuts,nodes,total_cuts,separation_calls\n");
    }
    GapTrace *gt = malloc(sizeof(GapTrace));
    if (!gt) { fclose(f); return NULL; }
    gt->f = f;
    return gt;
}

void gap_trace_close(GapTrace *gt) {
    if (!gt) return;
    if (gt->f) fclose(gt->f);
    free(gt);
}

void gap_trace_log(GapTrace *gt, const char *phase, long iteration,
                   double elapsed_time, double LB, double UB, double gap,
                   long cuts_added, long lazy_cuts, double nodes,
                   long total_cuts, long separation_calls) {
    if (!gt || !gt->f) return;
    fprintf(gt->f, "%s,%ld,", phase ? phase : "NA", iteration);
    print_num(gt->f, elapsed_time); fprintf(gt->f, ",");
    print_num(gt->f, LB); fprintf(gt->f, ",");
    print_num(gt->f, UB); fprintf(gt->f, ",");
    print_num(gt->f, gap); fprintf(gt->f, ",");
    fprintf(gt->f, "%ld,%ld,", cuts_added, lazy_cuts);
    print_num(gt->f, nodes); fprintf(gt->f, ",%ld,%ld\n", total_cuts, separation_calls);
    fflush(gt->f);
}
