# Curated results — pmedian-benders

Snapshot of validated results at commit `d1f2e1e`.

**Rule:** files in this directory are frozen evidence snapshots.
Do not mutate. Do not overwrite with runner scripts.
`benchmark.csv` (in `results/`) is append-only scratch; curated copy is `benchmark_current.csv`.

## Files

| File | Source command | Notes |
|---|---|---|
| `orlib_optima_check.csv` | `scripts/run_benchmark.py` (orlib targets)  OR  manual cross-check | OR-Library pmed1–15 official optima comparison |
| `comparison_vs_paper.csv` | `scripts/compare_paper.py` (rl1304 Table 2 subset) | Paper OPT/LB/UB comparison, 9/9 delta_OPT=0 |
| `warmstart_comparison.csv` | Manual run warm vs cold | Warm-start nodes/cuts reduction; wall-time mixed |
| `benchmark_current.csv` | Append-consolidated from `results/benchmark.csv` | Frozen copy of scratch benchmark at commit `d1f2e1e` |

## Commit

```
d1f2e1e (HEAD -> final/report-evidence-consolidation)
```

## Provenance

Regenerate procedure:
1. `git checkout d1f2e1e`
2. `make clean && make`
3. See `scripts/run_benchmark.py --help` and `scripts/compare_paper.py --help`
4. Always backup `results/benchmark.csv` before regeneration (append-only risk).
5. Re-run `scripts/validate_results.py` after any change.
