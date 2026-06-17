/* logging.c — implementacion de utilidades de tiempo y CSV. */
#include "logging.h"
#include <stdio.h>
#include <time.h>

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
