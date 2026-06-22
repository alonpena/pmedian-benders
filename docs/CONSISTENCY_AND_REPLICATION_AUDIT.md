# Consistency and replication audit — pmedian-benders

Fecha auditoría: 2026-06-19/20. Rol: auditor escéptico OR. Fuente principal: código C, scripts, CSV/logs, tests. Regla: docs no prueban implementación; código y artefactos sí.

Estados usados: `VERIFIED_LOCAL`, `PARTIAL_LOCAL`, `PAPER_REPORTED_ONLY`, `NOT_IMPLEMENTED`, `NOT_RUN`, `UNSUPPORTED_CLAIM`.

## Veredicto corto

Defendible:

> Replicación algorítmica completa del mecanismo central del paper + replicación computacional parcial documentada.

No defendible:

> “Nuestra implementación supera a Zebra.”

Zebra no está implementado ni corrido localmente. La comparación con Zebra es claim del paper.

Wording seguro:

> The paper reports that this method outperforms Zebra; this project does not rerun Zebra. Therefore, the comparison with Zebra is treated as a literature claim, not as a local experimental result.

---

## 1. Formulación realmente implementada

| Formulación | ¿Implementada en C? | Evidencia código | Estado | Veredicto |
|---|---:|---|---|---|
| F1 clásica con `x_ij`, `y_j` | No como solver principal | No hay variables `x_ij` en `src/phase1.c`/`src/phase2.c`; solo evaluador/brute force en `src/instance.c` para instancias chicas | NOT_IMPLEMENTED como método | F1 aparece en informe y brute-force evalúa sets; no es modelo C usado. |
| F2 con radios `z_i^k` | No | No hay variables `z` en maestro C; no se materializan restricciones F2 | NOT_IMPLEMENTED | Solo teoría/documentación. |
| F3 de Elloumi con variables `z_i^k` | No explícitamente en C; sí como base matemática y oráculo Python | `prototype/pmp_benders.py` tiene F3; C deriva cortes desde estructura F3 pero no crea `z` | PARTIAL_LOCAL | Implementación C es Benders derivado de F3, no F3 monolítico. |
| F4 compacta completa con todos los cortes | No completa upfront | Cortes se generan dinámicamente en `src/separation.c`, `src/phase1.c`, `src/phase2.c` | PARTIAL_LOCAL | Implementación = F4/Benders lazy, no F4 entera cargada al solver. |
| Adaptación propia | Sí | Maestro con `y_j`, `theta_i`, cortes cerrados, dos fases | VERIFIED_LOCAL | Método real = Benders sobre `y/theta` con cortes óptimos derivados de F3/F4. |

Conclusión de formulación: **no se resuelve F1/F2/F3/F4 monolítico en C**. El solver principal implementa **maestro Benders `y, theta` + cortes de optimalidad generados on demand**, equivalente operacional a F4 perezosa derivada de F3.

---

## 2. Descomposición de Benders real

| Componente | Implementación real | Evidencia | Estado |
|---|---|---|---|
| Maestro | Variables `y_j` y `theta_i`; objetivo `min sum theta_i`; restricción `sum y=p` | `src/phase1.c`, `src/phase2.c` | VERIFIED_LOCAL |
| Subproblema | No se resuelve LP; se evalúa en forma cerrada por cliente dado `ybar` | `src/separation.c::separation_client` | VERIFIED_LOCAL |
| Cortes de optimalidad | `theta_i + sum coef_j y_j >= rhs` | `p1_add_cut`, `p2_add_lazy` | VERIFIED_LOCAL |
| Cortes de factibilidad | No existen | No hay rama/código para infeasibility cuts; teoría: SP siempre factible/acotado | NOT_IMPLEMENTED por diseño |
| LB | Valor objetivo del maestro LP en Fase 1 | `res.LB1 = solver_objval(s)` en `src/phase1.c` | VERIFIED_LOCAL |
| UB | Heurística de redondeo sobre `ybar`, evalúa conjunto abierto exacto | `rounding_heuristic`, `instance_eval_open_set` | VERIFIED_LOCAL |
| Phase 1 LP relaxation | `y` continuas `[0,1]`, `theta` continuas, loop de cortes | `src/phase1.c` | VERIFIED_LOCAL |
| Phase 2 branch-and-Benders-cut | `y` binarias + lazy callback `GRBcblazy` | `src/phase2.c`, `src/solver_gurobi.c`, `results/logs/*.log` | VERIFIED_LOCAL |
| Separación lineal con `ktilde_i` | Recorre sitios ordenados hasta cubrir 1, cuenta saltos de radio | `src/separation.c::separation_k_tilde` | VERIFIED_LOCAL |
| Matriz de sitios ordenados `S_i` | `S[i*M+r]` y `Dord[i*M+r]` por cliente | `src/sortsites.c` | VERIFIED_LOCAL |

