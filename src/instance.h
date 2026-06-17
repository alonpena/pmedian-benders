/* instance.h — modelo de instancia del pMP y acceso a distancias d(i,j).
 *
 * Cubre Etapa 1 (parser + distancias) y Etapa 2 (evaluador fuerza bruta, oraculo).
 * Ver docs/INSTANCE_FORMAT.md (Variante A coordenadas / Variante B matriz) y
 * brief seccion 2.2. Distancias enteras se guardan como long; el objetivo se
 * acumula en double (brief: cuidado con TSP ~1e8).
 */
#ifndef PMP_INSTANCE_H
#define PMP_INSTANCE_H

typedef struct {
    int  N;            /* numero de clientes */
    int  M;            /* numero de sitios   */
    int  p;            /* sitios a abrir      */
    int  has_coords;   /* 1 = Variante A (coords), 0 = Variante B (matriz) */
    double *x;         /* coords (Variante A), tamano N */
    double *y;
    long  *matrix;     /* distancias (Variante B), tamano N*M, fila i: matrix[i*M+j] */
} Instance;

/* Carga una instancia .pmp. p_override < 0 => usar el p del archivo. */
Instance *instance_load(const char *path, int p_override);

/* d(i,j): euclidiana truncada (floor) para coords; entrada directa para matriz. */
long instance_dist(const Instance *inst, int i, int j);

/* Objetivo exacto dado un conjunto de sitios abiertos (suma de distancias minimas).
 * Etapa 2: oraculo. open_sites tiene k elementos. */
double instance_eval_open_set(const Instance *inst, const int *open_sites, int k);

/* Fuerza bruta: enumera C(M,p) conjuntos, devuelve el objetivo minimo y (opcional)
 * escribe el mejor conjunto en best_set (tamano p). Solo instancias chicas. */
double instance_brute_force(const Instance *inst, int *best_set);

void instance_free(Instance *inst);

#endif
