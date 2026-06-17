/* instance.c — implementacion del parser, d(i,j) y evaluador (Etapas 1-2). */
#include "instance.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

/* Lee la siguiente linea no vacia y no-comentario (# ...). Devuelve 0 al EOF. */
static int next_data_line(FILE *f, char *buf, int cap) {
    while (fgets(buf, cap, f)) {
        char *s = buf;
        while (*s == ' ' || *s == '\t') s++;
        if (*s == '\0' || *s == '\n' || *s == '#') continue;
        return 1;
    }
    return 0;
}

Instance *instance_load(const char *path, int p_override) {
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "no se pudo abrir %s\n", path); return NULL; }

    char line[1 << 16];
    if (!next_data_line(f, line, sizeof line)) { fclose(f); return NULL; }
    int N, M, p;
    if (sscanf(line, "%d %d %d", &N, &M, &p) != 3) { fclose(f); return NULL; }
    if (p_override >= 0) p = p_override;

    Instance *inst = calloc(1, sizeof(Instance));
    inst->N = N; inst->M = M; inst->p = p;

    /* mirar la siguiente linea: si es MATRIX => Variante B */
    long pos = ftell(f);
    if (next_data_line(f, line, sizeof line)) {
        char first[64] = {0};
        sscanf(line, "%63s", first);
        for (char *c = first; *c; c++) *c = toupper((unsigned char)*c);
        if (strcmp(first, "MATRIX") == 0) {
            inst->has_coords = 0;
            inst->matrix = malloc((size_t)N * M * sizeof(long));
            for (int i = 0; i < N; i++) {
                if (!next_data_line(f, line, sizeof line)) {
                    fprintf(stderr, "matriz incompleta en fila %d\n", i);
                    instance_free(inst); fclose(f); return NULL;
                }
                char *tok = strtok(line, " \t\n");
                for (int j = 0; j < M; j++) {
                    if (!tok) { fprintf(stderr, "fila %d corta\n", i); instance_free(inst); fclose(f); return NULL; }
                    inst->matrix[(size_t)i * M + j] = atol(tok);
                    tok = strtok(NULL, " \t\n");
                }
            }
            fclose(f);
            return inst;
        }
    }
    /* Variante A: coordenadas. Rebobinar a la primera linea de datos tras la cabecera. */
    fseek(f, pos, SEEK_SET);
    inst->has_coords = 1;
    inst->x = malloc((size_t)N * sizeof(double));
    inst->y = malloc((size_t)N * sizeof(double));
    for (int r = 0; r < N; r++) {
        if (!next_data_line(f, line, sizeof line)) {
            fprintf(stderr, "faltan coordenadas (fila %d)\n", r);
            instance_free(inst); fclose(f); return NULL;
        }
        int id; double xx, yy;
        if (sscanf(line, "%d %lf %lf", &id, &xx, &yy) != 3) {
            fprintf(stderr, "coordenada mal formada: %s", line);
            instance_free(inst); fclose(f); return NULL;
        }
        if (id < 0 || id >= N) id = r;   /* tolerar ids no consecutivos */
        inst->x[id] = xx; inst->y[id] = yy;
    }
    fclose(f);
    return inst;
}

long instance_dist(const Instance *inst, int i, int j) {
    if (!inst->has_coords)
        return inst->matrix[(size_t)i * inst->M + j];
    double dx = inst->x[i] - inst->x[j];
    double dy = inst->y[i] - inst->y[j];
    return (long)floor(sqrt(dx * dx + dy * dy));   /* euclidiana truncada */
}

double instance_eval_open_set(const Instance *inst, const int *open_sites, int k) {
    double total = 0.0;
    for (int i = 0; i < inst->N; i++) {
        long best = instance_dist(inst, i, open_sites[0]);
        for (int t = 1; t < k; t++) {
            long d = instance_dist(inst, i, open_sites[t]);
            if (d < best) best = d;
        }
        total += (double)best;
    }
    return total;
}

/* recursion de combinaciones para fuerza bruta */
static void brute_rec(const Instance *inst, int start, int depth, int *cur,
                      double *best, int *best_set) {
    if (depth == inst->p) {
        double v = instance_eval_open_set(inst, cur, inst->p);
        if (v < *best) {
            *best = v;
            if (best_set) memcpy(best_set, cur, inst->p * sizeof(int));
        }
        return;
    }
    for (int j = start; j <= inst->M - (inst->p - depth); j++) {
        cur[depth] = j;
        brute_rec(inst, j + 1, depth + 1, cur, best, best_set);
    }
}

double instance_brute_force(const Instance *inst, int *best_set) {
    double best = 1e300;
    int *cur = malloc(inst->p * sizeof(int));
    brute_rec(inst, 0, 0, cur, &best, best_set);
    free(cur);
    return best;
}

void instance_free(Instance *inst) {
    if (!inst) return;
    free(inst->x); free(inst->y); free(inst->matrix);
    free(inst);
}