Observación crítica: `separation_all` devuelve suma `OPT(SP_i)` y agrega cortes si `thetabar[i] < opt - tol`. Eso es separador, no solver de subproblema LP.

---

## 3. Mejoras del paper / estado local

| Mejora / componente | Estado | Evidencia |
|---|---|---|
| PopStar heuristic | NOT_IMPLEMENTED | `src/heuristic.c` solo ordena `ybar` y abre top-`p`; `src/heuristic.h` dice reemplaza PopStar |
| Rounding heuristic | VERIFIED_LOCAL | `src/heuristic.c::rounding_heuristic` |
| Constraint reduction | NOT_IMPLEMENTED | No hay código en `src/`; solo docs |
| Reduced-cost fixing | NOT_IMPLEMENTED | No hay lectura de reduced costs ni fijación de `y_j` |
| Warm start | VERIFIED_LOCAL | `src/cutpool.c`; `phase1_run(..., CutPool*)`; `phase2_run(..., warm)` precarga cortes |
| Callbacks Gurobi | VERIFIED_LOCAL | `solver_set_lazy_callback`, `GRBcblazy`, logs con `lazy_cuts>0` |
| Logs iteraciones/cortes/nodos | VERIFIED_LOCAL | `results/logs/*.log`; `results/benchmark.csv` |
| Backend CPLEX del paper | NOT_IMPLEMENTED | Solo `src/solver_gurobi.c` |
| Monolítico vs Benders benchmark | NOT_IMPLEMENTED | No hay solver monolítico C; solo prototipo F3/oráculo Python para chico |

---

## 4. Experimentos realmente corridos y presentes

| Experimento | Evidencia local persistente | Estado |
|---|---|---|
| `toy1` | `make test`, `tests/test_core.c`, `tests/test_separation_toy.c` | VERIFIED_LOCAL |
| OR-Library `pmed1`–`pmed15` | `results/orlib_optima_check.csv`, `results/benchmark.csv`, `results/logs/pmed*.log` | VERIFIED_LOCAL |
| TSPLIB `rl1304`, 9 valores de `p` Tabla 2 | `results/comparison_vs_paper.csv`, `results/logs/rl1304*.log` | VERIFIED_LOCAL |
| `kroA100` | `results/benchmark.csv`, `results/logs/kroA100.pmp_p10_full.log` | VERIFIED_LOCAL |
| `rw12` pequeño/asimétrico | `instances/orlib/rw12.pmp`, DEVLOG/tests cross-check | PARTIAL_LOCAL |
| Warm vs cold (`pmed1,pmed6,pmed11`) | `results/warmstart_comparison.csv` | VERIFIED_LOCAL |
| Large/huge TSP | No CSV/log | NOT_RUN |
| BIRCH grande | No instancia/log; solo generador | NOT_RUN |
| RW grande | No CSV/log | NOT_RUN |
| ODM | No parser/instancia/log | NOT_IMPLEMENTED / NOT_RUN |
| Zebra | No código/log/CSV | NOT_IMPLEMENTED / NOT_RUN |

---

## 5. Comandos ejecutados en esta auditoría

```bash
make clean && make                       # PASS, compila pmedian sin warnings visibles
make test                                # PASS
.venv/bin/python scripts/verify_cuts.py  # PASS, 0 diffs
.venv/bin/python tests/test_parse_orlib.py # PASS
```

Smoke benchmark ejecutado con restauración de CSV/logs curados después para evitar duplicados:

```bash
./pmedian instances/toy/toy1.pmp --p 2 --mode full --opt 6
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819
./pmedian instances/tsplib/kroA100.pmp --mode full
.venv/bin/python scripts/run_benchmark.py pmed1 pmed2
```

