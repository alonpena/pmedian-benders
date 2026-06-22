# Report tables

## 1. Benders 300s summary

| metric | value |
|---|---:|
| CSV | `report/evidence/csv/benders_300s_campaign.csv` |
| Rows | 26 |
| OPT_MATCH | 25 |
| OPTIMAL_NO_KNOWN | 1 |
| TIMEOUT | 0 |
| timeout_flag=0 | 26 |
| Max Ttot | 14.191127 s (`rl1304_p10`) |
| Max nodes | 329 (`rl1304_p10`) |
| Max lazy cuts | 2285 (`rl1304_p10`) |

## 2. Benders 300s by family

| family | rows | evidence |
|---|---:|---|
| toy | 1 | `toy1`, OPT_MATCH |
| OR-Library | 15 | `pmed1`–`pmed15`, all OPT_MATCH |
| TSPLIB | 10 | `kroA100` + `rl1304` p-grid; `kroA100` OPTIMAL_NO_KNOWN |

## 3. OR-Library status

| group | local status | rows/run | evidence | note |
|---|---|---:|---|---|
| pmed1–pmed15 | verified local | 15 | `report/evidence/csv/benders_300s_campaign.csv`, `report/evidence/csv/benders_real_instances_300s.csv` | official optima matched |
| pmed16 | smoke verified local | 1 | `report/evidence/csv/orlib_pmed16_smoke_300s.csv` | obj 8162, OPT_MATCH, 0.793458 s |
| pmed17–pmed40 | ready to run | 0 | `report/evidence/docs/WEB_SOURCE_AND_REPLICATION_FEASIBILITY_AUDIT.md` | official source available; no run yet |

## 4. Monolithic F1 summary

| instance | N | p | status | obj | gap | runtime | nodes | vars | cons | timeout |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| toy1 | 4 | 2 | OPTIMAL | 6 | 0 | 0.024817 | 1 | 20 | 21 | 0 |
| pmed1 | 100 | 5 | OPTIMAL | 5819 | 0 | 0.436110 | 1 | 10100 | 10101 | 0 |
| pmed2 | 100 | 10 | OPTIMAL | 4093 | 0 | 0.441374 | 1 | 10100 | 10101 | 0 |
| pmed6 | 200 | 5 | OPTIMAL | 7824 | 0 | 6.991906 | 1 | 40200 | 40201 | 0 |
| kroA100 | 100 | 10 | OPTIMAL | 30539 | 0 | 0.461514 | 1 | 10100 | 10101 | 0 |

## 5. Benders vs Monolithic F1 overlap

| instance | Benders Ttot | Monolithic runtime | Benders gap column | Monolithic gap | Benders nodes | Monolithic nodes |
|---|---:|---:|---:|---:|---:|---:|
| toy1 | 0.040586 | 0.024817 | 0 | 0.000000 | 1 | 1 |
| pmed1 | 0.035466 | 0.436110 | 0 | 0.000000 | 1 | 1 |
| pmed2 | 0.083832 | 0.441374 | 0.001099 | 0.000000 | 1 | 1 |
| pmed6 | 0.310273 | 6.991906 | 0.005176 | 0.000000 | 7 | 1 |
| kroA100 | 0.067967 | 0.461514 | 0.000295 | 0.000000 | 1 | 1 |

## 6. Gap trace summary

| instance | p | trace rows | final gap | evidence |
|---|---:|---:|---:|---|
| toy1 | 2 | 3 | 0 | `report/evidence/csv/gap_traces/toy1_p2_phase1.csv` |
| pmed1 | 5 | 6 | 0 | `report/evidence/csv/gap_traces/pmed1_p5_phase1.csv` |
| pmed6 | 5 | 6 | 0.010614 | `report/evidence/csv/gap_traces/pmed6_p5_phase1.csv` |
| rl1304 | 5 | 6 | 0 | `report/evidence/csv/gap_traces/rl1304_p5_phase1.csv` |

## 7. Real READY campaign summary

| metric | value |
|---|---:|
| CSV | `report/evidence/csv/benders_real_instances_300s.csv` |
| Rows | 26 |
| OR-Library rows | 15 |
| TSPLIB rows | 10 |
| RW rows | 1 |
| OPT_MATCH | 24 |
| OPTIMAL_NO_KNOWN | 2 |
| TIMEOUT | 0 |
| Max Ttot | 14.217998 s (`rl1304_p10`) |

## 8. Synthetic stress summary

| N | p_pct=5 Ttot/nodes/cuts | p_pct=10 Ttot/nodes/cuts | p_pct=20 Ttot/nodes/cuts |
|---:|---|---|---|
| 100 | 0.484661 / 1 / 93 | 0.037117 / 1 / 115 | 0.030035 / 1 / 88 |
| 250 | 0.092570 / 1 / 416 | 0.063482 / 1 / 279 | 0.057613 / 1 / 231 |
| 500 | 0.710534 / 59 / 721 | 0.141580 / 1 / 649 | 0.330849 / 1 / 516 |
| 1000 | 3.151895 / 7 / 1385 | 0.591020 / 1 / 1226 | 0.695118 / 3 / 1008 |
| 2000 | 3.043141 / 1 / 2725 | 2.442365 / 15 / 2494 | 1.649372 / 1 / 2023 |
| 5000 | 44.247668 / 292 / 6874 | 7.709930 / 8 / 6049 | 7.055344 / 6 / 4870 |

All 18 synthetic rows: `OPTIMAL_NO_KNOWN`, `timeout_flag=0`.

## 9. Paper replication matrix summary

| component | status | evidence |
|---|---|---|
| Benders master/cuts/separation | VERIFIED_LOCAL | `src/phase1.c`, `src/phase2.c`, `src/separation.c`, logs |
| Phase 1 / Phase 2 | VERIFIED_LOCAL | Benders CSV/logs, gap traces |
| OR-Library pmed1–pmed15 | VERIFIED_LOCAL | campaign CSVs |
| OR-Library pmed16 | VERIFIED_LOCAL smoke | pmed16 smoke CSV/log |
| OR-Library pmed17–pmed40 | READY_TO_RUN | official source audit, no run |
| TSPLIB rl1304 | VERIFIED_LOCAL | Benders CSV |
| TSPLIB kroA100 | PARTIAL_LOCAL | local solve, no known optimum supplied |
| Monolithic F1 | PARTIAL_LOCAL | five-row baseline |
| PopStar | NOT_IMPLEMENTED | audits |
| Zebra | NOT_AVAILABLE_PUBLICLY / PAPER_ONLY | source audit |
| Constraint reduction | NOT_IMPLEMENTED | audits |
| Reduced-cost fixing | NOT_IMPLEMENTED | audits |
| BIRCH/RW-large/ODM | NOT_RUN / NOT_IMPLEMENTED | audits |
| Synthetic stress | VERIFIED_LOCAL | synthetic CSV/logs |
