# Instance sources and benchmark pipeline

Purpose: explain where instances come from, how they become `.pmp`, how to run experiments, and which models are actually accessible from code.

## Key clarification: which formulations are implemented?

| Formulation/model | In report theory? | In C solver? | Evidence | How to use |
|---|---:|---:|---|---|
| F1 classical `x_ij,y_j` | yes | no monolithic C solver | `report/sections/03_formulaciones.tex`; brute-force evaluator in `src/instance.c` only | not selectable from CLI |
| F2 radius `z_i^k` | yes | no | documentation only | not selectable |
| F3 sparse `z_i^k` | yes | not materialized in C | Python oracle/prototype only; C derives Benders cuts from F3 | not selectable as monolithic C |
| F4 compact all cuts | yes | not loaded upfront | C generates F4-style cuts lazily | via Benders mode |
| Benders/F4 lazy derived from F3 | yes | yes | `src/phase1.c`, `src/phase2.c`, `src/separation.c` | `./pmedian ... --mode full` |

Bottom line: **the implemented/tested solver is Benders / F4 lazy-cut formulation derived from F3**. F1–F4 are explained in the report; they are not all implemented as selectable C models.

## Main solver CLI

```bash
./pmedian <instance.pmp> [--p P] [--mode phase1|full] [-v] [--opt V] [--coldstart] [--dump-cuts ...]
```

Examples:

```bash
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819
./pmedian instances/orlib/pmed1.pmp --mode phase1 --opt 5819
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819 --coldstart
./pmedian instances/toy/toy1.pmp --p 2 --dump-cuts 0 1
```

## User-friendly benchmark pipeline

Use `scripts/paperbench.py`. It avoids YAML and provides built-in case sets. The `current` set is the full local runnable catalog, not the full paper campaign; full paper reproduction still needs external Zebra/PopStar/data/provenance.

```bash
.venv/bin/python scripts/paperbench.py sources
.venv/bin/python scripts/paperbench.py list --set smoke
.venv/bin/python scripts/paperbench.py prepare --set current
.venv/bin/python scripts/paperbench.py run --set smoke --timeout 300 \
  --out results/curated/paperbench_smoke.csv \
  --log-dir results/logs/paperbench_smoke
.venv/bin/python scripts/paperbench.py summarize --csv results/curated/paperbench_smoke.csv
.venv/bin/python scripts/paperbench.py validate --csv results/curated/paperbench_smoke.csv
```

Built-in sets:

| Set | Contents | Use |
|---|---|---|
| `smoke` | `toy1`, `pmed1`, `kroA100` | fast pipeline test |
| `current` | `toy1`, OR-Library `pmed1`–`pmed15`, `kroA100`, `rl1304` p-grid | full local current catalog |
| `orlib` | OR-Library `pmed1`–`pmed15` | official optima check |
| `rl1304` | paper Table 2 `rl1304` p-grid | paper subset check |
| `kro` | `kroA100` | geometric sanity check |

Why use `paperbench.py` instead of `run_benchmark.py`?

- `run_benchmark.py` and `compare_paper.py` use `./pmedian`, which appends to `results/benchmark.csv`.
- `paperbench.py run` executes `./pmedian` from a temporary working directory, so append-only scratch files do not pollute repo results.
- It writes clean CSV + logs to explicit paths.

## Instance format

Internal solver format: `.pmp`.

See `docs/INSTANCE_FORMAT.md`.

Two variants:

1. Coordinates: first line `N M p`, then rows `id x y`.
2. Matrix: first line `N M p`, second line `MATRIX`, then distance matrix.

## OR-Library source and conversion

Current local raw files:

```text
instances/orlib/pmed1.txt ... pmed15.txt
instances/orlib/pmedopt.txt
```

Convert raw to `.pmp`:

```bash
.venv/bin/python scripts/parse_orlib.py \
  instances/orlib/pmed1.txt \
  instances/orlib/pmed1.pmp
```

Pipeline:

```text
OR-Library raw graph pmed*.txt
  -> scripts/parse_orlib.py
  -> all-pairs shortest paths matrix
  -> instances/orlib/pmed*.pmp
  -> ./pmedian
```

Important data rule:

- OR-Library duplicate edges use **last occurrence wins**, not minimum edge.
- Evidence: `docs/ADR/0002-orlib-duplicate-edges.md`, `docs/orlib_pmed_format_spec.txt`.

Official optima:

- `instances/orlib/pmedopt.txt`.

To extend to `pmed16`–`pmed40`:

1. Add raw `pmed16.txt` … `pmed40.txt` from OR-Library with provenance/checksum.
2. Parse with `scripts/parse_orlib.py` or `paperbench.py prepare` after catalog extension.
3. Run with official optima.
4. Do not use archived evidence as fully reproducible unless raw inputs are present.

