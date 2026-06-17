/* solver.h — capa de abstraccion delgada sobre el solver MILP/LP.
 *
 * Backend por defecto: Gurobi (ver src/solver_gurobi.c, ADR 0001). El nucleo en C
 * no incluye headers del solver: habla solo con esta interfaz. Fase 1 resuelve el
 * LP; Fase 2 resuelve el MIP con callback de lazy constraints.
 *
 * Convencion de sentidos:  '<' menor-igual, '>' mayor-igual, '=' igual.
 * Tipos de variable:       'C' continua, 'B' binaria.
 */
#ifndef PMP_SOLVER_H
#define PMP_SOLVER_H

typedef struct Solver Solver;

/* contexto opaco pasado al callback de lazy constraints */
typedef struct SolverCB SolverCB;

/* firma del callback de usuario: se invoca por cada solucion entera candidata.
 * Debe leer la solucion con solver_cb_get_solution y agregar cortes con
 * solver_cb_add_lazy. */
typedef void (*solver_lazy_fn)(SolverCB *cb, void *user);

Solver *solver_create(int silent);
void    solver_destroy(Solver *s);

/* Agrega n variables (mismo tipo, lb, ub). obj puede ser NULL (=> 0).
 * Devuelve el indice base de la primera variable agregada. */
int  solver_add_vars(Solver *s, int n, double lb, double ub, char vtype, const double *obj);

/* sum_{k} val[k]*x[ind[k]]  sense  rhs */
void solver_add_constr(Solver *s, int len, const int *ind, const double *val,
                       char sense, double rhs);

void solver_set_minimize(Solver *s);
void solver_set_int_param(Solver *s, const char *name, int v);
void solver_set_dbl_param(Solver *s, const char *name, double v);

int    solver_optimize(Solver *s);     /* 0 = optimo */
double solver_objval(Solver *s);
double solver_node_count(Solver *s);   /* nodos del B&B (Fase 2) */
/* copia x[start..start+len) en out */
void   solver_get_x(Solver *s, int start, int len, double *out);
int    solver_num_vars(Solver *s);

/* --- Fase 2: callback de lazy constraints --- */
void solver_enable_lazy(Solver *s);
void solver_set_lazy_callback(Solver *s, solver_lazy_fn fn, void *user);

/* dentro del callback: copia la solucion entera completa (todas las vars) en out
 * (out debe tener tamano solver_num_vars). */
void solver_cb_get_solution(SolverCB *cb, double *out);
/* agrega un corte perezoso: sum val[k]*x[ind[k]] sense rhs */
void solver_cb_add_lazy(SolverCB *cb, int len, const int *ind, const double *val,
                        char sense, double rhs);

#endif
