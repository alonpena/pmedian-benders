# Notas del solver (Gurobi C API)

> Documentado a partir de los headers **instalados en esta máquina**:
> `/Library/gurobi1200/macos_universal2/include/gurobi_c.h` (Gurobi **12.0.0**).
> No confiar en firmas memorizadas — estas son las reales de esta instalación.

## Instalación detectada

- Versiones presentes en `/Library/`: `gurobi1001`, `gurobi1102`, `gurobi1200`.
- **Usamos 12.0.0** (la más nueva).
- `GUROBI_HOME` (sugerido): `/Library/gurobi1200/macos_universal2`.
- Include: `$GUROBI_HOME/include/gurobi_c.h`.
- Lib: `$GUROBI_HOME/lib/libgurobi120.dylib` → enlazar con `-lgurobi120`.
- Licencia: `/Users/apena/gurobi.lic` (académica, expira **2027-06-15**). Verificada: modelo trivial resuelve OK.
- En macOS hay que exponer la lib en runtime: `DYLD_LIBRARY_PATH=$GUROBI_HOME/lib`.

## Firmas exactas (copiadas del header)

### Entorno y modelo
```c
/* macros: se expanden a *internal con los números de versión */
#define GRBloadenv(envP, logfilename)  GRBloadenvinternal(envP, logfilename, MAJ, MIN, TECH)
#define GRBemptyenv(envP)              GRBemptyenvinternal(envP, MAJ, MIN, TECH)

int GRBstartenv(GRBenv *env);
GRBenv *GRBgetenv(GRBmodel *model);
void    GRBfreeenv(GRBenv *env);

int GRBnewmodel(GRBenv *env, GRBmodel **modelP, const char *Pname, int numvars,
                double *obj, double *lb, double *ub, char *vtype, char **varnames);
int GRBupdatemodel(GRBmodel *model);
int GRBoptimize(GRBmodel *model);
int GRBfreemodel(GRBmodel *model);
```

### Variables y restricciones
```c
int GRBaddvar(GRBmodel *model, int numnz, int *vind, double *vval,
              double obj, double lb, double ub, char vtype, const char *varname);

int GRBaddconstr(GRBmodel *model, int numnz, int *cind, double *cval,
                 char sense, double rhs, const char *constrname);
/* sense: GRB_LESS_EQUAL '<', GRB_GREATER_EQUAL '>', GRB_EQUAL '=' */
```

### Atributos y parámetros
```c
int GRBgetintattr(GRBmodel *m, const char *name, int *valueP);
int GRBsetintattr(GRBmodel *m, const char *name, int newvalue);
int GRBgetdblattr(GRBmodel *m, const char *name, double *valueP);
int GRBgetdblattrarray(GRBmodel *m, const char *name, int start, int len, double *values);
int GRBsetdblattrelement(GRBmodel *m, const char *name, int element, double newvalue);

int GRBsetintparam(GRBenv *env, const char *paramname, int value);
int GRBsetdblparam(GRBenv *env, const char *paramname, double value);
```
- `ModelSense`: `GRB_MINIMIZE` (+1) / `GRB_MAXIMIZE` (-1).
- `GRB_INT_PAR_LAZYCONSTRAINTS` = `"LazyConstraints"` → poner a **1** para usar cortes perezosos.

### Callbacks (corazón de Fase 2)
```c
/* La firma del callback la fija el macro CB_ARGS: */
#define CB_ARGS GRBmodel *model, void *cbdata, int where, void *usrdata
/* => int __stdcall mycb(GRBmodel *model, void *cbdata, int where, void *usrdata); */

int GRBsetcallbackfunc(GRBmodel *model, int (*cb)(CB_ARGS), void *usrdata);

int GRBcbget(void *cbdata, int where, int what, void *resultP);

int GRBcblazy(void *cbdata, int lazylen, const int *lazyind,
              const double *lazyval, char lazysense, double lazyrhs);

int GRBcbsolution(void *cbdata, const double *solution, double *objvalP); /* inyectar heurística */
```

Constantes de callback relevantes:
- `GRB_CB_MIPSOL` = **4** (where: se encontró una solución entera candidata).
- `GRB_CB_MIPSOL_SOL` = **4001** (what para `GRBcbget`: obtener el vector solución `y` entero).
- `GRB_CB_MIPSOL_OBJ` = 4002, `GRB_CB_MIPSOL_OBJBST` = 4003, `GRB_CB_MIPSOL_OBJBND` = 4004.

## Flujo de la lazy-constraint callback (branch-and-Benders-cut)

1. Antes de optimizar el MIP: `GRBsetintparam(env, "LazyConstraints", 1)`.
2. Registrar: `GRBsetcallbackfunc(model, benders_cb, &data)` donde `data` lleva instancia + matriz S + índices de variables `y` y `theta`.
3. Dentro de `benders_cb`, **solo** cuando `where == GRB_CB_MIPSOL`:
   - Reservar `double *ybar` de tamaño M, `double *thetabar` de tamaño N.
   - `GRBcbget(cbdata, where, GRB_CB_MIPSOL_SOL, ybar)` → primero las `y`, luego las `theta` (según el orden en que se agregaron las variables; conviene agregar `y_0..y_{M-1}` y luego `theta_0..theta_{N-1}` para que `MIPSOL_SOL` sea contiguo). Hacer **una** llamada con buffer de tamaño numVars y partir el vector.
   - Para cada cliente i: correr Algoritmo 1 (calcular `k̃_i`, `OPT(SP_i)` ec.18). Si `thetabar[i] < OPT - eps`: construir corte (ec.20) y agregarlo con `GRBcblazy(cbdata, len, ind, val, GRB_GREATER_EQUAL, rhs)`.
4. Retornar 0 (no error). El solver reanuda el branch-and-cut.

Detalle del corte (ec.20) como fila lineal `theta_i + sum_j coef_j * y_j >= rhs`:
- Si `k̃_i = 0`: `theta_i >= D^1_i`  → `ind=[theta_i]`, `val=[1]`, sense `>`, rhs `D^1_i`.
- Si `k̃_i > 0`: `theta_i + sum_{j: d_ij <= D^{k̃}_i} (D^{k̃+1}_i - d_ij) y_j >= D^{k̃+1}_i`.

## CPLEX
`cplex.h` **no** está presente en esta máquina → backend CPLEX no disponible ahora.
Equivalentes (para referencia futura, sin verificar aquí): `CPXcallbacksetfunc` con
contexto `CPX_CALLBACKCONTEXT_CANDIDATE`, `CPXcallbackgetcandidatepoint`,
`CPXcallbackrejectcandidate` (lazy). Documentar al integrar.
