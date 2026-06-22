# Overnight figures audit

## Scope

Audited committed PNG figures across experiment branches using PNG magic header and IHDR dimensions.

## Benders 300s figures

Branch: `exp/requirements-and-300s-benchmark`.

| figure | bytes | dimensions | readable PNG |
|---|---:|---|---|
| `benders_300s_runtime_by_instance.png` | 5726 | 1200x650 | yes |
| `benders_300s_nodes_by_instance.png` | 5726 | 1200x650 | yes |
| `benders_300s_lazy_cuts_by_instance.png` | 6136 | 1200x650 | yes |
| `benders_300s_runtime_vs_N.png` | 6920 | 900x620 | yes |
| `benders_300s_status_summary.png` | 3472 | 800x500 | yes |

## Gap trace figures

Branch: `exp/gap-trace-integration`.

| figure | bytes | dimensions | readable PNG |
|---|---:|---|---|
| `gap_vs_iteration_pmed1.png` | 4233 | 900x560 | yes |
| `bounds_vs_iteration_pmed1.png` | 4218 | 900x560 | yes |

## Benders vs monolithic figures

Branch: `exp/monolithic-baselines`.

| figure | bytes | dimensions | readable PNG |
|---|---:|---|---|
| `benders_vs_monolithic_runtime.png` | 4495 | 950x560 | yes |
| `benders_vs_monolithic_gap.png` | 3869 | 950x560 | yes |
| `benders_vs_monolithic_nodes.png` | 4688 | 950x560 | yes |

## Synthetic stress figures

Branch: `exp/synthetic-stress`.

| figure | bytes | dimensions | readable PNG |
|---|---:|---|---|
| `synthetic_runtime_vs_N.png` | 5588 | 950x560 | yes |
| `synthetic_lazy_cuts_vs_N.png` | 6010 | 950x560 | yes |
| `synthetic_nodes_vs_N.png` | 4817 | 950x560 | yes |
| `synthetic_timeout_summary.png` | 2909 | 800x480 | yes |

## Caution

Figures were generated with a custom stdlib PNG helper, not matplotlib. They are valid PNGs and nonempty, but visually simple. For final polished report, regenerating with matplotlib in an environment with dependencies would improve aesthetics; evidence value remains CSV-first.

## Verdict

All audited figures are nonempty readable PNG files.