Resultados observados:

| Comando | Resultado observado | Estado |
|---|---|---|
| toy1 full | opt=6, lazy_cuts=2, nodes=1 | VERIFIED_LOCAL smoke |
| pmed1 full | opt=5819, lazy_cuts=90, nodes=1 | VERIFIED_LOCAL smoke |
| kroA100 full | opt=30539, lazy_cuts=162, nodes=1 | VERIFIED_LOCAL smoke |
| run_benchmark pmed1 pmed2 | both `OPT_MATCH` | VERIFIED_LOCAL smoke |

Nota: el binario no tiene parámetro de time limit. Protocolo recomendado usa wrapper externo `timeout=300` (ver `docs/EXPERIMENTAL_PROTOCOL.md`).

---

## 6. Tabla de resultados persistentes disponibles

### OR-Library

Fuente: `results/orlib_optima_check.csv`.

- Filas: `pmed1`–`pmed15`.
- Estado: 15/15 `OPT_MATCH`.
- Delta vs óptimo oficial: 0 en todas.

### TSPLIB `rl1304`

Fuente: `results/comparison_vs_paper.csv`.

- p: 5, 10, 20, 50, 100, 200, 300, 400, 500.
- Estado: 9/9 `OK`.
- `delta_OPT=0` en todas.
- Tiempos marcados `MACHINE_DEPENDENT`; no comparar directamente contra paper.

### Warm-start

Fuente: `results/warmstart_comparison.csv`.

| Instancia | cold nodes | warm nodes | cold lazy | warm lazy | Veredicto |
|---|---:|---:|---:|---:|---|
| pmed1 | 223 | 1 | 513 | 90 | reduce nodos/cortes |
| pmed6 | 632 | 7 | 1053 | 240 | reduce nodos/cortes; tiempo warm peor |
| pmed11 | 352 | 1 | 1768 | 308 | reduce nodos/cortes; tiempo warm peor |

Defendible: warm-start reduce nodos/cortes en estas corridas. No defender mejora general de wall-time.

---

## 7. Afirmaciones del informe/slides que deben calificarse

| Afirmación | Acción |
|---|---|
| “supera a Zebra” | Calificar: “el paper reporta”; no resultado local. |
| “estado del arte” | Calificar como contexto bibliográfico del paper. |
| “resuelve instancias enormes” | Calificar como paper-reported only. |
| “replicamos el paper completo” | Reemplazar por “replicamos el mecanismo algorítmico central; computacional parcial”. |
| “warm-start acelera” | Cambiar a “reduce nodos/cortes; wall-time mixto localmente”. |
| “PopStar usado” | Cambiar a “PopStar no implementado; se usa redondeo”. |
| “constraint reduction / reduced-cost fixing” | Declarar no implementado. |
| “comparación monolítico vs Benders” | No afirmar; no hay monolítico C defendible. |

Revisión actual: report/slides ya están mayormente calificados; mantener vigilancia si se editan PDFs.

---

## 8. Riesgos para informe final

1. Profesor pide Zebra: respuesta = no corrido; claim del paper.
2. Profesor pide campaña completa: no corrida; subset local documentado.
3. Profesor pide monolítico vs Benders: no hay monolítico C; solo oráculo/prototipo F3 en chico.
4. Profesor pide PopStar: no implementado; redondeo explica `UB1` peor en algunos `rl1304`.
5. Profesor pide escalabilidad `O(NM)` real: complejidad implementada, no perfil huge.
6. Profesor pide CPLEX: no usado; Gurobi 12.0 local.
7. Logs/CSV trazables existen, pero `results/benchmark.csv` es append-only; para regenerar limpio hay que borrar/respaldar antes.

---

## 9. Conclusión defendible

El repositorio implementa y verifica localmente el núcleo algorítmico del paper: maestro Benders `y/theta`, subproblema cerrado, cortes de optimalidad, separación con `S_i` y `ktilde_i`, Fase 1 LP, Fase 2 lazy callback, warm-start por cortes. Los experimentos locales son OR-Library, `rl1304`, `kroA100`, `toy1` y validación `rw12`. Zebra, PopStar, reduced-cost fixing, constraint reduction y campaña grande son fuera de alcance local.
