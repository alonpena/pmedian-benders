# Overnight traceability audit

## Scope

Checked CSV rows, status counts, max runtime rows, and row-to-log traceability via committed git objects.

## CSV counts

| artifact | branch | rows | statuses |
|---|---|---:|---|
| `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | 26 | `OPT_MATCH=25`, `OPTIMAL_NO_KNOWN=1` |
| `results/monolithic_f1_300s.csv` | `exp/monolithic-baselines` | 5 | `OPTIMAL=5` |
| `results/benders_real_instances_300s.csv` | `exp/large-instance-campaign` | 26 | `OPT_MATCH=24`, `OPTIMAL_NO_KNOWN=2` |
| `results/synthetic_stress_300s.csv` | `exp/synthetic-stress` | 18 | `OPTIMAL_NO_KNOWN=18` |

## Row-to-log traceability

| CSV | rows with `log_path` | missing log files |
|---|---:|---:|
| Benders 300s | 26 | 0 |
| Monolithic F1 300s | 5 | 0 |
| Real instances 300s | 26 | 0 |
| Synthetic stress 300s | 18 | 0 |

## Gap traces

Branch: `exp/gap-trace-integration`, commit `11db33b`.

| trace file | rows | final row summary |
|---|---:|---|
| `results/gap_traces/toy1_p2_phase1.csv` | 3 | final gap 0 |
| `results/gap_traces/pmed1_p5_phase1.csv` | 6 | final gap 0 |
| `results/gap_traces/pmed6_p5_phase1.csv` | 6 | final gap 0.010614 |
| `results/gap_traces/rl1304_p5_phase1.csv` | 6 | final gap 0 |

## Current branch caveat

The final handoff branch does not physically contain all CSV/log/figure artifacts from all experimental branches. Traceability is branch-based:

- Monolithic evidence lives on `exp/monolithic-baselines`.
- Gap trace evidence lives on `exp/gap-trace-integration`.
- Real instance evidence lives on `exp/large-instance-campaign`.
- Synthetic evidence lives on `exp/synthetic-stress`.

This is intentional branch isolation, but report reproduction commands must switch branches.

## Verdict

Traceability passes. Every audited CSV row points to an existing committed log file on its experiment branch.
