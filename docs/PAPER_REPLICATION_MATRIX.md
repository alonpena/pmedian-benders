# Matriz de replicación del paper

Paper: Duran-Mateluna, Ales & Elloumi (2023), *An efficient Benders decomposition for the p-median problem*.

Regla de lectura: solo evidencia local cuenta como resultado local. Si Zebra no fue corrido, no se dice “nuestra implementación supera a Zebra”.

**Wording obligatorio:** “The paper reports that this method outperforms Zebra; this project does not rerun Zebra. Therefore, the comparison with Zebra is treated as a literature claim, not as a local experimental result.”

## Tabla maestra

| Paper component / experiment | Paper location | What paper does | What this repo does | Local evidence | Status | Defense-safe wording |
|---|---|---|---|---|---|---|
| F3 formulation | §2 | Usa F3 de Elloumi como formulación fuerte/rala base. | Replica F3 en teoría; usa maestro Benders derivado de F3; mantiene prototipo F3 como oráculo. | `report/sections/03_formulaciones.tex`; `prototype/pmp_benders.py`; `docs/AUDIT.md` #10 | VERIFIED_LOCAL | “Replicamos F3 como base matemática y validamos contra oráculo F3 en instancias pequeñas.” |
| Benders master | §3.1–3.2 | Maestro con variables `y_j`, `theta_i`, restricción `sum y=p`, cortes. | Implementa maestro LP/MIP en Fase 1/2. | `src/phase1.c`; `src/phase2.c`; `results/benchmark.csv` | VERIFIED_LOCAL | “El maestro de Benders está implementado en C.” |
| Primal subproblem | §3.2 | Fijado `y`, separa por cliente; calcula distancia asignación vía variables de radio. | Derivado en informe; evaluado por separador, sin resolver LP explícito. | `report/sections/05_benders.tex`; `src/separation.c` | VERIFIED_LOCAL | “El subproblema se usa por su forma cerrada, no como LP llamado al solver.” |
| Dual subproblem | §3.2 | Deriva dual y puntos extremos que producen cortes. | Derivado en informe; solución cerrada codificada. | `report/sections/05_benders.tex`; `report/sections/06_separacion.tex`; `src/separation.c` | VERIFIED_LOCAL | “Replicamos el dual y explotamos su solución cerrada.” |
| Benders optimality cuts | §3.2, Eq. 16/20 | Genera cortes de optimalidad; no requiere cortes de factibilidad. | Implementa cortes `theta_i + sum coef*y >= rhs`. | `src/separation.c`; `src/phase1.c`; `src/phase2.c`; `results/logs/*full.log` | VERIFIED_LOCAL | “Solo hay cortes de optimalidad porque el subproblema siempre es factible y acotado.” |
| Algorithm 1 separation | §3.3 | Recorre clientes, separa cortes violados. | `separation_all` recorre `N` clientes y agrega cortes vía callback/sink. | `src/separation.c`; `make test`; `scripts/verify_cuts.py` | VERIFIED_LOCAL | “Algoritmo 1 está implementado y probado.” |
| Algorithm 2 `ktilde` computation | §3.3 | Calcula índice `ktilde_i` en `O(M)` por cliente. | `separation_k_tilde` recorre sitios ordenados y acumula `ybar`. | `src/separation.c`; `tests/test_separation_toy.c` | VERIFIED_LOCAL | “Algoritmo 2 está implementado y validado con cortes derivados a mano.” |
| `O(NM)` separation | §3.3 | Separación cerrada `O(NM)` por iteración. | Estructura de código es `O(M)` por cliente; verificada hasta `N=1304`, sin timing aislado a gran escala. | `src/separation.c`; `results/benchmark.csv`; no perfil a `>10^4` | PARTIAL_LOCAL | “La complejidad algorítmica está replicada; no medimos escalabilidad masiva.” |
| Phase 1 LP relaxation | §3.5 / Alg. 3 | Resuelve maestro LP con cortes y obtiene `LB1/UB1`. | Implementa Fase 1 con redondeo uniforme (no PopStar). | `src/phase1.c`; `results/benchmark.csv`; `results/comparison_vs_paper.csv` | VERIFIED_LOCAL | “Fase 1 está replicada; la heurística inicial difiere.” |
| Phase 2 branch-and-Benders-cut | §3.5 | MIP con lazy constraints. | Implementa callback lazy con Gurobi. | `src/phase2.c`; `results/logs/*full.log` (`lazy_cuts>0`) | VERIFIED_LOCAL | “Fase 2 es branch-and-Benders-cut real; los logs prueban cortes lazy.” |
| Warm-start from Phase 1 cuts/bounds | §3.5 | Fase 2 hereda cortes/cotas de Fase 1. | Hereda cortes de Fase 1 como restricciones iniciales; no prueba ventaja wall-time general. | `src/cutpool.c`; `src/phase1.c`; `src/phase2.c`; `results/warmstart_comparison.csv` | VERIFIED_LOCAL | “Warm-start por cortes está implementado; reduce nodos localmente, tiempo mixto.” |
| OR-Library | §4 | Paper la menciona como benchmark estándar; no tabla local del paper en repo. | Corre `pmed1`–`pmed15` y compara con óptimos oficiales Beasley. | `results/orlib_optima_check.csv`; `results/logs/pmed*.log` | VERIFIED_LOCAL | “OR-Library se validó localmente contra óptimos oficiales: 15/15.” |
| `rl1304` / TSPLIB subset | §4, Table 2 | Reporta Tabla 2 small TSP para `rl1304` con 9 valores de `p`. | Transcribe Tabla 2 y corre los 9 `p`; compara OPT/LB1/UB1. | `results/comparison_vs_paper.csv`; `scripts/compare_paper.py`; logs `rl1304_*` | VERIFIED_LOCAL | “Reproducimos la Tabla 2 para `rl1304`: 9/9 óptimos.” |
| Zebra | §4 | Compara contra Zebra y reporta ventaja. | No implementa ni ejecuta Zebra. | `rg Zebra src scripts results` sin binario/log; docs declaran ausencia | PAPER_REPORTED_ONLY / NOT_RUN | “Zebra no fue reejecutado; comparación tratada como literatura.” |
| PopStar | §3.5 | Usa PopStar como heurística inicial. | No implementa PopStar; usa arranque uniforme + redondeo. | `src/heuristic.h`; `src/heuristic.c`; `results/comparison_vs_paper.csv` (`UB1` peor en algunos p) | NOT_IMPLEMENTED | “PopStar quedó fuera; esto afecta `UB1`, no la validez de Benders.” |
| Reduced-cost fixing | §3.5 | Aplica fijación por costos reducidos bajo ciertas condiciones. | No implementado. | `rg "reduced-cost|reduced cost|rc_" src` sin implementación | NOT_IMPLEMENTED | “No implementamos reduced-cost fixing.” |
| Constraint reduction | §3.5 | Reduce restricciones/cortes tras Fase 1. | No implementado. | `rg "constraint reduction|reduction" src` sin implementación | NOT_IMPLEMENTED | “No implementamos constraint reduction.” |
| Large TSP | §4, Tables 3–? | Corre TSPLIB medianas/grandes. | No corre esas familias; solo raw `.tsp` algunos presentes sin `.pmp`/logs. | No CSV/log local; `instances/tsplib/fl1400.tsp`, `u1432.tsp`, `vm1748.tsp` sin resultados | NOT_RUN | “No hay resultados locales para TSP medianas/grandes fuera de `rl1304` y `kroA100`.” |
| Huge TSP | §4 | Corre TSP huge hasta cientos de miles de puntos. | No corrido. | Sin instancias/results/logs huge | NOT_RUN | “Huge TSP es paper-reported only.” |
| BIRCH | §4 | Corre instancias BIRCH grandes. | Solo existe generador `scripts/gen_birch.py`; no resultados. | Sin `instances/*birch*`; sin CSV/log | NOT_RUN | “BIRCH no fue corrido localmente.” |
| RW | §4 | Corre familia RW de tamaño 100–1000 y casos difíciles. | Solo valida `rw12` pequeño/asimétrico. | `instances/orlib/rw12.pmp`; DEVLOG/test cross-check; sin CSV benchmark formal grande | PARTIAL_LOCAL | “RW solo se probó como validación pequeña, no como campaña del paper.” |
| ODM | §4 | Corre Optimal Diversity Management como pMP con asignaciones prohibidas. | No implementa asignaciones prohibidas ni corre ODM. | Sin parser/instancias/logs ODM | NOT_IMPLEMENTED / NOT_RUN | “ODM quedó fuera del alcance.” |

## Clasificación final

| Clase | Definición | Componentes |
|---|---|---|
| A. Fully replicated locally | Implementado y verificado con evidencia local. | F3, maestro, subproblema/dual, cortes, Alg. 1, Alg. 2, Fase 1, Fase 2, warm-start por cortes, OR-Library, `rl1304` Tabla 2. |
| B. Algorithmically replicated, partially tested | Código/derivación local existe, pero escala/campaña no se revalidó completa. | Separación `O(NM)` a gran escala; RW (solo `rw12`); TSPLIB fuera de `rl1304`/`kroA100`. |
| C. Paper-reported only | Descrito desde el paper; no medido localmente. | Superioridad frente a Zebra; resultados de gran escala reportados por paper. |
| D. Not implemented / not run | Ausente o no ejecutado. | Zebra, PopStar, reduced-cost fixing, constraint reduction, CPLEX/SCIP, large/huge TSP, BIRCH, RW grande, ODM. |

## Veredicto de defensa

Defensa segura: “Replicamos completamente el mecanismo algorítmico central y verificamos un subconjunto computacional trazable. No reejecutamos Zebra ni la campaña completa de gran escala; esas comparaciones son resultados del paper, no resultados locales.”
