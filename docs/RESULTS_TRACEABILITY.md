# Results traceability

Auditoría de trazabilidad: cada resultado numérico defendible debe apuntar a CSV/log/test.

## Fuentes principales

| Archivo | Qué prueba | Estado |
|---|---|---|
| `results/orlib_optima_check.csv` | OR-Library `pmed1`–`pmed15` vs óptimos oficiales | VERIFIED_LOCAL |
| `results/comparison_vs_paper.csv` | `rl1304` Tabla 2 paper, 9 valores de `p` | VERIFIED_LOCAL |
| `results/benchmark.csv` | Corridas locales agregadas: LB1, UB1, T1, gap, iter, nodes, Ttot | VERIFIED_LOCAL |
| `results/warmstart_comparison.csv` | warm vs cold en `pmed1,pmed6,pmed11` | VERIFIED_LOCAL |
| `results/logs/*.log` | prueba callback: separation calls, lazy cuts, nodes | VERIFIED_LOCAL |
| `results/logs/verify_cuts_oracle_diff.log` | C separator vs Python oracle, 0 diffs | VERIFIED_LOCAL |
| `tests/test_separation_toy.c` | cortes derivados a mano para `toy1` | VERIFIED_LOCAL |
| `docs/ADR/0002-orlib-duplicate-edges.md` | regla OR-Library duplicate edges = last occurrence wins | VERIFIED_LOCAL |
| `scripts/validate_results.py` | Validator: benchmark duplicates, OPT_MATCH, logs/content | IMPLEMENTED_LOCAL |
| `results/curated/README.md` | Frozen evidence snapshot manifest at commit `d1f2e1e` | VERIFIED_LOCAL |

## OR-Library table

Fuente: `results/orlib_optima_check.csv`.

| Claim | Valor | Fuente | Status |
|---|---:|---|---|
| OR-Library corridas | 15 instancias `pmed1`–`pmed15` | `results/orlib_optima_check.csv` | VERIFIED_LOCAL |
| Óptimos oficiales alcanzados | 15/15 | `status=OPT_MATCH` | VERIFIED_LOCAL |
| Delta vs oficial | 0 en todas | columna `delta` | VERIFIED_LOCAL |
| Rango N local OR-Library | 100, 200, 300 | CSV/instances | VERIFIED_LOCAL |
| Rango p local OR-Library | 5–100 | CSV/instances | VERIFIED_LOCAL |

## `rl1304` / paper Table 2

Fuente: `results/comparison_vs_paper.csv`.

| Claim | Valor | Fuente | Status |
|---|---:|---|---|
| Filas `rl1304` comparadas | 9 | CSV | VERIFIED_LOCAL |
| Valores de `p` | 5,10,20,50,100,200,300,400,500 | CSV | VERIFIED_LOCAL |
| Óptimos coinciden | 9/9 | `delta_OPT=0` | VERIFIED_LOCAL |
| N | 1304 | CSV/instance | VERIFIED_LOCAL |
| Tiempos comparables con paper | No | `time_note=MACHINE_DEPENDENT` | VERIFIED_LOCAL caveat |
| `UB1` peor sin PopStar | p=10,100,300 | columns `paper_UB1`, `our_UB1` | VERIFIED_LOCAL |

## `kroA100`

Fuente: `results/benchmark.csv`, `results/logs/kroA100.pmp_p10_full.log`.

| Claim | Valor | Fuente | Status |
|---|---:|---|---|
| Instance | `kroA100.pmp` | benchmark/log | VERIFIED_LOCAL |
| N=M | 100 | benchmark/log | VERIFIED_LOCAL |
| p | 10 | benchmark/log | VERIFIED_LOCAL |
| Benders optimum | 30539 | benchmark/log | VERIFIED_LOCAL |
| Callback lazy cuts | 162 | log | VERIFIED_LOCAL |
| Nodes | 1 | benchmark/log | VERIFIED_LOCAL |

## Warm-start

Fuente: `results/warmstart_comparison.csv`.

| Claim | Valor | Fuente | Status |
|---|---:|---|---|
| pmed1 nodes cold→warm | 223→1 | CSV | VERIFIED_LOCAL |
| pmed6 nodes cold→warm | 632→7 | CSV | VERIFIED_LOCAL |
| pmed11 nodes cold→warm | 352→1 | CSV | VERIFIED_LOCAL |
| pmed1 lazy cuts cold→warm | 513→90 | CSV | VERIFIED_LOCAL |
| pmed6 lazy cuts cold→warm | 1053→240 | CSV | VERIFIED_LOCAL |
| pmed11 lazy cuts cold→warm | 1768→308 | CSV | VERIFIED_LOCAL |
| Wall-time always improves | false / not supported | CSV shows mixed | UNSUPPORTED_CLAIM |

## Separator correctness

| Claim | Valor | Fuente | Status |
|---|---:|---|---|
| `toy1` optimum | 6 | `make test`, `tests/test_core.c` | VERIFIED_LOCAL |
| `toy1` hand cuts match C | PASS | `tests/test_separation_toy.c` | VERIFIED_LOCAL |
| C vs Python separator | 0 diffs | `results/logs/verify_cuts_oracle_diff.log` | VERIFIED_LOCAL |
| `ktilde_2` in hand toy scenario | 2 | test output/source | VERIFIED_LOCAL |
| `theta_2` cut in hand toy scenario | `theta_2 >= 4 - 4y_2 - y_3` | `tests/test_separation_toy.c` | VERIFIED_LOCAL |

## Callback evidence

| Claim | Value | Source | Status |
|---|---:|---|---|
| pmed1 lazy cuts | 90 | `results/logs/pmed1.pmp_p5_full.log` | VERIFIED_LOCAL |
| pmed1 branch-and-Benders-cut flag | YES | same log | VERIFIED_LOCAL |
| rl1304 p=5 lazy cuts | 1850 | `results/logs/rl1304_p5.pmp_p5_full.log` | VERIFIED_LOCAL |
| kroA100 lazy cuts | 162 | `results/logs/kroA100.pmp_p10_full.log` | VERIFIED_LOCAL |

## Claims that are paper-only, not local

| Claim | Status | Required wording |
|---|---|---|
| Method outperforms Zebra | PAPER_REPORTED_ONLY | “The paper reports…” |
| Zebra memory issues | PAPER_REPORTED_ONLY | “The paper reports…” |
| Huge TSP optimality | PAPER_REPORTED_ONLY | “The paper reports…” |
| BIRCH large results | PAPER_REPORTED_ONLY | “The paper reports…” |
| Full RW campaign | PAPER_REPORTED_ONLY / NOT_RUN | “not rerun locally” |
| ODM results | PAPER_REPORTED_ONLY / NOT_RUN | “not rerun locally” |

## Claims to avoid

| Bad claim | Why invalid |
|---|---|
| “Nuestra implementación supera a Zebra” | Zebra not run. |
| “Replicamos toda la campaña experimental” | Large/huge families not run. |
| “PopStar fue usado” | Not implemented. |
| “Warm-start acelera siempre” | Local wall-time mixed. |
| “Comparamos monolítico vs Benders” | No monolithic C benchmark. |

## Reproduction commands

```bash
make clean && make
make test
.venv/bin/python scripts/verify_cuts.py
.venv/bin/python tests/test_parse_orlib.py
.venv/bin/python scripts/validate_results.py
.venv/bin/python scripts/run_benchmark.py
.venv/bin/python scripts/compare_paper.py
.venv/bin/python scripts/plot_results.py
```

For clean regeneration, see `docs/EXPERIMENTAL_PROTOCOL.md` before deleting/appending CSVs.
