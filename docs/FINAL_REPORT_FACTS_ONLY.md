# Final report facts only

Use this file as approved factual content for report/slides/defense. No embellishment.

## One-sentence scope

Este proyecto replica el mecanismo algorítmico central de Duran-Mateluna, Ales & Elloumi (2023) y verifica localmente un subconjunto computacional; no replica toda la campaña experimental ni reejecuta Zebra.

## What is implemented

| Fact | Status | Evidence |
|---|---|---|
| Master variables are `y_j` and `theta_i`, not `x_ij` or `z_i^k` | VERIFIED_LOCAL | `src/phase1.c`, `src/phase2.c` |
| Objective is `min sum_i theta_i` | VERIFIED_LOCAL | `solver_add_vars` objective for theta in phases |
| Constraint `sum_j y_j = p` is enforced | VERIFIED_LOCAL | `src/phase1.c`, `src/phase2.c` |
| Phase 1 uses continuous `y in [0,1]` | VERIFIED_LOCAL | `solver_add_vars(...,'C')` in `src/phase1.c` |
| Phase 2 uses binary `y` | VERIFIED_LOCAL | `solver_add_vars(...,'B')` in `src/phase2.c` |
| Separator computes `ktilde_i` using sorted sites | VERIFIED_LOCAL | `src/separation.c`, `src/sortsites.c` |
| Generated cuts are optimality cuts | VERIFIED_LOCAL | `p1_add_cut`, `p2_add_lazy` |
| No feasibility cuts are implemented | VERIFIED_LOCAL | no code path; SP always feasible/acotado |
| Warm-start loads Phase 1 cuts into Phase 2 | VERIFIED_LOCAL | `src/cutpool.c`, `src/phase2.c` |
| Gurobi lazy callback is used | VERIFIED_LOCAL | `GRBcblazy` in `src/solver_gurobi.c` |

## What is not implemented

| Item | Status |
|---|---|
| Zebra | NOT_IMPLEMENTED / NOT_RUN |
| PopStar | NOT_IMPLEMENTED |
| Constraint reduction | NOT_IMPLEMENTED |
| Reduced-cost fixing | NOT_IMPLEMENTED |
| CPLEX backend | NOT_IMPLEMENTED |
| SCIP/HiGHS backend | NOT_IMPLEMENTED |
| Monolithic F1/F2/F3/F4 C benchmark | NOT_IMPLEMENTED |
| User-friendly non-contaminating benchmark pipeline | IMPLEMENTED (`scripts/paperbench.py`) |
| ODM forbidden assignments | NOT_IMPLEMENTED |

## What was run locally

| Experiment | Status | Evidence |
|---|---|---|
| `toy1` tests | VERIFIED_LOCAL | `make test` |
| Separator C vs hand derivation | VERIFIED_LOCAL | `tests/test_separation_toy.c` |
| Separator C vs Python oracle | VERIFIED_LOCAL | `scripts/verify_cuts.py`, `results/logs/verify_cuts_oracle_diff.log` |
| OR-Library `pmed1`–`pmed15` | VERIFIED_LOCAL | `results/orlib_optima_check.csv` |
| `rl1304` Table 2 subset | VERIFIED_LOCAL | `results/comparison_vs_paper.csv` |
| `kroA100` | VERIFIED_LOCAL | `results/benchmark.csv`, `results/logs/kroA100.pmp_p10_full.log` |
| Warm/cold comparison on 3 OR-Library instances | VERIFIED_LOCAL | `results/warmstart_comparison.csv` |
| Tiny RW asymmetric validation | PARTIAL_LOCAL | `instances/orlib/rw12.pmp`, DEVLOG/tests |

## What was not run locally

| Experiment | Status |
|---|---|
| Zebra comparison | NOT_RUN |
| Large TSP campaign | NOT_RUN |
| Huge TSP campaign | NOT_RUN |
| BIRCH campaign | NOT_RUN |
| RW large campaign | NOT_RUN |
| ODM campaign | NOT_RUN |

## Defendable numerical facts

| Fact | Source |
|---|---|
| OR-Library `pmed1`–`pmed15`: 15/15 match official optimum, delta 0 | `results/orlib_optima_check.csv` |
| `rl1304`: 9/9 match paper OPT, delta 0 | `results/comparison_vs_paper.csv` |
| `kroA100`: opt 30539 | `results/benchmark.csv`, log |
| `toy1`: opt 6 | `make test` |
| C vs Python separator: 0 diffs | `results/logs/verify_cuts_oracle_diff.log` |
| pmed1 callback proof: lazy_cuts=90, nodes=1 | `results/logs/pmed1.pmp_p5_full.log` |
| rl1304 p=5 callback proof: lazy_cuts=1850 | `results/logs/rl1304_p5.pmp_p5_full.log` |
| Warm-start pmed1 nodes 223→1 | `results/warmstart_comparison.csv` |
| Warm-start pmed6 nodes 632→7 | `results/warmstart_comparison.csv` |
| Warm-start pmed11 nodes 352→1 | `results/warmstart_comparison.csv` |

## Defendable interpretation

1. The implementation is a Benders/F4-style lazy-cut method derived from F3, not a monolithic F3 C solver.
2. The separator is the critical replicated component and is verified by hand, tests, and Python oracle.
3. Phase 2 is real branch-and-Benders-cut because lazy cuts are logged.
4. Warm-start reduces B&B nodes and lazy cuts in recorded tests.
5. Local computational replication is limited but traceable.

## Required caveats

1. Zebra is a paper comparator only. This repo does not run Zebra.
2. Timings vs paper are machine/solver dependent and not direct performance claims.
3. PopStar absence explains weaker `UB1` in some `rl1304` rows.
4. Large-scale claims belong to the paper, not to local experiments.
5. `O(NM)` separation is implemented by algorithmic structure; huge-scale timing is not measured.

## Sentences allowed in final report

- “La implementación C principal es Benders/F4 con cortes perezosos derivada de F3; F1–F4 se presentan como formulaciones matemáticas, no como modelos monolíticos C seleccionables.”
- “Se implementó el maestro de Benders con variables `y_j` y `theta_i`, y cortes de optimalidad generados perezosamente.”
- “La separación implementa el cálculo de `ktilde_i` usando sitios ordenados `S_i`, sin resolver LPs de subproblema.”
- “OR-Library `pmed1`–`pmed15` coincide con los óptimos oficiales en las 15 instancias corridas.”
- “Para `rl1304`, los 9 óptimos de la Tabla 2 del paper se reproducen localmente.”
- “Zebra no fue reejecutado; la comparación con Zebra se cita como resultado del paper.”

## Sentences forbidden unless new evidence is added

- “Nuestra implementación supera a Zebra.”
- “Replicamos toda la campaña computacional del paper.”
- “PopStar fue implementado.”
- “Reduced-cost fixing está implementado.”
- “Constraint reduction está implementado.”
- “El warm-start mejora siempre el tiempo.”
- “Corrimos BIRCH/RW grande/ODM/huge TSP.”
- “Comparamos contra un monolítico C equivalente.”
- “Las instancias BIRCH generadas localmente son las BIRCH exactas del paper.”
