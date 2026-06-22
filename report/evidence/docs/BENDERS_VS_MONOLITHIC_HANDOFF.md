# Benders vs Monolithic F1 handoff

## Phase

FASE 4 — Comparación Benders vs Monolithic F1.

## Branch

- `exp/monolithic-baselines`
- Starting commit: `aea894a`

## Inputs

- `results/benders_300s_campaign.csv`
- `results/monolithic_f1_300s.csv`

Only overlapping instances were plotted:

- `toy1`
- `pmed1`
- `pmed2`
- `pmed6`
- `kroA100`

## Script

- `scripts/plot_benders_vs_monolithic.py`

Uses only committed CSV evidence and stdlib PNG helper.

## Figures generated

- `results/figures/benders_vs_monolithic_runtime.png`
- `results/figures/benders_vs_monolithic_gap.png`
- `results/figures/benders_vs_monolithic_nodes.png`

## Comparison table from CSVs

| instance | Benders Ttot | Monolithic runtime | Benders gap column | Monolithic gap | Benders nodes | Monolithic nodes |
|---|---:|---:|---:|---:|---:|---:|
| toy1 | 0.040586 | 0.024817 | 0 | 0.000000 | 1 | 1 |
| pmed1 | 0.035466 | 0.436110 | 0 | 0.000000 | 1 | 1 |
| pmed2 | 0.083832 | 0.441374 | 0.001099 | 0.000000 | 1 | 1 |
| pmed6 | 0.310273 | 6.991906 | 0.005176 | 0.000000 | 7 | 1 |
| kroA100 | 0.067967 | 0.461514 | 0.000295 | 0.000000 | 1 | 1 |

## Metric caveat

The plotted `gap` columns are CSV evidence, but definitions differ:

- Benders campaign `gap` is tied to the Benders run output and Phase 1 lower bound column in that CSV.
- Monolithic F1 `gap` is recorded as solver optimality gap for solved optimal runs and is `0` for all five rows.

Use gap figure as recorded-column comparison, not as a rigorous identical-metric proof unless definitions are normalized later.

## Defensible interpretation

Supported by CSV/log evidence:

- All five overlapping monolithic F1 runs solved with `status=OPTIMAL` and `timeout_flag=0`.
- All five overlapping Benders rows have `timeout_flag=0`; four have known/reference handling in prior Benders CSV and `kroA100` is `OPTIMAL_NO_KNOWN` there.
- For these five local rows, Benders `Ttot` is lower than monolithic F1 `runtime` except `toy1`.
- pmed6 shows the largest local runtime separation in this subset: Benders `0.310273`, monolithic F1 `6.991906`.

## Claims not allowed

Do not claim:

- broad dominance over monolithic models beyond these five rows;
- paper-level monolithic C comparison;
- comparison against F3/F4 monolithic models;
- Zebra comparison;
- machine-independent runtime claims;
- full paper replication.

## Reproduction

```bash
python3 scripts/plot_benders_vs_monolithic.py
```