## TSPLIB source and conversion

Current local raw files include:

```text
instances/tsplib/rl1304.tsp
instances/tsplib/kroA100.tsp
instances/tsplib/fl1400.tsp
instances/tsplib/u1432.tsp
instances/tsplib/vm1748.tsp
```

Convert raw `.tsp` to `.pmp` for a chosen `p`:

```bash
.venv/bin/python scripts/parse_tsplib.py \
  instances/tsplib/rl1304.tsp \
  5 \
  instances/tsplib/rl1304_p5.pmp
```

Pipeline:

```text
TSPLIB .tsp coordinates
  -> scripts/parse_tsplib.py with p
  -> instances/tsplib/<name>_p<p>.pmp
  -> ./pmedian
```

Distance convention:

- This project uses Euclidean **floor**, matching the paper for `rl1304`.
- TSPLIB canonical rounding may differ; do not switch without retesting.

Paper subset currently implemented:

- `rl1304` p-grid: `5,10,20,50,100,200,300,400,500`.
- Paper values transcribed in `scripts/compare_paper.py`.

To extend full paper Table 2:

1. Transcribe p-grid + OPT/LB/UB for `fl1400`, `u1432`, `vm1748` from paper.
2. Generate `.pmp` for each p.
3. Add cases to `scripts/paperbench.py` catalog or create a proper manifest later.
4. Run and write a new curated CSV.

## RW generator

Script:

```bash
.venv/bin/python scripts/gen_rw.py N p seed salida.pmp [--symmetric]
```

Example:

```bash
mkdir -p instances/rw
.venv/bin/python scripts/gen_rw.py 100 10 1 instances/rw/rw100_p10_seed1.pmp
./pmedian instances/rw/rw100_p10_seed1.pmp --mode full
```

Caveat:

- This produces RW-like matrices matching the broad description.
- It is not a paper Table 8 replication unless exact paper seeds/spec are documented.

## BIRCH-like generator

Script:

```bash
.venv/bin/python scripts/gen_birch.py N p seed n_clusters salida.pmp
```

Example:

```bash
mkdir -p instances/birch
.venv/bin/python scripts/gen_birch.py 1000 100 1 10 instances/birch/birch1000_p100.pmp
./pmedian instances/birch/birch1000_p100.pmp --mode full
```

Caveat:

- This is **BIRCH-like synthetic**, not verified exact paper BIRCH.
- Do not present as paper BIRCH unless exact source/generator/seeds are established.

## ODM

Status: not supported.

Reason:

- ODM requires forbidden assignments.
- Current `.pmp` format and separation assume every client-site assignment is allowed.
- Needs model/parser/separation audit before use.

## Comparators

| Comparator | Status |
|---|---|
| Zebra | not in repo; paper-reported only |
| PopStar | not implemented; rounding heuristic used |
| AvellaB&C | not in repo |
| AvellaHeu | not in repo |
| IrawanHeu | not in repo |

Do not claim local comparator performance without executable + command + CSV + log.

## Recommended interaction patterns

### Check current evidence

```bash
.venv/bin/python scripts/validate_results.py
```

### Explore available cases

```bash
.venv/bin/python scripts/paperbench.py list --set current
```

### Prepare missing `.pmp` files for current catalog

```bash
.venv/bin/python scripts/paperbench.py prepare --set current
```

### Run non-mutating smoke benchmark

```bash
.venv/bin/python scripts/paperbench.py run --set smoke --timeout 300 \
  --out results/curated/paperbench_smoke.csv \
  --log-dir results/logs/paperbench_smoke
```

### Run full local current catalog non-mutating

```bash
.venv/bin/python scripts/paperbench.py run --set current --timeout 300 \
  --out results/curated/paperbench_current.csv \
  --log-dir results/logs/paperbench_current
.venv/bin/python scripts/paperbench.py summarize --csv results/curated/paperbench_current.csv
.venv/bin/python scripts/paperbench.py validate --csv results/curated/paperbench_current.csv
```

## What to say in report

Allowed:

> The C implementation exposes the Benders/F4 lazy-cut method derived from F3. F1–F4 are documented mathematically; they are not all implemented as selectable C formulations.

Allowed:

> Official OR-Library and TSPLIB inputs are converted to the internal `.pmp` format by parser scripts; generated RW/BIRCH-like instances are local stress tests unless exact paper provenance is established.

Forbidden:

> We implemented and benchmarked F1, F2, F3, and F4 monolithic formulations.

Forbidden:

> BIRCH/RW/ODM paper campaigns were reproduced.

Forbidden:

> We outperform Zebra locally.
