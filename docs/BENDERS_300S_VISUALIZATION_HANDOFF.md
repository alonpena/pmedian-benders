# Benders 300s visualization handoff

## Phase

FASE 1 — Visualizaciones de campaña Benders 300s.

## Branch and commit at creation

- Branch: `exp/requirements-and-300s-benchmark`
- Base commit before phase: `bf33671`

## Data source

- `results/benders_300s_campaign.csv`
- Rows: 26
- Families: toy = 1, OR-Library = 15, TSPLIB = 10
- Status counts: `OPT_MATCH` = 25, `OPTIMAL_NO_KNOWN` = 1
- Timeout flags: 26 rows with `timeout_flag = 0`

## Script

- `scripts/plot_benders_300s.py`

Implementation note: local Python environment did not have `matplotlib`, `pandas`, or `numpy`. First run failed with `ModuleNotFoundError: No module named 'matplotlib'`. The script was rewritten to use only the Python standard library and a minimal PNG writer. No project solver code was changed.

## Figures generated

All requested figures were generated under `results/figures/`:

1. `results/figures/benders_300s_runtime_by_instance.png`
2. `results/figures/benders_300s_nodes_by_instance.png`
3. `results/figures/benders_300s_lazy_cuts_by_instance.png`
4. `results/figures/benders_300s_runtime_vs_N.png`
5. `results/figures/benders_300s_status_summary.png`

## Columns used

### `benders_300s_runtime_by_instance.png`

- `family`
- `instance`
- `N`
- `p`
- `Ttot`

### `benders_300s_nodes_by_instance.png`

- `family`
- `instance`
- `N`
- `p`
- `nodes`

### `benders_300s_lazy_cuts_by_instance.png`

- `family`
- `instance`
- `N`
- `p`
- `lazy_cuts`

### `benders_300s_runtime_vs_N.png`

- `family`
- `N`
- `Ttot`

### `benders_300s_status_summary.png`

- `status`

## Missing columns

None for requested figures.

## Defensible interpretation

Supported by `results/benders_300s_campaign.csv`:

- The 26-row Benders campaign produced 25 `OPT_MATCH` rows and 1 `OPTIMAL_NO_KNOWN` row.
- No row timed out under the external 300-second wrapper (`timeout_flag = 0` for all rows).
- Runtime, node count, and lazy-cut count vary substantially by instance and p-value.
- The largest observed total wall time in this CSV is 14.191127 seconds for `rl1304_p10`.
- The largest observed B&B node count in this CSV is 329.
- The largest observed lazy-cut count in this CSV is 2285.

## Claims not allowed from these figures alone

Do not claim:

- full replication of the paper;
- superiority over Zebra;
- comparison against a monolithic C baseline;
- behavior on BIRCH, ODM, RW large, or huge TSPLIB;
- machine-independent runtime conclusions;
- causal claims about why a given instance is harder without additional logs or traces;
- per-iteration gap behavior, because this CSV has only aggregate Phase 1/Phase 2 values.

## Reproduction command

```bash
python3 scripts/plot_benders_300s.py
```

## Output verification command

```bash
file results/figures/*.png
```
