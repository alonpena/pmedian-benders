# pmedian-benders

Replicación en C de la descomposición de Benders eficiente para el **problema de las p-medianas (pMP)**, basada en:

> Duran-Mateluna, C., Ales, Z. & Elloumi, S. (2023). *An efficient Benders decomposition for the p-median problem*. European Journal of Operational Research, 308, 84–96.

Proyecto del curso **Optimización Computacional** (PUCV).

## Alcance de la replicación

- **Replicación algorítmica completa del núcleo:** F3, maestro de Benders, subproblema primal/dual, cortes de optimalidad, separación cerrada `O(NM)`, Fase 1 LP, Fase 2 branch-and-Benders-cut y warm-start por cortes de Fase 1.
- **Replicación computacional parcial documentada:** solo instancias efectivamente ejecutadas y registradas en `results/`.
- **Zebra no fue reejecutado localmente.** El paper reporta que el método supera a Zebra; este proyecto no valida esa comparación como resultado local.
- **No corrido localmente:** campaña completa de gran escala del paper (TSP grandes/huge, BIRCH, RW grande, ODM).
- **No implementado:** PopStar, reduced-cost fixing, constraint reduction, CPLEX/SCIP.

## Estado del proyecto

| Componente | Estado | Evidencia |
|---|---|---|
| Núcleo C + Gurobi | Implementado | `src/` |
| Separador Alg. 1/2 | Verificado 3 vías | `make test`, `scripts/verify_cuts.py`, `results/logs/verify_cuts_oracle_diff.log` |
| Fase 1 LP + cortes | Implementada | `src/phase1.c`, `results/benchmark.csv` |
| Fase 2 branch-and-Benders-cut | Implementada | `src/phase2.c`, `results/logs/*full.log` |
| Warm-start por cortes Fase 1 | Implementado | `results/warmstart_comparison.csv` |
| OR-Library pmed1–15 | Corrido localmente, 15/15 óptimos | `results/orlib_optima_check.csv` |
| TSPLIB rl1304 | Corrido localmente, 9/9 óptimos vs paper Tabla 2 | `results/comparison_vs_paper.csv` |
| Zebra | No implementado, no corrido | tratado como claim del paper |

## Arquitectura

- **Núcleo en C:** lectura de instancias, distancias `d(i,j)`, matriz `S`, separación `O(NM)`, Fase 1, Fase 2, warm-start, logging.
- **Solver:** API C de **Gurobi** detrás de `src/solver.h`.
- **Prototipo Python+Gurobi:** oráculo legible para validar F3, callbacks y separador.
- **Scripts:** parsers OR-Library/TSPLIB, generadores RW/BIRCH, benchmark y figuras.

## Requisitos

- Compilador C y `make`.
- Gurobi con licencia activa (`GUROBI_HOME` o autodetección del `Makefile`).
- Python 3 para scripts y prototipo.

## Uso

```bash
make test
make pmedian

./pmedian instances/toy/toy1.pmp --p 2 --mode full
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819

.venv/bin/python scripts/verify_cuts.py
.venv/bin/python scripts/run_benchmark.py
.venv/bin/python scripts/compare_paper.py
.venv/bin/python scripts/plot_results.py
```

## Documentos clave

- `docs/CONSISTENCY_AND_REPLICATION_AUDIT.md` — auditoría honesta de alcance.
- `docs/PAPER_REPLICATION_MATRIX.md` — matriz paper vs repo.
- `docs/NUMERICAL_CLAIMS_TRACE.md` — trazabilidad de números del informe/slides.
- `docs/FINAL_SUBMISSION_AUDIT.md` — checklist final de entrega.
- `overleaf/README_OVERLEAF.md` — paquetes Overleaf limpios.
