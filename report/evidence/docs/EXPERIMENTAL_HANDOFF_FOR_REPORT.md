# Experimental handoff for report

## Purpose

Consolidated experimental handoff only. Not final academic narrative.

## Branch/commit map

| phase | branch | commit(s) | scope |
|---|---|---|---|
| FASE 0–1 | `exp/requirements-and-300s-benchmark` | `bf33671`, `1de348e` | autonomous plan + Benders 300s figures |
| FASE 2 | `exp/gap-trace-integration` | `11db33b` | Phase 1 gap traces |
| FASE 3–4 | `exp/monolithic-baselines` | `92381db`, `aea894a`, `98b84e9` | monolithic F1 baseline + comparison plots |
| FASE 5 | `exp/large-instance-campaign` | `1ce87ee`, `5240bde` | paper-instance inventory + real READY campaign |
| FASE 6 | `exp/synthetic-stress` | `d6241d8`, `c5de792` | synthetic generator + stress campaign |
| FASE 7 | `exp/final-experimental-handoff` | this commit | consolidation doc |

## 1. What was implemented

- Benders 300s campaign visualizations from committed CSV evidence.
- Optional non-invasive Phase 1 gap trace logging (`--gap-trace PATH`) on separate branch.
- Experimental monolithic F1 baseline mode (`--mode monolithic-f1`) on separate branch.
- Real-instance inventory and READY campaign wrapper.
- Synthetic Euclidean instance generator and 300s stress wrapper.
- Plot scripts using stdlib PNG output because local Python lacks `matplotlib`, `pandas`, `numpy`.

## 2. What was run

### Existing Benders 300s campaign

Evidence:

- `results/benders_300s_campaign.csv`
- `results/logs/benders_300s/`
- branch `exp/requirements-and-300s-benchmark`, commit `1de348e`

Summary:

| rows | OPT_MATCH | OPTIMAL_NO_KNOWN | TIMEOUT | max Ttot |
|---:|---:|---:|---:|---:|
| 26 | 25 | 1 | 0 | 14.191127 |

### Gap traces

Evidence:

- branch `exp/gap-trace-integration`, commit `11db33b`
- `results/gap_traces/*_phase1.csv`
- `results/logs/gap_traces/`

Rows:

| instance | p | trace rows | final gap |
|---|---:|---:|---:|
| toy1 | 2 | 3 | 0 |
| pmed1 | 5 | 6 | 0 |
| pmed6 | 5 | 6 | 0.010614 |
| rl1304 | 5 | 6 | 0 |

### Monolithic F1 baseline

Evidence:

- branch `exp/monolithic-baselines`, commits `92381db`, `aea894a`
- `results/monolithic_f1_300s.csv`
- `results/logs/monolithic_f1/`

Summary:

| rows | OPTIMAL | TIMEOUT | max runtime |
|---:|---:|---:|---:|
| 5 | 5 | 0 | 6.991906 |

### Benders vs monolithic plots

Evidence:

- branch `exp/monolithic-baselines`, commit `98b84e9`
- `results/figures/benders_vs_monolithic_runtime.png`
- `results/figures/benders_vs_monolithic_gap.png`
- `results/figures/benders_vs_monolithic_nodes.png`

Overlap:

| instance | Benders Ttot | Monolithic runtime | Benders nodes | Monolithic nodes |
|---|---:|---:|---:|---:|
| toy1 | 0.040586 | 0.024817 | 1 | 1 |
| pmed1 | 0.035466 | 0.436110 | 1 | 1 |
| pmed2 | 0.083832 | 0.441374 | 1 | 1 |
| pmed6 | 0.310273 | 6.991906 | 7 | 1 |
| kroA100 | 0.067967 | 0.461514 | 1 | 1 |

### Real READY instance campaign

Evidence:

- branch `exp/large-instance-campaign`, commits `1ce87ee`, `5240bde`
- `docs/PAPER_REPLICATION_MATRIX.md`
- `results/benders_real_instances_300s.csv`
- `results/logs/real_instances_300s/`

Summary:

| rows | OPT_MATCH | OPTIMAL_NO_KNOWN | TIMEOUT | max Ttot |
|---:|---:|---:|---:|---:|
| 26 | 24 | 2 | 0 | 14.217998 |

### Synthetic stress

Evidence:

- branch `exp/synthetic-stress`, commits `d6241d8`, `c5de792`
- `instances/synthetic/`
- `results/synthetic_stress_300s.csv`
- `results/logs/synthetic_stress_300s/`

Summary:

| rows | OPTIMAL_NO_KNOWN | TIMEOUT | max Ttot | max case |
|---:|---:|---:|---:|---|
| 18 | 18 | 0 | 44.247668 | `euclidean_N5000_p5pct` |

