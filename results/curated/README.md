# Curated results — pmedian-benders

Frozen/validated evidence snapshots used by report and slides.

**Rule:** files in this directory are treated as final evidence snapshots. Do not overwrite casually. `results/benchmark.csv` in repo root is append-only scratch; `benchmark_current.csv` is the curated copy.

## Files

| File | Source command | Notes |
|---|---|---|
| `orlib_optima_check.csv` | `.venv/bin/python scripts/run_benchmark.py` (OR-Library targets) | OR-Library `pmed1`–`pmed15` official optima comparison; 15/15 delta=0 |
| `comparison_vs_paper.csv` | `.venv/bin/python scripts/compare_paper.py` | Paper Table 2 subset for `rl1304`; 9/9 `delta_OPT=0` |
| `warmstart_comparison.csv` | Manual warm/cold runs documented in docs | Warm-start nodes/cuts reduction; wall-time mixed |
| `benchmark_current.csv` | Copy of `results/benchmark.csv` after validation | Combined scratch benchmark snapshot; avoid rerun appends |
| `paperbench_smoke.csv` | `.venv/bin/python scripts/paperbench.py run --set smoke --timeout 300 --out results/curated/paperbench_smoke.csv --log-dir results/logs/paperbench_smoke` | Non-contaminating smoke run: `toy1`, `pmed1`, `kroA100` |

## Validation

Run:

```bash
.venv/bin/python scripts/validate_results.py
```

Expected:

```text
RESULT: PASS
```

## Regeneration policy

1. Backup existing CSV/logs.
2. Regenerate with explicit command.
3. Run `scripts/validate_results.py`.
4. If using `paperbench.py`, prefer writing to a new file under `results/curated/` and logs under `results/logs/paperbench_*`.
5. Update `docs/RESULTS_TRACEABILITY.md` if any numbers used in report/slides change.

## Notes

- `scripts/run_benchmark.py` and `scripts/compare_paper.py` can append rows to `results/benchmark.csv`; this is why curated snapshots exist.
- `scripts/paperbench.py` runs from a temporary working directory, so it does not contaminate repo-level `results/benchmark.csv`.
- Zebra is not run locally; no curated Zebra result exists.
