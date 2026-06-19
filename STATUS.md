# STATUS — pmedian-benders

_Snapshot: 2026-06-19 — final consistency/replication audit._

## Estado global

Repositorio listo para defensa como **replicación algorítmica completa + replicación computacional parcial documentada** del paper de Duran-Mateluna, Ales & Elloumi (2023).

## Implementado y verificado localmente

| Componente | Estado | Evidencia |
|---|---|---|
| F3 / maestro Benders (`y`, `theta`, `sum y=p`) | VERIFIED_LOCAL | `src/phase1.c`, `src/phase2.c`, `prototype/pmp_benders.py` |
| Subproblema primal/dual y cortes de optimalidad | VERIFIED_LOCAL | `src/separation.c`, `report/sections/05_benders.tex` |
| Algoritmos 1 y 2, separación `O(NM)` | VERIFIED_LOCAL | `make test`, `scripts/verify_cuts.py`, `results/logs/verify_cuts_oracle_diff.log` |
| Fase 1 LP + loop de cortes | VERIFIED_LOCAL | `src/phase1.c`, `results/benchmark.csv` |
| Fase 2 branch-and-Benders-cut con lazy callback | VERIFIED_LOCAL | `src/phase2.c`, `results/logs/*full.log` (`lazy_cuts>0`) |
| Warm-start = herencia de cortes de Fase 1 | VERIFIED_LOCAL | `src/cutpool.c`, `results/warmstart_comparison.csv` |
| OR-Library `pmed1`–`pmed15` | VERIFIED_LOCAL | `results/orlib_optima_check.csv` (15/15, delta=0) |
| TSPLIB `rl1304` Tabla 2 | VERIFIED_LOCAL | `results/comparison_vs_paper.csv` (9/9 OPT, delta=0) |
| `kroA100` F3 oracle check | VERIFIED_LOCAL | `results/benchmark.csv`, `results/logs/kroA100...log` |
| RW asimétrica pequeña `rw12` | PARTIAL_LOCAL | `instances/orlib/rw12.pmp`, DEVLOG/test cross-check |

## No implementado / no corrido

| Tema | Estado |
|---|---|
| Zebra | NOT_IMPLEMENTED / NOT_RUN |
| PopStar | NOT_IMPLEMENTED (reemplazado por redondeo uniforme) |
| reduced-cost fixing | NOT_IMPLEMENTED |
| constraint reduction | NOT_IMPLEMENTED |
| CPLEX/SCIP | NOT_IMPLEMENTED (solo Gurobi compilado) |
| TSP grandes/huge, BIRCH, RW grande, ODM | NOT_RUN |

## Regla de honestidad para defensa

El paper reporta que este método supera a Zebra; este proyecto no reejecuta Zebra. Por lo tanto, la comparación con Zebra se trata como una afirmación de literatura, no como un resultado experimental local.

## Comandos de verificación

```bash
make test
make pmedian
.venv/bin/python scripts/verify_cuts.py
.venv/bin/python scripts/run_benchmark.py
.venv/bin/python scripts/compare_paper.py
.venv/bin/python scripts/plot_results.py
```

## Artefactos finales

- Informe fuente: `report/main.tex`
- Slides fuente: `slides/main.tex`
- Paquete Overleaf informe: `overleaf/report/`
- Paquete Overleaf slides: `overleaf/slides/`
- Auditoría final: `docs/FINAL_SUBMISSION_AUDIT.md`
