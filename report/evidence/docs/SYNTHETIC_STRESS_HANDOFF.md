# Synthetic stress handoff

## Phase

FASE 6 — Synthetic stress test.

## Branch

- `exp/synthetic-stress`
- Base commit: `1de348e`
- Restore-point commit before campaign: `d6241d8`

## Scripts

- `scripts/gen_synthetic_euclidean.py`
- `scripts/run_synthetic_stress_300s.py`
- `scripts/plot_synthetic_stress.py`

## Instance generation

Generated coordinate `.pmp` instances under:

- `instances/synthetic/`

Grid:

- `N = 100, 250, 500, 1000, 2000, 5000`
- `p_pct = 5, 10, 20`
- seed: `20260622`
- p value: `floor(N * p_pct / 100)` with minimum 1
- distance rule: solver coordinate mode computes Euclidean distances rounded down by existing `instance_dist`

Total instances: 18.

## Long-run safeguard

Created `RUNNING_EXPERIMENT.md` before launch because worst-case timeout envelope was 18 × 300s > 30 minutes. Wrapper/scripts and generated instances were committed before campaign.

## Commands run

```bash
python3 scripts/gen_synthetic_euclidean.py
make clean && make && make test
python3 scripts/run_synthetic_stress_300s.py
python3 scripts/plot_synthetic_stress.py
```

Compile/tests passed before campaign. Both core tests printed `RESULT: PASS`.

## Outputs

CSV:

- `results/synthetic_stress_300s.csv`

Logs:

- `results/logs/synthetic_stress_300s/`

Figures:

- `results/figures/synthetic_runtime_vs_N.png`
- `results/figures/synthetic_lazy_cuts_vs_N.png`
- `results/figures/synthetic_nodes_vs_N.png`
- `results/figures/synthetic_timeout_summary.png`

## Results summary

Rows: 18.

| status | count |
|---|---:|
| OPTIMAL_NO_KNOWN | 18 |
| TIMEOUT | 0 |
| ERROR | 0 |
| PARSE_WARNING | 0 |

Timeout flags:

- `timeout_flag=0`: 18
- `timeout_flag=1`: 0

Runtime summary from `Ttot`:

- min: 0.030035 s
- median: 0.643069 s
- max: 44.247668 s (`euclidean_N5000_p5pct`)

Selected rows by N:

| N | p_pct | Ttot | lazy_cuts | nodes |
|---:|---:|---:|---:|---:|
| 100 | 5 | 0.484661 | 93 | 1 |
| 100 | 10 | 0.037117 | 115 | 1 |
| 100 | 20 | 0.030035 | 88 | 1 |
| 500 | 5 | 0.710534 | 721 | 59 |
| 1000 | 5 | 3.151895 | 1385 | 7 |
| 2000 | 10 | 2.442365 | 2494 | 15 |
| 5000 | 5 | 44.247668 | 6874 | 292 |
| 5000 | 10 | 7.70993 | 6049 | 8 |
| 5000 | 20 | 7.055344 | 4870 | 6 |

## Defensible claims

- Synthetic coordinate generator is deterministic for seed `20260622`.
- All 18 synthetic rows completed under external 300-second timeout.
- Largest runtime in this grid is `euclidean_N5000_p5pct` at `44.247668` seconds.
- No synthetic row timed out.

## Claims not allowed

Do not claim:

- results generalize to all Euclidean p-median distributions;
- known optima were externally verified (all rows are `OPTIMAL_NO_KNOWN`);
- paper huge-instance replication;
- Zebra comparison;
- machine-independent runtime conclusions.

## Reproduction

```bash
make clean && make
python3 scripts/gen_synthetic_euclidean.py
python3 scripts/run_synthetic_stress_300s.py
python3 scripts/plot_synthetic_stress.py
```
