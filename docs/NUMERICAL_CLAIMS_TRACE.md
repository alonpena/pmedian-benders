# Numerical claims trace

Scope: empirical/numerical claims in `report/` and `slides/`. Formula indices, citation years, LaTeX layout numbers, and symbolic dimensions (`N`, `M`, `p`) are not treated as experimental claims unless used as measured data.

Status values: `VERIFIED`, `NOT FOUND`.

## Report claims

| Claim text | File | Value(s) | Source CSV/log/file | Status |
|---|---|---:|---|---|
| Separador verificado por oráculo Python con 0 diferencias | `report/main.tex`, `report/sections/06_separacion.tex`, `report/sections/11_reproducibilidad.tex` | 0 diffs | `results/logs/verify_cuts_oracle_diff.log`; `scripts/verify_cuts.py` | VERIFIED |
| OR-Library alcanza óptimo oficial con brecha 0% | `report/main.tex`, `report/sections/09_experimentos.tex`, `report/sections/10_resultados.tex` | 15/15, delta=0 | `results/orlib_optima_check.csv` | VERIFIED |
| `rl1304` reproduce óptimos del paper | `report/main.tex`, `report/sections/09_experimentos.tex`, `report/sections/10_resultados.tex` | 9/9, delta=0, p<=500 | `results/comparison_vs_paper.csv` | VERIFIED |
| Escala local máxima probada | `report/sections/01_motivacion.tex`, `08_instancias.tex`, `10_resultados.tex` | N=1304 | `results/benchmark.csv`; `results/comparison_vs_paper.csv` | VERIFIED |
| `toy1` caso base | `report/sections/02_definicion.tex`, `08_instancias.tex` | N=M=4, p=2, opt=6 | `tests/test_core.c`; `make test`; `instances/toy/toy1.pmp` | VERIFIED |
| Distancias `toy1` | `report/sections/02_definicion.tex` | d01=3, d02=4, d03=5, d12=5, d13=4, d23=3 | `instances/toy/toy1.pmp`; `tests/test_core.c` | VERIFIED |
| OR-Library family local range | `report/sections/08_instancias.tex`, `09_experimentos.tex` | pmed1–15; N=100/200/300; p=5..100 | `instances/orlib/*.pmp`; `results/orlib_optima_check.csv` | VERIFIED |
| TSPLIB local subset | `report/sections/08_instancias.tex` | `rl1304`, `kroA100`; p={5,10,20,50,100,200,300,400,500} for comparison | `instances/tsplib/*.pmp`; `results/comparison_vs_paper.csv`; `results/benchmark.csv` | VERIFIED |
| `rl1304` floored distance validates paper optimum | `report/sections/08_instancias.tex` | p=5, opt=3,099,073 | `results/comparison_vs_paper.csv` | VERIFIED |
| OR-Library duplicate-edge wrong-min vs official | `report/sections/08_instancias.tex` | min rule 5718; last-wins 5819 | `docs/ADR/0002-orlib-duplicate-edges.md`; `docs/orlib_pmed_format_spec.txt`; `instances/orlib/pmedopt.txt` | VERIFIED |
| OR-Library table values | `report/sections/09_experimentos.tex`, Table `tab:orlib` | pmed1–15 LB1/UB1/opt/official/iter/nodes | `results/orlib_optima_check.csv`; `results/benchmark.csv` | VERIFIED |
| OR-Library total runtime claim | `report/sections/09_experimentos.tex` | all OR-Library Ttot < 0.36 s | `results/benchmark.csv` (max OR-Library Ttot 0.359 s) | VERIFIED |
| OR-Library branching exceptions | `report/sections/09_experimentos.tex` | pmed3 nodes=3, pmed6 nodes=7, pmed12 nodes=7 | `results/orlib_optima_check.csv`; `results/benchmark.csv` | VERIFIED |
| `rl1304` comparison table values | `report/sections/09_experimentos.tex`, Table `tab:paper` | all 9 rows: paper/our OPT, LB1, UB1 | `results/comparison_vs_paper.csv`; `scripts/compare_paper.py` | VERIFIED |
| `rl1304` paper-vs-local machine note | `report/sections/09_experimentos.tex` | paper XEON W-2145/CPLEX 20.1; local M1/Gurobi 12 | `scripts/compare_paper.py`; `DEVLOG.md`; `docs/AUDIT.md` | VERIFIED |
| Warm-start table values | `report/sections/09_experimentos.tex`, Table `tab:warm` | pmed1 223→1 nodes, 513→90 cuts, 0.047→0.016 s; pmed6 632→7, 1053→240, 0.143→0.600; pmed11 352→1, 1768→308, 0.030→0.940 | `results/warmstart_comparison.csv` | VERIFIED |
| Warm-start preload cuts | `report/sections/09_experimentos.tex` | 337/694/1285 warm cuts | `results/warmstart_comparison.csv` | VERIFIED |
| Callback proof pmed1 | `report/sections/09_experimentos.tex` | separation_calls=3, lazy_cuts=90, bb_nodes=1 | `results/logs/pmed1.pmp_p5_full.log` | VERIFIED |
| Callback proof rl1304 p=5 | `report/sections/09_experimentos.tex` | lazy_cuts=1850 | `results/logs/rl1304_p5.pmp_p5_full.log` | VERIFIED |
| `UB1` worse without PopStar example | `report/sections/10_resultados.tex` | our 2243679 vs paper 2134295 for rl1304 p=10; p in {10,100,300} affected | `results/comparison_vs_paper.csv` | VERIFIED |
| Local limitations | `report/sections/08_instancias.tex`, `10_resultados.tex` | no BIRCH/ODM/RW large/TSP >10^4/Zebra | absence in `results/`; `docs/CONSISTENCY_AND_REPLICATION_AUDIT.md` | VERIFIED |
| Solver and exactness settings | `report/sections/07_implementacion.tex`, `09_experimentos.tex`, `11_reproducibilidad.tex` | Gurobi 12.0.0; MIPGap=1e-10; Apple M1 | `src/phase2.c`; `docs/AUDIT.md`; `DEVLOG.md` | VERIFIED |
| Figures use real data | `report/sections/09_experimentos.tex` | 4 figures | `results/plot_a_bounds_orlib.png`; `results/plot_b_time_vs_N.png`; `results/plot_c_gap_vs_pM.png`; `results/plot_d_iter_nodes_vs_p.png`; `scripts/plot_results.py` | VERIFIED |

