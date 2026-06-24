# Agent-executable runbook — paper replication roadmap

Purpose: turn `docs/PAPER_REPLICATION_COMPLETION_ROADMAP.md` into tasks an agent can execute without inventing evidence.

Rule: tasks marked `EXECUTABLE_NOW` may be run by agent. Tasks marked `BLOCKED_EXTERNAL` require user-supplied data/code/license or explicit approval. Tasks marked `DO_NOT_RUN_DEFAULT` are too large/risky for routine agent execution.

## Global guardrails

1. Never claim local Zebra result unless a Zebra executable, command, CSV row, and log exist.
2. Never overwrite curated results without backup.
3. Never run huge experiments by default.
4. Keep `git status --short` clean before and after each work package.
5. For every numeric claim, create/update trace row in `docs/RESULTS_TRACEABILITY.md`.
6. For every experiment, store:
   - command
   - input instance path
   - solver/version
   - time limit
   - stdout/stderr log
   - CSV row
   - status: OPTIMAL, TIME_LIMIT, MEMORY_LIMIT, ERROR, NOT_RUN

## Task groups

### A. Executable now — safe maintenance and reproducibility

#### A1. Validate current results are clean

Status: `EXECUTABLE_NOW`

Commands:

```bash
git status --short
.venv/bin/python - <<'PY'
import csv, collections, pathlib, sys
p=pathlib.Path('results/benchmark.csv')
if not p.exists():
    print('MISSING results/benchmark.csv'); sys.exit(1)
rows=list(csv.DictReader(p.open()))
key=lambda r:(r['instance'],r['mode'],r.get('opt_known',''))
dups=[(k,v) for k,v in collections.Counter(map(key,rows)).items() if v>1]
print(f'rows={len(rows)} duplicates={len(dups)}')
for k,v in dups: print('DUP',k,v)
sys.exit(1 if dups else 0)
PY
```

Acceptance:
- `duplicates=0`.
- If duplicates exist, stop and ask whether to restore, dedupe, or archive.

#### A2. Run core build/tests

Status: `EXECUTABLE_NOW`

Commands:

```bash
make clean && make
make test
.venv/bin/python scripts/verify_cuts.py
.venv/bin/python tests/test_parse_orlib.py
```

Acceptance:
- Build succeeds.
- `make test` prints PASS twice.
- `verify_cuts.py` prints 0 diffs.
- OR-Library duplicate-edge parser test PASS.

#### A3. Smoke Benders pipeline without changing curated results

Status: `EXECUTABLE_NOW`

Commands:

```bash
mkdir -p /tmp/pmedian_audit_backup
cp results/benchmark.csv /tmp/pmedian_audit_backup/benchmark.csv 2>/dev/null || true
cp results/logs/pmed1.pmp_p5_full.log /tmp/pmedian_audit_backup/pmed1.log 2>/dev/null || true
cp results/logs/kroA100.pmp_p10_full.log /tmp/pmedian_audit_backup/kroA100.log 2>/dev/null || true

./pmedian instances/toy/toy1.pmp --p 2 --mode full --opt 6 | tee /tmp/pmedian_toy_smoke.log
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819 | tee /tmp/pmedian_pmed1_smoke.log
./pmedian instances/tsplib/kroA100.pmp --mode full | tee /tmp/pmedian_kroA100_smoke.log

cp /tmp/pmedian_audit_backup/benchmark.csv results/benchmark.csv 2>/dev/null || true
cp /tmp/pmedian_audit_backup/pmed1.log results/logs/pmed1.pmp_p5_full.log 2>/dev/null || true
cp /tmp/pmedian_audit_backup/kroA100.log results/logs/kroA100.pmp_p10_full.log 2>/dev/null || true
rm -f results/logs/toy1.pmp_p2_full.log
```

Acceptance:
- toy1 opt=6.
- pmed1 opt=5819.
- kroA100 opt=30539.
- lazy cuts > 0 for pmed1/kroA100.
- `git status --short` unchanged.

#### A4. Add permanent result validator script

Status: `EXECUTABLE_NOW`

Implementation target:

- Create `scripts/validate_results.py`.
- It must check:
  - duplicate keys in `results/benchmark.csv`.
  - all `results/orlib_optima_check.csv` rows have `status=OPT_MATCH` and `delta=0`.
  - all `results/comparison_vs_paper.csv` rows have `opt_comparison=OK` and `delta_OPT=0`.
  - referenced core logs exist for `pmed1`, `rl1304_p5`, `kroA100`, separator diff.

Acceptance:

```bash
.venv/bin/python scripts/validate_results.py
# RESULT: PASS
```

Commit message:

```bash
git add scripts/validate_results.py docs/RESULTS_TRACEABILITY.md
git commit -m "scripts: add result evidence validator"
```

#### A5. Create curated results directory

Status: `EXECUTABLE_NOW`

Commands:

```bash
mkdir -p results/curated
cp results/orlib_optima_check.csv results/curated/
cp results/comparison_vs_paper.csv results/curated/
cp results/warmstart_comparison.csv results/curated/
cp results/benchmark.csv results/curated/benchmark_current.csv
```

Also create `results/curated/README.md` with:

- source command for each CSV
- commit hash
- note that `benchmark.csv` is append-only scratch unless curated

Acceptance:
- `results/curated/README.md` exists.
- `scripts/validate_results.py` can validate curated files or normal files.

#### A6. Add time-limit support to local solver

