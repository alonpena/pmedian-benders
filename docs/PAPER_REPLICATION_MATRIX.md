# Paper replication matrix

Paper: Duran-Mateluna, Ales & Elloumi (2023), *An efficient Benders decomposition for the p-median problem*.

Rule: only local code + CSV/log/test evidence counts as local replication. Zebra/PopStar/paper large campaigns remain paper-only unless local build/run evidence exists.

## Matrix

| paper_component | implemented_local | run_local | evidence_file | status | priority | next_step | notes |
|---|---|---|---|---|---|---|---|
| Benders master (`y_j`, `theta_i`, `sum y=p`) | yes | yes | `src/phase1.c`, `src/phase2.c`, `results/benders_300s_campaign.csv` | VERIFIED_LOCAL | high | keep core frozen unless reproducible bug | verified core |
| Benders optimality cuts | yes | yes | `src/separation.c`, Benders logs with `lazy_cuts` | VERIFIED_LOCAL | high | cite logs | no feasibility cuts needed |
| Algorithm 1 separation | yes | yes | `src/separation.c`, `make test` | VERIFIED_LOCAL | high | cite tests | customer-wise separation implemented |
| Algorithm 2 `ktilde` | yes | yes | `tests/test_separation_toy.c` | VERIFIED_LOCAL | high | cite toy derivation | validated by hand-derived toy test |
| Benders Phase 1 | yes | yes | `results/benders_300s_campaign.csv`, `results/gap_traces/*` on `exp/gap-trace-integration` | VERIFIED_LOCAL | high | use aggregate + trace plots | PopStar not used |
| Benders Phase 2 | yes | yes | logs with `[CALLBACK]`, `lazy_cuts`, `separation_calls` | VERIFIED_LOCAL | high | cite callback proof | Gurobi lazy callback evidence |
| Warm-start by Phase 1 cuts | yes | yes | `src/cutpool.c`, logs with `warm_cuts` | VERIFIED_LOCAL | medium | describe as cut warm-start | not PopStar |
| OR-Library pmed1 | yes | yes | `results/benders_real_instances_300s.csv` on `exp/large-instance-campaign` | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed2 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed3 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed4 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed5 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed6 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed7 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed8 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed9 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed10 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed11 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed12 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed13 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed14 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed15 | yes | yes | same | VERIFIED_LOCAL | high | report row | official optimum matched |
| OR-Library pmed16 | yes | smoke yes | `results/orlib_pmed16_smoke_300s.csv`, `docs/ORLIB_PMED16_SMOKE_HANDOFF.md` | VERIFIED_LOCAL | high | expand to pmed17–pmed20 first | official source downloaded/converted; optimum matched |
| OR-Library pmed17–pmed40 | parser/converter exists for OR-Lib style | no | source audit: official OR-Library files available | READY_TO_RUN | high | download/convert/run bounded campaign | official source available; not yet run |
| TSPLIB kroA100 | yes | yes | `results/benders_real_instances_300s.csv` | PARTIAL_LOCAL | medium | keep as local solved, no known optimum supplied | `OPTIMAL_NO_KNOWN` |
| TSPLIB rl1304 p-grid | yes | yes | `results/benders_real_instances_300s.csv`, `results/benders_300s_campaign.csv` | VERIFIED_LOCAL | high | report p-grid | paper Table 2 subset matched where optima supplied |
| TSPLIB fl1400 | converter likely exists | no | raw local `.tsp`; source audit official `.tsp.gz` available | NEEDS_PREPROCESSING | high | define paper p-grid, convert smoke | local raw file exists |
| TSPLIB u1432 | converter likely exists | no | raw local `.tsp`; source audit official `.tsp.gz` available | NEEDS_PREPROCESSING | high | define paper p-grid, convert smoke | local raw file exists |
| TSPLIB vm1748 | converter likely exists | no | raw local `.tsp`; source audit official `.tsp.gz` available | NEEDS_PREPROCESSING | high | define paper p-grid, convert smoke | local raw file exists |
| TSPLIB d2103 | converter likely exists | no | source audit official `.tsp.gz` available | NEEDS_DOWNLOAD | medium | download only after small/medium success | not local |
| TSPLIB pcb3038 | converter likely exists | no | source audit official `.tsp.gz` available | NEEDS_DOWNLOAD | medium | later candidate | not local |
| TSPLIB fl3795 | converter likely exists | no | source audit official `.tsp.gz` available | NEEDS_DOWNLOAD | medium | memory-check before run | not local |
| TSPLIB rl5934 | converter likely exists | no | source audit official `.tsp.gz` available | TOO_RISKY_TONIGHT | low | document only | likely memory/time risk |
| TSPLIB usa13509 | converter likely exists | no | source audit official `.tsp.gz` available | TOO_RISKY_TONIGHT | low | document only | too large tonight |
| TSPLIB sw24978 | no | no | checked common TSPLIB mirror URLs; not found | NEEDS_DOWNLOAD | low | find source/provenance | source unresolved |
| BIRCH | local generator only | no paper campaign | `scripts/gen_birch.py`; no CSV/log campaign | NOT_RUN | medium | source exact data or run clearly-labeled generated BIRCH-like campaign | paper-scale not replicated |
| RW | local generator + tiny rw12 | only tiny row | `instances/orlib/rw12.pmp`, real campaign row | PARTIAL_LOCAL | medium | run generated RW campaign if labeled synthetic/RW-like | not paper full RW campaign |
| ODM | no | no | no parser/log/data | NOT_IMPLEMENTED | low | requires forbidden-assignment support | too risky |
| Zebra comparison | no | no | web audit: no trustworthy official source found | NOT_AVAILABLE_PUBLICLY | high for claims | keep paper-only wording; seek author code if needed | GitHub repo found is not proven paper Zebra |
| PopStar warm start | no | no | web audit: no trustworthy source found | NOT_IMPLEMENTED | medium | write feasibility only or implement independent heuristic later under new branch | do not claim PopStar |
| F1 formulation comparison | yes | yes | `results/monolithic_f1_300s.csv`, branch `exp/monolithic-baselines` | PARTIAL_LOCAL | medium | report five-row overlap only | F1 baseline implemented, not paper C benchmark |
| F2 formulation comparison | no | no | no code/results | NOT_IMPLEMENTED | low | not tonight | paper formulation only |
| F3 formulation comparison | theoretical/core basis only | no monolithic F3 | docs/source; no monolithic F3 CSV | PARTIAL_LOCAL | low | optional future baseline | Benders derived from F3 |
| F4 formulation/Benders comparison | yes core Benders | yes | core Benders evidence | VERIFIED_LOCAL | high | present as core method | naming depends report convention |
| Constraint reduction | no | no | no implementation | NOT_IMPLEMENTED | medium | future isolated branch | do not claim |
| Reduced-cost fixing | no | no | no implementation | NOT_IMPLEMENTED | medium | future isolated branch | do not claim |
| Synthetic stress test | yes | yes | `results/synthetic_stress_300s.csv`, branch `exp/synthetic-stress` | VERIFIED_LOCAL | medium | use as local stress evidence only | not paper data |
| Gap trace logging | yes | yes | `results/gap_traces/*`, branch `exp/gap-trace-integration` | VERIFIED_LOCAL | medium | use pmed1 trace figures | logging branch only |

## Safe wording

“The project locally verifies the central Benders mechanism and several benchmark subsets. Full paper replication remains incomplete: Zebra, PopStar, reduction techniques, BIRCH/RW-large/ODM, and huge TSPLIB are not locally replicated.”
