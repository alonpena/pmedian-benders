# Next agent handoff — pmedian-benders

Branch: `final/report-evidence-consolidation`  
Current commit at handoff creation: `128a289cec4a1e91d3e97c504aa6f763979ab601`  
Expected status: clean, pushed to `origin/final/report-evidence-consolidation`

## Project target

Level 2 replication now:

- replicate paper mechanism 1:1 where mathematical/core algorithm matters
- corroborate with reachable benchmark subset
- leave full paper campaign / Zebra / huge families as posterior enhancement

Do **not** target full Level 3 now:

- no Zebra local replication unless source/binary provided
- no PopStar unless source/implementation approved
- no huge TSPLIB/BIRCH/RW/ODM by default
- no CPLEX unless installed/licensed
- no claim of local Zebra outperformance

## Core honest claim

> Replicamos el mecanismo algorítmico central del paper y lo validamos computacionalmente sobre un subconjunto documentado. La campaña completa del paper, incluyendo Zebra y familias grandes, queda como trabajo futuro.

## Read first

1. `docs/AGENT_EXECUTION_RUNBOOK.md`
2. `docs/PAPER_REPLICATION_COMPLETION_ROADMAP.md`
3. `docs/CONSISTENCY_AND_REPLICATION_AUDIT.md`
4. `docs/FINAL_REPORT_FACTS_ONLY.md`
5. `docs/RESULTS_TRACEABILITY.md`
6. `src/separation.c`
7. `src/phase1.c`
8. `src/phase2.c`
9. `scripts/run_benchmark.py`
10. `scripts/compare_paper.py`

## Implemented core

- Master `y/theta`: `src/phase1.c`, `src/phase2.c`
- F3-derived/F4 lazy Benders cuts: `src/separation.c`
- Algorithm 1: `separation_all()`
- Algorithm 2 `ktilde`: `separation_k_tilde()`
- Sorted `S`: `src/sortsites.c`
- Phase 1 LP: `src/phase1.c`
- Phase 2 branch-and-Benders-cut: `src/phase2.c`, `src/solver_gurobi.c`
- Warm-start: `src/cutpool.c`
- Rounding heuristic: `src/heuristic.c`

## Not implemented

- Zebra
- PopStar
- constraint reduction
- reduced-cost fixing
- CPLEX backend
- monolithic F1/F2/F3/F4 full benchmark
- ODM forbidden assignments
- full BIRCH/RW/huge TSPLIB campaign

## Current evidence

- OR-Library `pmed1`–`pmed15`:
  - `results/orlib_optima_check.csv`
  - 15/15 `OPT_MATCH`, delta 0
- `rl1304` Table 2 subset:
  - `results/comparison_vs_paper.csv`
  - 9/9 OPT OK, `delta_OPT=0`
- `kroA100`:
  - `results/benchmark.csv`
  - opt 30539
- callback proof:
  - `results/logs/*.log`
  - `lazy_cuts > 0`
- warm/cold:
  - `results/warmstart_comparison.csv`
  - nodes/cuts drop, wall-time mixed
- separator proof:
  - `results/logs/verify_cuts_oracle_diff.log`
  - 0 diffs

## Important current decision

Do not execute full roadmap automatically.

Only safe default tasks:

1. A1 validate results
2. A2 build/tests
3. A3 smoke pipeline with backup/restore
4. A4 add `validate_results.py`
5. A5 create `results/curated/`
6. Stop and report

## Next implementation task recommended

Implement A4 + A5 from `docs/AGENT_EXECUTION_RUNBOOK.md`.

### A4 — create result validator

Create `scripts/validate_results.py`.

Checks:

1. duplicate keys in `results/benchmark.csv`
2. OR-Library status all `OPT_MATCH` and delta 0
3. `comparison_vs_paper` all OK and `delta_OPT=0`
4. required logs exist:
   - `results/logs/pmed1.pmp_p5_full.log`
   - `results/logs/rl1304_p5.pmp_p5_full.log`
   - `results/logs/kroA100.pmp_p10_full.log`
   - `results/logs/verify_cuts_oracle_diff.log`
5. required text inside logs:
   - `is_branch_and_benders_cut=YES`
   - `lazy_cuts > 0` where applicable
   - `diffs=0` for oracle diff

Acceptance:

```bash
.venv/bin/python scripts/validate_results.py
# RESULT: PASS
```

### A5 — create curated results

Create `results/curated/`.

Copy:

- `results/orlib_optima_check.csv`
- `results/comparison_vs_paper.csv`
- `results/warmstart_comparison.csv`
- `results/benchmark.csv` -> `results/curated/benchmark_current.csv`

Create `results/curated/README.md` documenting:

- source command for each CSV
- commit hash
- note `benchmark.csv` is append-only scratch unless curated

## Commands to run before changes

```bash
git status --short
make clean && make
make test
.venv/bin/python scripts/verify_cuts.py
.venv/bin/python tests/test_parse_orlib.py
```

## Do not mutate curated results during smoke tests

If smoke testing:

1. backup `results/benchmark.csv` and key logs to `/tmp`
2. run toy/pmed1/kroA100
3. restore benchmark/logs
4. remove toy generated log
5. verify `git status` unchanged before code changes

Smoke commands:

```bash
./pmedian instances/toy/toy1.pmp --p 2 --mode full --opt 6
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819
./pmedian instances/tsplib/kroA100.pmp --mode full
```

## Known pitfalls

- `results/benchmark.csv` is append-only; reruns duplicate rows.
- `compare_paper.py` appends benchmark rows indirectly.
- Do not compare local Gurobi times directly to paper CPLEX times.
- Do not mention Zebra as local result.
- `pmed17`–`pmed40` evidence exists in `report/evidence`, but raw main instances absent.
- Huge instances likely memory-risk because `S` is full `N x M`.

## If implementing time limit later

Do not just set `TimeLimit` and call `solver_objval` blindly.

Need robust solver status handling for `TIME_LIMIT` / no incumbent.

Files likely involved:

- `src/solver.h`
- `src/solver_gurobi.c`
- `src/phase2.c`
- `src/main.c`

Need CSV status semantics.

## Commit message for next task

```bash
scripts: add result evidence validator and curated outputs
```

## Final response expected from next agent

Include:

1. branch/commit
2. git status
3. commands run
4. files changed
5. validation PASS/FAIL
6. whether results regenerated
7. whether Zebra run (should be NO)
8. remaining blockers
