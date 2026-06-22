# Benders 300s campaign
## 1. Purpose
Run the existing Benders implementation under the report's 5-minute protocol using an external Python timeout. The mathematical Benders core was not modified.
## 2. Exact commands
```bash
make
./scripts/run_benchmark_300s.py --campaign smoke --time-limit 300 --overwrite
./scripts/run_benchmark_300s.py --campaign full --time-limit 300 --overwrite
```
The wrapper calls `subprocess.run(..., timeout=300)` and runs `./pmedian` from a temporary working directory, so repository `results/benchmark.csv` is not appended by these runs.
## 3. Instance list
- `toy1`
- OR-Library `pmed1`–`pmed15`
- TSPLIB `kroA100`
- TSPLIB `rl1304` with `p = 5, 10, 20, 50, 100, 200, 300, 400, 500` using available `.pmp` files
## 4. Summary counts
| Status | Count |
|---|---:|
| OPT_MATCH | 25 |
| OPTIMAL_NO_KNOWN | 1 |
| TIMEOUT | 0 |
| ERROR | 0 |
| PARSE_WARNING | 0 |

Timeout flags: `0` = 26, `1` = 0.
## 5. Table of results
| family | instance | N | p | status | obj | LB1 | UB1 | gap | Ttot | iterations | nodes | lazy_cuts | separation_calls | matches_known_opt | delta_opt | log_path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| toy | toy1 | 4 | 2 | OPT_MATCH | 6 | 6 | 6 | 0 | 0.040586 | 3 | 1 | 2 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_toy_toy1_p2.log |
| OR-Library | pmed1 | 100 | 5 | OPT_MATCH | 5819 | 5819 | 5819 | 0 | 0.035466 | 6 | 1 | 90 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed1_p5.log |
| OR-Library | pmed2 | 100 | 10 | OPT_MATCH | 4093 | 4088.5 | 4116 | 0.001099 | 0.083832 | 6 | 1 | 136 | 13 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed2_p10.log |
| OR-Library | pmed3 | 100 | 10 | OPT_MATCH | 4250 | 4240.5 | 4250 | 0.002235 | 0.082504 | 6 | 3 | 134 | 10 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed3_p10.log |
| OR-Library | pmed4 | 100 | 20 | OPT_MATCH | 3034 | 3034 | 3034 | 0 | 0.026538 | 5 | 1 | 56 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed4_p20.log |
| OR-Library | pmed5 | 100 | 33 | OPT_MATCH | 1355 | 1355 | 1355 | 0 | 0.02894 | 5 | 1 | 44 | 5 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed5_p33.log |
| OR-Library | pmed6 | 200 | 5 | OPT_MATCH | 7824 | 7783.5 | 7867 | 0.005176 | 0.310273 | 6 | 7 | 240 | 16 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed6_p5.log |
| OR-Library | pmed7 | 200 | 10 | OPT_MATCH | 5631 | 5631 | 5631 | 0 | 0.114798 | 6 | 1 | 144 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed7_p10.log |
| OR-Library | pmed8 | 200 | 20 | OPT_MATCH | 4445 | 4445 | 4445 | 0 | 0.045486 | 5 | 1 | 168 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed8_p20.log |
| OR-Library | pmed9 | 200 | 40 | OPT_MATCH | 2734 | 2734 | 2734 | 0 | 0.038114 | 6 | 1 | 132 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed9_p40.log |
| OR-Library | pmed10 | 200 | 67 | OPT_MATCH | 1255 | 1255 | 1255 | 0 | 0.040525 | 9 | 1 | 85 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed10_p67.log |
| OR-Library | pmed11 | 300 | 5 | OPT_MATCH | 7696 | 7693.3333 | 7696 | 0.000347 | 0.388687 | 9 | 1 | 308 | 12 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed11_p5.log |
| OR-Library | pmed12 | 300 | 10 | OPT_MATCH | 6634 | 6625.75 | 6638 | 0.001244 | 0.328951 | 7 | 7 | 204 | 11 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed12_p10.log |
| OR-Library | pmed13 | 300 | 30 | OPT_MATCH | 4374 | 4374 | 4374 | 0 | 0.072906 | 5 | 1 | 213 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed13_p30.log |
| OR-Library | pmed14 | 300 | 60 | OPT_MATCH | 2968 | 2967.2 | 2971 | 0.00027 | 0.086312 | 8 | 1 | 238 | 7 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed14_p60.log |
| OR-Library | pmed15 | 300 | 100 | OPT_MATCH | 1729 | 1729 | 1729 | 0 | 0.063793 | 7 | 1 | 140 | 4 | YES | 0 | results/logs/benders_300s/full_20260622_033304_OR-Library_pmed15_p100.log |
| TSPLIB | kroA100 | 100 | 10 | OPTIMAL_NO_KNOWN | 30539 | 30530 | 30545 | 0.000295 | 0.067967 | 8 | 1 | 162 | 12 | NA | NA | results/logs/benders_300s/full_20260622_033304_TSPLIB_kroA100_p10.log |
| TSPLIB | rl1304_p5 | 1304 | 5 | OPT_MATCH | 3099073 | 3099073 | 3099073 | 0 | 4.468375 | 6 | 1 | 1850 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p5_p5.log |
| TSPLIB | rl1304_p10 | 1304 | 10 | OPT_MATCH | 2134295 | 2131788 | 2243679 | 0.001175 | 14.191127 | 8 | 329 | 2285 | 21 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p10_p10.log |
| TSPLIB | rl1304_p20 | 1304 | 20 | OPT_MATCH | 1412108 | 1412108 | 1412108 | 0 | 2.101193 | 7 | 1 | 1845 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p20_p20.log |
| TSPLIB | rl1304_p50 | 1304 | 50 | OPT_MATCH | 795012 | 795012 | 795012 | 0 | 1.318409 | 7 | 1 | 1714 | 3 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p50_p50.log |
| TSPLIB | rl1304_p100 | 1304 | 100 | OPT_MATCH | 491639 | 491506.5 | 496403 | 0.00027 | 1.663946 | 8 | 157 | 1628 | 16 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p100_p100.log |
| TSPLIB | rl1304_p200 | 1304 | 200 | OPT_MATCH | 268573 | 268573 | 268573 | 0 | 0.582194 | 8 | 1 | 1387 | 5 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p200_p200.log |
| TSPLIB | rl1304_p300 | 1304 | 300 | OPT_MATCH | 177326 | 177318 | 179952 | 0.000045 | 0.497276 | 7 | 1 | 1192 | 7 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p300_p300.log |
| TSPLIB | rl1304_p400 | 1304 | 400 | OPT_MATCH | 128332 | 128332 | 128332 | 0 | 0.496503 | 9 | 1 | 953 | 11 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p400_p400.log |
| TSPLIB | rl1304_p500 | 1304 | 500 | OPT_MATCH | 97024 | 97018 | 97034 | 0.000062 | 0.455383 | 13 | 1 | 838 | 9 | YES | 0 | results/logs/benders_300s/full_20260622_033304_TSPLIB_rl1304_p500_p500.log |

