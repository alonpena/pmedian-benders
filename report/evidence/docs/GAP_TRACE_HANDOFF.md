# Gap trace integration handoff

## Phase

FASE 2 — Gap trace logging.

## Branch

- `exp/gap-trace-integration`
- Base commit: `1de348e`

## Scope

Integrated non-invasive Phase 1 gap trace logging. No mathematical Benders separation logic was changed. Phase 2 callback logic was not modified.

## Code changes

- `src/logging.h`
  - Declares `GapTrace` and Phase 1 trace functions.
- `src/logging.c`
  - Writes exact trace header:
    `iteration,elapsed_time,LB,UB,gap,cuts_added,total_cuts`
- `src/phase1.h`
  - Adds optional `GapTrace *trace` parameter.
- `src/phase1.c`
  - Logs one row per Phase 1 iteration.
  - Logs after adding cuts and reoptimizing when cuts are added, so `LB` corresponds to the current master after new cuts.
- `src/main.c`
  - Adds CLI option `--gap-trace PATH`.
  - Opens/closes optional trace handle around Phase 1.
- `scripts/run_gap_trace_smoke.py`
  - Runs selected Phase 1 traces with external 300-second timeout per instance.
  - Captures raw logs.
  - Restores `results/benchmark.csv` after runs to avoid contaminating curated benchmark CSV.
- `scripts/plot_gap_trace.py`
  - Generates pmed1 gap/bounds figures using stdlib PNG helper.

## Commands run

```bash
make clean && make && make test
python3 scripts/run_gap_trace_smoke.py
python3 scripts/plot_gap_trace.py
make clean && make && make test
```

## Compile/test result

Passed:

- `make clean && make`
- `make test`

Both core tests printed `RESULT: PASS`.

## Trace outputs

CSV files:

- `results/gap_traces/toy1_p2_phase1.csv`
- `results/gap_traces/pmed1_p5_phase1.csv`
- `results/gap_traces/pmed6_p5_phase1.csv`
- `results/gap_traces/rl1304_p5_phase1.csv`

Raw logs:

- `results/logs/gap_traces/toy1_p2_phase1.log`
- `results/logs/gap_traces/pmed1_p5_phase1.log`
- `results/logs/gap_traces/pmed6_p5_phase1.log`
- `results/logs/gap_traces/rl1304_p5_phase1.log`

## Trace summary

| instance | p | rows | final row |
|---|---:|---:|---|
| toy1 | 2 | 3 | `3,0.011525,6.000000,6.000000,0.000000,0,6` |
| pmed1 | 5 | 6 | `6,0.008005,5819.000000,5819.000000,0.000000,0,337` |
| pmed6 | 5 | 6 | `6,0.025379,7783.500000,7867.000000,0.010614,0,694` |
| rl1304 | 5 | 6 | `6,1.522503,3099073.000000,3099073.000000,0.000000,0,4692` |

Interpretation: these are Phase 1 traces only. `gap` is `(UB-LB)/UB` for current Phase 1 incumbent upper bound and LP master lower bound. A nonzero final Phase 1 gap is not a solver failure; exact solve remains Phase 2 responsibility.

## Figures generated

- `results/figures/gap_vs_iteration_pmed1.png`
- `results/figures/bounds_vs_iteration_pmed1.png`

## Defensible claims

Supported by committed CSV/log/test evidence:

- Optional Phase 1 trace logging works on toy1, pmed1, pmed6, and rl1304 p=5.
- The trace CSV schema matches requested columns exactly.
- pmed1 trace closes Phase 1 gap to zero in 6 iterations in this run.
- rl1304 p=5 trace closes Phase 1 gap to zero in 6 iterations in this run.
- pmed6 Phase 1 stops with no violated cuts and nonzero Phase 1 gap; this is aggregate bound evidence, not exact-optimality evidence.

## Claims not allowed

Do not claim from these traces alone:

- full paper replication;
- Zebra comparison;
- monolithic baseline comparison;
- Phase 2 gap trajectory;
- branch-and-bound callback gap trajectory;
- machine-independent runtime conclusions;
- optimality for pmed6 from Phase 1 alone.

## Reproduction

```bash
make clean && make
python3 scripts/run_gap_trace_smoke.py
python3 scripts/plot_gap_trace.py
```