## 3. Models compared

- Core Benders/F4-style method already verified in repository.
- Monolithic F1 classical assignment model:
  - `y_j` binary;
  - `x_ij` continuous in `[0,1]`;
  - `sum_j y_j = p`;
  - `sum_j x_ij = 1`;
  - `x_ij <= y_j`.

Not compared:

- Zebra.
- PopStar.
- Monolithic F3/F4.
- Reduced-cost fixing variants.
- Constraint-reduction variants.

## 4. Paper instances replicated locally

Supported by local CSV/log evidence:

- OR-Library `pmed1`–`pmed15`.
- TSPLIB `rl1304` p-grid available locally: `5,10,20,50,100,200,300,400,500`.
- TSPLIB `kroA100` solved locally but no trusted known optimum supplied.

Inventory but not run:

- OR-Library `pmed16`–`pmed40`: optima present, instance files missing.
- TSPLIB `fl1400`, `u1432`, `vm1748`: raw `.tsp` present, `.pmp` p-grid missing.
- BIRCH, ODM, RW large: missing local data.

## 5. What remained out

- Full paper replication.
- Zebra local build/run.
- PopStar initialization.
- Reduced-cost fixing.
- Constraint reduction.
- BIRCH/ODM/RW large campaigns.
- Huge TSPLIB runs.
- Hardware-normalized timing analysis.

## 6. Final tables to use

Use only tables backed by CSV/log evidence:

1. Benders 300s campaign table from `results/benders_300s_campaign.csv`.
2. Gap trace table from `results/gap_traces/*_phase1.csv` on `exp/gap-trace-integration`.
3. Monolithic F1 table from `results/monolithic_f1_300s.csv` on `exp/monolithic-baselines`.
4. Benders-vs-F1 overlap table from `docs/BENDERS_VS_MONOLITHIC_HANDOFF.md`.
5. Real-instance READY campaign table from `results/benders_real_instances_300s.csv` on `exp/large-instance-campaign`.
6. Synthetic stress table from `results/synthetic_stress_300s.csv` on `exp/synthetic-stress`.

## 7. Final figures to use

- `results/figures/benders_300s_runtime_by_instance.png`
- `results/figures/benders_300s_nodes_by_instance.png`
- `results/figures/benders_300s_lazy_cuts_by_instance.png`
- `results/figures/benders_300s_runtime_vs_N.png`
- `results/figures/benders_300s_status_summary.png`
- `results/figures/gap_vs_iteration_pmed1.png`
- `results/figures/bounds_vs_iteration_pmed1.png`
- `results/figures/benders_vs_monolithic_runtime.png`
- `results/figures/benders_vs_monolithic_gap.png`
- `results/figures/benders_vs_monolithic_nodes.png`
- `results/figures/synthetic_runtime_vs_N.png`
- `results/figures/synthetic_lazy_cuts_vs_N.png`
- `results/figures/synthetic_nodes_vs_N.png`
- `results/figures/synthetic_timeout_summary.png`

## 8. Reproduction commands

### Benders 300s figures

```bash
git switch exp/requirements-and-300s-benchmark
python3 scripts/plot_benders_300s.py
```

### Gap traces

```bash
git switch exp/gap-trace-integration
make clean && make && make test
python3 scripts/run_gap_trace_smoke.py
python3 scripts/plot_gap_trace.py
```

### Monolithic F1 baseline

```bash
git switch exp/monolithic-baselines
make clean && make && make test
python3 scripts/run_monolithic_f1_300s.py
python3 scripts/plot_benders_vs_monolithic.py
```

### Real READY campaign

```bash
git switch exp/large-instance-campaign
make clean && make && make test
python3 scripts/run_real_instances_300s.py
```

### Synthetic stress

```bash
git switch exp/synthetic-stress
make clean && make && make test
python3 scripts/gen_synthetic_euclidean.py
python3 scripts/run_synthetic_stress_300s.py
python3 scripts/plot_synthetic_stress.py
```

## 9. Claims permitted

- Local project implements and tests a Benders decomposition core for p-median.
- Local 300s Benders wrapper campaign solved 26 curated rows with 0 timeouts.
- Local Phase 1 gap trace logging exists and produced traces for toy1, pmed1, pmed6, and rl1304 p=5.
- Local monolithic F1 baseline exists and solved five small/medium rows with 0 timeouts.
- On five overlapping rows, Benders local runtime is lower than monolithic F1 except toy1.
- Local READY real-instance campaign solved OR-Library pmed1–pmed15 plus preprocessed TSPLIB rows and rw12 with 0 timeouts.
- Synthetic Euclidean stress grid completed 18 rows with 0 timeouts, up to N=5000.

