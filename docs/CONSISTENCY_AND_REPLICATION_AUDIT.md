# Consistency and replication audit

Fecha: 2026-06-19. Auditoría de consistencia para defensa final.

Status allowed: `VERIFIED_LOCAL`, `PARTIAL_LOCAL`, `PAPER_REPORTED_ONLY`, `NOT_IMPLEMENTED`, `NOT_RUN`, `UNSUPPORTED_CLAIM`.

## Resumen ejecutivo

Este repositorio soporta una tesis honesta:

> Replicación algorítmica completa del mecanismo central del paper + replicación computacional parcial documentada.

No soporta una tesis de “nuestra implementación supera a Zebra” ni de “reproducimos toda la campaña computacional del paper”.

Required Zebra wording:

> The paper reports that this method outperforms Zebra; this project does not rerun Zebra. Therefore, the comparison with Zebra is treated as a literature claim, not as a local experimental result.

## 1. What has actually been implemented?

| Item | Evidence | Status |
|---|---|---|
| F3-derived Benders master with `y_j`, `theta_i`, `sum y=p` | `src/phase1.c`, `src/phase2.c` | VERIFIED_LOCAL |
| Primal/dual subproblem derivation and optimality cuts | `report/sections/05_benders.tex`, `src/separation.c` | VERIFIED_LOCAL |
| Algorithm 1 separation over clients | `src/separation.c::separation_all` | VERIFIED_LOCAL |
| Algorithm 2 `ktilde` computation | `src/separation.c::separation_k_tilde` | VERIFIED_LOCAL |
| Closed-form separation, no LP subproblem solves | `src/separation.c`, tests/logs | VERIFIED_LOCAL |
| Phase 1 LP relaxation with cut loop | `src/phase1.c` | VERIFIED_LOCAL |
| Phase 2 branch-and-Benders-cut lazy callback | `src/phase2.c`, `results/logs/*full.log` | VERIFIED_LOCAL |
| Warm-start by loading Phase 1 cuts into Phase 2 | `src/cutpool.c`, `src/phase1.c`, `src/phase2.c` | VERIFIED_LOCAL |
| Rounding heuristic | `src/heuristic.c` | VERIFIED_LOCAL |
| OR-Library parser with last-edge-wins rule | `scripts/parse_orlib.py`, `docs/ADR/0002-orlib-duplicate-edges.md` | VERIFIED_LOCAL |
| TSPLIB parser with floored Euclidean distances | `scripts/parse_tsplib.py`, `results/comparison_vs_paper.csv` | VERIFIED_LOCAL |
| RW/BIRCH generators | `scripts/gen_rw.py`, `scripts/gen_birch.py` | PARTIAL_LOCAL |
| Zebra | no source/script/log | NOT_IMPLEMENTED |
| PopStar | no source/script/log; replaced by rounding | NOT_IMPLEMENTED |
| Reduced-cost fixing | no source/script/log | NOT_IMPLEMENTED |
| Constraint reduction | no source/script/log | NOT_IMPLEMENTED |
| CPLEX/SCIP backend | no source compiled | NOT_IMPLEMENTED |

## 2. What has actually been run?

| Run family | Evidence | Status |
|---|---|---|
| `toy1` | `make test`, `tests/test_core.c`, `tests/test_separation_toy.c` | VERIFIED_LOCAL |
| OR-Library `pmed1`–`pmed15` | `results/orlib_optima_check.csv`, `results/benchmark.csv`, `results/logs/pmed*.log` | VERIFIED_LOCAL |
| TSPLIB `rl1304`, 9 p-values from paper Table 2 | `results/comparison_vs_paper.csv`, `results/logs/rl1304*.log` | VERIFIED_LOCAL |
| TSPLIB `kroA100` | `results/benchmark.csv`, `results/logs/kroA100.pmp_p10_full.log` | VERIFIED_LOCAL |
| RW small/asymmetric `rw12` | `instances/orlib/rw12.pmp`, DEVLOG/test cross-check | PARTIAL_LOCAL |
| Warm vs cold start on `pmed1,pmed6,pmed11` | `results/warmstart_comparison.csv` | VERIFIED_LOCAL |
| Large/huge TSP, BIRCH, RW large, ODM | no CSV/log | NOT_RUN |
| Zebra | no executable/log/result | NOT_RUN |

## 3. What has actually been verified?

| Claim | Evidence | Status |
|---|---|---|
| Separator matches hand-derived cuts on `toy1` | `tests/test_separation_toy.c`, `make test` | VERIFIED_LOCAL |
| Separator C matches Python oracle, 0 diffs | `scripts/verify_cuts.py`, `results/logs/verify_cuts_oracle_diff.log` | VERIFIED_LOCAL |
| Branch-and-Benders-cut is real (`lazy_cuts>0`) | `results/logs/*full.log` | VERIFIED_LOCAL |
| OR-Library 15/15 official optima | `results/orlib_optima_check.csv` | VERIFIED_LOCAL |
| `rl1304` 9/9 paper optima | `results/comparison_vs_paper.csv` | VERIFIED_LOCAL |
| Warm-start reduces B&B nodes/lazy cuts in tested cases | `results/warmstart_comparison.csv` | VERIFIED_LOCAL |
| Warm-start improves wall-time generally | local times mixed; no large tests | UNSUPPORTED_CLAIM |
| `O(NM)` asymptotic separation at huge scale | code structure supports; no huge timing | PARTIAL_LOCAL |

