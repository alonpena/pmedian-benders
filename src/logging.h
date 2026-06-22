/* logging.h — utilidades de tiempo, CSV y trazas experimentales. */
#ifndef PMP_LOGGING_H
#define PMP_LOGGING_H

typedef struct GapTrace GapTrace;

double wall_seconds(void);   /* reloj monotonico en segundos */

/* Agrega (append) una fila al CSV de benchmark; crea cabecera si el archivo no existe.
 * Columnas: instance,N,M,p,backend,mode,LB1,UB1,T1,gap,iter,nodes,Ttot,opt_known,status */
void csv_append(const char *path, const char *instance, int N, int M, int p,
                const char *backend, const char *mode,
                double LB1, double UB1, double T1, double gap,
                long iter, double nodes, double Ttot,
                const char *opt_known, const char *status);

/* Traza gap/curva por iteracion/callback. Append-only: no pisa trazas previas. */
GapTrace *gap_trace_open(const char *path);
void      gap_trace_close(GapTrace *gt);
void      gap_trace_log(GapTrace *gt, const char *phase, long iteration,
                        double elapsed_time, double LB, double UB, double gap,
                        long cuts_added, long lazy_cuts, double nodes,
                        long total_cuts, long separation_calls);

#endif