## 10. Claims prohibited

- We replicated the full paper.
- We outperform Zebra.
- We ran Zebra locally.
- We implemented PopStar.
- We implemented reduced-cost fixing.
- We implemented constraint reduction.
- We ran BIRCH, ODM, RW large, or huge TSPLIB.
- We compared against paper's monolithic C baseline.
- Runtime conclusions are machine-independent.
- Synthetic results prove behavior on all large real instances.

## 11. Recommendations for report

- Present this as progressive, evidence-backed partial replication.
- Separate verified Benders core, added baselines, and missing paper components.
- Use CSV/log-backed tables only.
- Label all runtime plots as local hardware/software evidence.
- For gap comparison, explain metric definitions before interpreting.
- Put limitations near results, not only at end.
- Avoid Zebra language except as paper-reported background.

## 12. Overnight verification update

Added on branch `exp/orlib-pmed16-smoke` after forensic audit.

### What is now report-ready

- Benders 300s campaign evidence: row counts, statuses, timeout flags, logs, and figures verified.
- Gap trace evidence: trace CSVs and pmed1 figures verified on `exp/gap-trace-integration`.
- Monolithic F1 evidence: five-row baseline verified, with caution about log metadata.
- Real READY campaign evidence: CSV/log traceability verified.
- Synthetic stress evidence: 18 generated instances validated against intended `N` and `p`; CSV/logs/figures verified.
- OR-Library pmed16 smoke: official source downloaded, converted, solved under 300s wrapper, objective matched official optimum 8162.

### What is suspicious or requires caution

- Current branch isolation means not all artifacts exist simultaneously on one branch. Reproduction must switch to the correct branch.
- Monolithic F1 logs do not include `TIMEOUT_SECONDS` metadata, although wrapper source and CSV enforce/report timeout.
- Gap columns are not identical metrics across Benders and monolithic F1; explain definitions before comparing.
- Synthetic rows are `OPTIMAL_NO_KNOWN`; no independent benchmark optima.
- pmed16 is only a smoke row, not a completed pmed16–pmed40 campaign.

### What was verified overnight

Audit docs created:

- `docs/OVERNIGHT_TIMEOUT_AUDIT.md`
- `docs/OVERNIGHT_TRACEABILITY_AUDIT.md`
- `docs/OVERNIGHT_LOG_AUTHENTICITY_AUDIT.md`
- `docs/OVERNIGHT_SYNTHETIC_INSTANCE_AUDIT.md`
- `docs/OVERNIGHT_FIGURES_AUDIT.md`
- `docs/WEB_SOURCE_AND_REPLICATION_FEASIBILITY_AUDIT.md`

Safe addition:

- `docs/ORLIB_PMED16_SMOKE_HANDOFF.md`
- `results/orlib_pmed16_smoke_300s.csv`
- `results/logs/orlib_pmed16_smoke/pmed16_300s.log`
- `instances/orlib/pmed16.txt`
- `instances/orlib/pmed16.pmp`

### Internet/source audit findings

- Official OR-Library pmed1–pmed40 files are available from J.E. Beasley OR-Library.
- Official TSPLIB direct `.tsp.gz` files are available for rl1304, fl1400, u1432, vm1748, d2103, pcb3038, fl3795, rl5934, usa13509. `sw24978` was not found at checked TSPLIB mirror URLs.
- No trustworthy official PopStar source found during light audit.
- No trustworthy official Zebra source found during light audit. A GitHub repository named `p-median-zebra` exists, but it is not proven to be the paper Zebra code and must not support Zebra claims.
- BIRCH/ODM exact data sources remain unresolved locally; RW has local generator/tiny smoke only.

### Feasible next components

1. OR-Library pmed17–pmed40 bounded campaign from official source.
2. TSPLIB fl1400/u1432/vm1748 preprocessing and smoke runs after defining p-grid.
3. RW generated campaign, clearly labeled RW-like/local generator, not paper-exact data.
4. PopStar/Zebra only if trustworthy source/provenance appears.

### Impossible or too risky tonight

- Zebra implementation/build.
- PopStar integration.
- ODM parser/model support.
- Huge TSPLIB or `usa13509` campaign without memory profiling.
- Full BIRCH/RW-large/ODM paper campaign.

### Exact next action for morning

Create a dedicated OR-Library expansion branch and run pmed17–pmed20 first under the same 300s wrapper style. If clean, expand to pmed21–pmed40 and generate one consolidated OR-Library pmed1–pmed40 CSV/log handoff.