## 4. What has merely been described from the paper?

| Paper-described item | Local status |
|---|---|
| Zebra comparison / order-of-magnitude speedup | PAPER_REPORTED_ONLY |
| Zebra memory failures | PAPER_REPORTED_ONLY |
| First optimal solves for huge TSP/BIRCH | PAPER_REPORTED_ONLY |
| PopStar effect in paper | PAPER_REPORTED_ONLY locally; PopStar NOT_IMPLEMENTED |
| Reduced-cost fixing / constraint reduction effects | PAPER_REPORTED_ONLY locally; NOT_IMPLEMENTED |
| Full Tables 3–9 campaign | PAPER_REPORTED_ONLY / NOT_RUN |
| CPLEX timings from paper | PAPER_REPORTED_ONLY; local solver is Gurobi |

## 5. What is claimed in report/slides but not supported by repo evidence?

After patching, no final report/slide sentence should imply local Zebra superiority or full campaign replication.

| Claim pattern | Finding | Status | Fix |
|---|---|---|---|
| “our implementation beats Zebra” | Not present after patch | n/a | Wording says paper-reported only |
| “full paper campaign reproduced” | Not present after patch | n/a | Wording says computational subset |
| “large TSP/BIRCH/RW/ODM run locally” | Not present after patch | n/a | Listed as not run |
| “PopStar implemented” | Not present after patch | n/a | Listed as not implemented |
| “wall-time warm-start always better” | Not present after patch | n/a | Report says mixed wall-time |
| Any raw table number without source | See `docs/NUMERICAL_CLAIMS_TRACE.md` | VERIFIED_LOCAL | Sources listed |

## 6. Is Zebra implemented or run locally?

No.

Evidence:
- No `src/` implementation.
- No benchmark script invoking Zebra.
- No `results/` CSV/log from Zebra.
- `rg Zebra src scripts results` finds only comments/docs or no implementation.

Status: `NOT_IMPLEMENTED`, `NOT_RUN`.

Defense wording: Zebra comparison is `PAPER_REPORTED_ONLY`.

## 7. Are PopStar, reduced-cost fixing, and constraint reduction implemented?

No.

| Component | Evidence | Status |
|---|---|---|
| PopStar | `src/heuristic.h` says rounding replaces PopStar | NOT_IMPLEMENTED |
| reduced-cost fixing | no code path in `src/`; docs only | NOT_IMPLEMENTED |
| constraint reduction | no code path in `src/`; docs only | NOT_IMPLEMENTED |

## 8. Are large TSP, BIRCH, RW, ODM experiments run locally?

No, except tiny RW sanity check.

| Family | Local evidence | Status |
|---|---|---|
| Large/huge TSP | no CSV/log beyond `rl1304` and `kroA100`; raw `fl1400/u1432/vm1748` files are not results | NOT_RUN |
| BIRCH | generator exists; no generated instances/results | NOT_RUN |
| RW large | only `rw12` toy-like validation | PARTIAL_LOCAL |
| ODM | no parser/instances/results | NOT_IMPLEMENTED / NOT_RUN |

## 9. Are OR-Library and `rl1304` results actually present in CSV/logs?

Yes.

| Evidence | Contents | Status |
|---|---|---|
| `results/orlib_optima_check.csv` | 15 rows `pmed1`–`pmed15`, all `OPT_MATCH`, delta 0 | VERIFIED_LOCAL |
| `results/benchmark.csv` | OR-Library rows, `rl1304` subset rows, `kroA100` row | VERIFIED_LOCAL |
| `results/comparison_vs_paper.csv` | 9 `rl1304` p-values, all `delta_OPT=0` | VERIFIED_LOCAL |
| `results/logs/pmed*.log` | callback proof for OR-Library | VERIFIED_LOCAL |
| `results/logs/rl1304*.log` | callback proof for `rl1304` | VERIFIED_LOCAL |

## 10. Are all numerical claims in report/slides traceable to `results/` files?

Yes for empirical result claims after patching. Trace file: `docs/NUMERICAL_CLAIMS_TRACE.md`.

Caveat: mathematical exposition numbers (equation indices, dimensions like `N*M`, citation years, page/section references) are not experimental claims. Empirical values in tables/slides are traced to `results/*.csv`, `results/logs/*.log`, tests, or documented OR-Library/Paper sources.

## Final audit verdict

| Area | Verdict |
|---|---|
| Algorithmic replication | VERIFIED_LOCAL |
| Computational replication subset | VERIFIED_LOCAL / PARTIAL_LOCAL |
| Zebra comparison | PAPER_REPORTED_ONLY; NOT_RUN locally |
| Full paper campaign | NOT_RUN |
| Report/slides honesty | VERIFIED_LOCAL after patches |
| Readiness | READY_WITH_RISKS |

Primary remaining risk: professor asks for full computational campaign or Zebra rerun. Correct answer: out of local scope; paper claim only; project contribution is replicated mechanism plus documented subset.