## Slide claims

| Claim text | File | Value(s) | Source CSV/log/file | Status |
|---|---|---:|---|---|
| Presentation length/slide count | `slides/main.tex`, `slides/speaker_notes.md` | 8 slides, ~15 min | `slides/main.tex` frame count; speaker plan | VERIFIED |
| F1 scale example | `slides/main.tex`, `slides/speaker_notes.md` | N=M=10^4 gives ~10^8 variables | formula `N*M`; `report/sections/03_formulaciones.tex` | VERIFIED |
| Separator verification | `slides/main.tex`, `slides/speaker_notes.md` | 3 ways; 0 differences | `make test`; `results/logs/verify_cuts_oracle_diff.log` | VERIFIED |
| OR-Library result | `slides/main.tex`, `slides/speaker_notes.md` | 15/15, delta=0 | `results/orlib_optima_check.csv` | VERIFIED |
| `rl1304` result | `slides/main.tex`, `slides/speaker_notes.md` | N=1304, p<=500, 9/9 paper optima | `results/comparison_vs_paper.csv` | VERIFIED |
| Callback proof in slides | `slides/main.tex` | pmed1 lazy_cuts=90, nodes=1; rl1304 p5 lazy_cuts=1850 | `results/logs/pmed1.pmp_p5_full.log`; `results/logs/rl1304_p5.pmp_p5_full.log` | VERIFIED |
| Warm-start nodes table | `slides/main.tex`, `slides/speaker_notes.md` | pmed1 223→1; pmed6 632→7; pmed11 352→1 | `results/warmstart_comparison.csv` | VERIFIED |
| Scale limitation in slides | `slides/main.tex`, `slides/speaker_notes.md` | local max N=1304; TSP >10^4/BIRCH/ODM/RW large/Zebra not rerun | `results/`; `docs/CONSISTENCY_AND_REPLICATION_AUDIT.md` | VERIFIED |

## Paper-only numbers intentionally not local claims

| Claim text | File | Value(s) | Source | Status |
|---|---|---:|---|---|
| Paper reports Zebra speedup/order of magnitude | `report/sections/01_motivacion.tex`, `02b_literatura.tex`; `docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md` | order of magnitude | Paper, not local | VERIFIED as PAPER_REPORTED_ONLY |
| Paper reports huge TSP/BIRCH sizes | `docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md` | TSP 238,025; BIRCH 89,600; etc. | Paper summary/brief | VERIFIED as PAPER_REPORTED_ONLY |

## NOT FOUND items

None after final patch. If a new number is added to report/slides, add row here or remove/qualify the number.
