# Overnight timeout audit

## Scope

Audited committed experiment evidence across branches, not only current worktree.

## Branch evidence map

| artifact | branch | commit |
|---|---|---|
| `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | `1de348e` |
| `results/monolithic_f1_300s.csv` | `exp/monolithic-baselines` | `aea894a` |
| `results/benders_real_instances_300s.csv` | `exp/large-instance-campaign` | `5240bde` |
| `results/synthetic_stress_300s.csv` | `exp/synthetic-stress` | `c5de792` |
| `results/gap_traces/` | `exp/gap-trace-integration` | `11db33b` |

## Timeout enforcement

| wrapper | branch | evidence | verdict |
|---|---|---|---|
| `scripts/run_benchmark_300s.py` | `exp/requirements-and-300s-benchmark` | default `DEFAULT_TIMEOUT = 300`, `subprocess.run(..., timeout=timeout)` | PASS |
| `scripts/run_gap_trace_smoke.py` | `exp/gap-trace-integration` | `TIMEOUT = 300`, `subprocess.run(..., timeout=TIMEOUT)` | PASS |
| `scripts/run_monolithic_f1_300s.py` | `exp/monolithic-baselines` | `TIMEOUT = 300`, `subprocess.run(..., timeout=TIMEOUT)` | PASS |
| `scripts/run_real_instances_300s.py` | `exp/large-instance-campaign` | `TIMEOUT = 300`, calls `bench.run_case(..., TIMEOUT, ...)` | PASS |
| `scripts/run_synthetic_stress_300s.py` | `exp/synthetic-stress` | `TIMEOUT = 300`, calls `bench.run_case(..., TIMEOUT, ...)` | PASS |

## Timeout counts

| CSV | rows | timeout_flag=0 | timeout_flag=1 |
|---|---:|---:|---:|
| Benders 300s | 26 | 26 | 0 |
| Monolithic F1 300s | 5 | 5 | 0 |
| Real instances 300s | 26 | 26 | 0 |
| Synthetic stress 300s | 18 | 18 | 0 |

## Max runtime rows

| CSV | runtime column | max runtime | instance |
|---|---|---:|---|
| Benders 300s | `Ttot` | 14.191127 | `rl1304_p10` |
| Monolithic F1 300s | `runtime` | 6.991906 | `pmed6` |
| Real instances 300s | `Ttot` | 14.217998 | `rl1304_p10` |
| Synthetic stress 300s | `Ttot` | 44.247668 | `euclidean_N5000_p5pct` |

## Suspicious or caution items

- Monolithic F1 logs do not include `TIMEOUT_SECONDS` metadata inside each log. Timeout is enforced by wrapper source and represented in CSV `timeout_flag`, but logs are less self-describing than Benders wrapper logs.
- Current branch `exp/final-experimental-handoff` does not contain every artifact from all experimental branches. Audit uses committed branch objects.

## Verdict

Timeout audit passes for wrapper enforcement and CSV timeout flags. Caveat: monolithic logs should include timeout metadata in future reruns.