Status: `EXECUTABLE_NOW_WITH_CODE_CHANGE`

Files:
- `src/main.c`
- `src/phase2.h`, `src/phase2.c`
- `src/solver.h`, `src/solver_gurobi.c` only if generic setter already enough

Implementation:
- Add CLI option `--time-limit SEC`.
- Pass to Phase 2 Gurobi param `TimeLimit`.
- Ideally also Phase 1 if desired.
- Log status and whether time limit hit.

Acceptance:

```bash
make clean && make
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819 --time-limit 300
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819 --time-limit 1
```

Expected:
- 300s run OPTIMAL_MATCH.
- 1s run should not crash; status explicit.

Caution:
- Requires status handling beyond current `solver_objval` assumptions. Implement carefully.

### B. Executable now but may consume time

#### B1. Regenerate OR-Library pmed1–15

Status: `EXECUTABLE_NOW_MODERATE`

Commands:

```bash
mkdir -p results/archive
cp results/benchmark.csv results/archive/benchmark.before_orlib.csv 2>/dev/null || true
cp results/orlib_optima_check.csv results/archive/orlib.before_orlib.csv 2>/dev/null || true
rm -f results/benchmark.csv results/orlib_optima_check.csv
.venv/bin/python scripts/run_benchmark.py
.venv/bin/python scripts/validate_results.py || true
```

Acceptance:
- 15 rows in `orlib_optima_check.csv`.
- all `OPT_MATCH`, delta 0.

Risk:
- destroys combined benchmark unless archived. Use only if user asks.

#### B2. Regenerate `rl1304` Table 2 subset

Status: `EXECUTABLE_NOW_MODERATE`

Command:

```bash
.venv/bin/python scripts/compare_paper.py
```

Acceptance:
- 9/9 OPT match.
- no duplicate benchmark rows if benchmark is kept curated or restored.

Caution:
- `compare_paper.py` appends to `results/benchmark.csv` via solver runs. Backup/restore or dedupe.

### C. Needs external data/provenance

#### C1. Full Table 2 beyond `rl1304`

Status: `BLOCKED_EXTERNAL_PARTIAL`

Needed:
- exact Table 2 p-grid and OPT/LB/UB values for `fl1400`, `u1432`, `vm1748`.
- `.pmp` generated for each p.

Agent can do only if:
- values are transcribed from PDF or provided.
- raw `.tsp` files exist or are downloaded with provenance.

Acceptance:
- `results/table2_tsp_small_local_benders.csv`.
- logs per instance/p.
- no Zebra local claim.

#### C2. OR-Library pmed16–40 reproducible rerun

Status: `BLOCKED_EXTERNAL_PARTIAL`

Needed:
- raw pmed16–40 files in `instances/orlib/` or downloader.

Current:
- archived evidence exists under `report/evidence/`, but raw main inputs absent.

Acceptance:
- raw files + `.pmp` + checksum manifest + clean CSV/logs.

#### C3. BIRCH exact campaign

Status: `BLOCKED_EXTERNAL`

Needed:
- exact BIRCH data/source/seeds from paper.

Do not use `scripts/gen_birch.py` as paper BIRCH unless explicitly labeled `BIRCH-like synthetic`.

#### C4. RW full campaign

Status: `BLOCKED_EXTERNAL_PARTIAL`

Needed:
- exact seeds/spec for RW instances.
- p-grid from paper.

Current tiny `rw12` is sanity check only.

#### C5. ODM campaign

Status: `BLOCKED_EXTERNAL_AND_MODEL_CHANGE`

Needed:
- ODM data.
- support forbidden assignments.
- verify cut validity under forbidden assignments.

### D. Not executable by agent as-is

#### D1. Zebra comparator

Status: `BLOCKED_EXTERNAL_HIGH_RISK`

Reason:
- no Zebra source/binary in repo.
- no trustworthy local build instructions.
- no logs/CSV.

Only executable if user supplies:
- source or binary
- license permissions
- build commands
- validation instance

Until then mandatory wording:

> Zebra no fue reejecutado localmente; la comparación con Zebra es un resultado reportado por el paper.

#### D2. PopStar comparator/initial heuristic

Status: `BLOCKED_EXTERNAL_OR_IMPLEMENTATION`

Needed:
- source or full reimplementation.
- validation against known PopStar outputs.

Without it:
- Keep rounding heuristic.
- State `UB1` may be weaker than paper.

#### D3. CPLEX backend

Status: `BLOCKED_LICENSE_OR_INSTALL`

Needed:
- CPLEX headers/libs/license.
- GenericCallback implementation.

Without it:
- Local solver remains Gurobi.
- Time comparisons remain machine/solver dependent.

#### D4. Huge TSP / huge BIRCH

Status: `DO_NOT_RUN_DEFAULT`

Reason:
- memory/time risk.
- current full `S` is `N x M`; huge instances likely infeasible without memory changes.

Requires explicit user approval, hardware check, and time budget.

## Agent default execution order

If user says “execute roadmap”, agent should run only this sequence unless given more data:

```text
A1 validate current results
A2 build/tests
A3 smoke pipeline with restore
A4 add validate_results.py
A5 create curated results directory
STOP and report status
```

Do not proceed to B/C/D without explicit approval.

## Final answer template after execution

Agent must report:

1. branch and commit hash
2. git status
3. commands run
4. files changed
5. PASS/FAIL for build/tests/validation
6. whether any results were regenerated
7. whether Zebra was run (normally no)
8. remaining blockers