## 6. Known/paper optimum matches
- `toy1`: matched known toy optimum.
- OR-Library `pmed1`–`pmed15`: matched `instances/orlib/pmedopt.txt`.
- TSPLIB `rl1304` all nine p-values: matched paper Table 2 optima transcribed in the wrapper.
- `kroA100`: solved locally, but wrapper did not use a trusted known optimum, so status is `OPTIMAL_NO_KNOWN`.

## 7. Logs proving lazy callbacks
All 26 final campaign logs are referenced by `log_path` in `results/benders_300s_campaign.csv`. Each final row has parsed `lazy_cuts` and `separation_calls`; minimum parsed `lazy_cuts` is 2 and minimum parsed `separation_calls` is 3. Logs contain the `[CALLBACK]` line emitted by the solver.

## 8. Unavailable fields
- `matches_known_opt` and `delta_opt` are `NA` for `kroA100` because no trusted known optimum was supplied to the wrapper.
- Per-iteration gap traces are not included in this campaign; gap logging integration remains parked in `docs/dev_wip/gap_logging_wip.patch`.

## 9. Limitations
- No Zebra execution; no claim of outperforming Zebra.
- No monolithic C baseline.
- No PopStar, reduced-cost fixing, or constraint reduction.
- No BIRCH, RW large, ODM, or huge TSPLIB campaign.
- Runtime includes wrapper-level process startup and Gurobi license initialization; compare only as local evidence, not machine-independent paper timing.

## 10. Next recommended experiments
1. Add non-invasive per-iteration gap trace integration from parked WIP.
2. Create monolithic F1 baseline on separate branch.
3. Extend TSPLIB preprocessing for `fl1400`, `u1432`, and `vm1748` with explicit p-grid.
4. Generate plots from `results/benders_300s_campaign.csv`.
