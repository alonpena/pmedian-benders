/* logging.h — utilidades de tiempo y registro CSV (brief seccion 9 del kickoff). */
#ifndef PMP_LOGGING_H
#define PMP_LOGGING_H

double wall_seconds(void);   /* reloj monotonico en segundos */

/* Agrega (append) una fila al CSV de benchmark; crea cabecera si el archivo no existe.
 * Columnas: instance,N,M,p,backend,mode,LB1,UB1,T1,gap,iter,nodes,Ttot,opt_known,status */
void csv_append(const char *path, const char *instance, int N, int M, int p,
                const char *backend, const char *mode,
                double LB1, double UB1, double T1, double gap,
                long iter, double nodes, double Ttot,
                const char *opt_known, const char *status);

#endif
