# PLAN — Efficient Benders Decomposition for the p-Median Problem (C replication)

**Course:** Optimización Computacional (PUCV) — transversal project, implementation deliverable.
**Paper replicated:** Duran-Mateluna, Ales & Elloumi (2023), *An efficient Benders decomposition for the p-median problem*, EJOR 308:84–96.
**Author:** Alonso Peña Domarchi.
**Language policy:** plans/roadmap in English (this file). All other artifacts (report, README, code comments) in Spanish. Code identifiers in English.

---

## 1. Goal & scope

Replicate the *core logic* of the paper in a clean, modular, reproducible C repository:

1. The **F3** formulation as the Benders base.
2. The **O(NM) separation algorithm** (Algorithms 1 & 2) — the intellectual heart: the subproblem dual has a closed form, so we never solve an LP to get a cut.
3. The **two-phase algorithm**: Phase 1 (LP master + cut loop + rounding) and Phase 2 (branch-and-Benders-cut via lazy callbacks).
4. **Instance generation + benchmark runner + preliminary analysis.**
5. A **report** (Spanish) that explains the full paper AND folds in the three pending course deliverables (Entrega 1 formulación, Entrega 2 lagrangiana teórica, Entrega 3 Benders teórico).

This is the base the professor wants for later modeling/solver optimizations — so faithfulness of the *core* matters more than covering every enhancement.

## 2. Pareto cut (what we build vs. what we only document)

**Build (high value, demonstrates mastery):**
- F3 reference model in Gurobi (baseline + correctness oracle).
- Separation Algorithm 1 + 2 in C, unit-tested against brute force.
- Phase 1: LP cut loop + rounding heuristic → LB1, UB1.
- Phase 2: branch-and-Benders-cut with Gurobi lazy callback.
- CLI to choose mode (`phase1` / `full`).
- Instance generation (RW, BIRCH) + parsers (OR-Library, TSP-Library).
- Benchmark runner → CSV; preliminary analysis.

**Document only (discuss as future work / "implemented partially"):**
- PopStar heuristic → replace with greedy/random init.
- Reduced-cost fixing and constraint reduction (mention; implement only if time).
- Huge instances (>100k), UFL extension, ODM forbidden allocations.

Rationale: the separation + two-phase loop is what proves you understood the paper. Enhancements are bolt-ons that mostly buy speed on giant instances we won't run anyway.

## 3. Architecture decision

- **C core (pure C):** I/O, instance model + distance access `d(i,j)`, S matrix (sorted sites per client via `qsort`), separation (`k̃_i`, OPT(SP_i), cut coefficients), Phase 1 loop, rounding, bounds bookkeeping, logging.
- **Solver abstraction layer (thin interface in C):** one internal API (`solver_init`, `solver_add_var`, `solver_add_constr`, `solver_set_lazy_callback`, `solver_optimize`, ...) with swappable backends:
  - **Gurobi** (primary — license available).
  - **CPLEX** (the solver the paper used; ideal for faithful comparison).
  - **Open backend** (SCIP or HiGHS) for license-free reproducibility.
  Backend chosen at build time (`make SOLVER=gurobi|cplex|scip`) and/or runtime flag. Satisfies "C mandatory": code is C; solver is a linked library. Phase 1 uses the LP; Phase 2 uses MIP + lazy-constraint callback.
- **Optional Python+Gurobi prototype:** readable callback reference + correctness oracle on toy/small instances + fast early results while C is built.

Why not pure C / no solver: Phase 2 needs a branch-and-cut tree. Writing B&B from scratch is out of scope and time. The solver provides the tree; we provide the cuts.

## 4. Repository structure

```
pmedian-benders/
├── README.md                 # ES: qué es, build, run, estado
├── PLAN.md                   # EN: this file (north star)
├── .gitignore
├── Makefile                  # build C, link Gurobi  (added Stage 5)
├── docs/
│   ├── PMEDIAN_BENDERS_PROJECT_BRIEF.md   # ES: full theory report
│   ├── entrega1_formulacion.md            # ES (folded into brief)
│   ├── entrega2_lagrangiana.md            # ES
│   ├── entrega3_benders.md                # ES
│   └── INSTANCE_FORMAT.md                 # ES: instance file spec
├── src/                      # C core
│   ├── main.c                # CLI: instance, p, --mode
│   ├── instance.{h,c}        # parse, store, d(i,j)
│   ├── sortsites.{h,c}       # build S matrix
│   ├── separation.{h,c}      # Alg 1 & 2: k̃_i, OPT, cut
│   ├── master.{h,c}          # Gurobi model build/manage
│   ├── phase1.{h,c}          # LP cut loop + rounding
│   ├── phase2.{h,c}          # branch-and-cut + lazy callback
│   ├── heuristic.{h,c}       # init + rounding
│   └── logging.{h,c}
├── prototype/                # optional Python+Gurobi oracle
│   └── pmp_benders.py
├── scripts/
│   ├── gen_rw.py             # random distance-matrix instances
│   ├── gen_birch.py          # clustered 2D instances
│   ├── parse_orlib.py        # OR-Library pmed → internal format
│   ├── parse_tsplib.py       # TSP-Library coords → internal format
│   └── run_benchmark.py      # batch runner → results CSV
├── instances/
│   ├── toy/                  # tiny hand-checkable
│   ├── orlib/
│   └── tsplib/
├── results/                  # CSVs + plots
└── tests/                    # C unit tests + pytest for prototype
```

## 5. Staged roadmap

Each stage: **Goal · Files · Test · Acceptance.**

**Stage 0 — Skeleton (THIS TURN, partial).**
Goal: repo bones + plan + README + toy instance + git.
Files: `PLAN.md`, `README.md`, `.gitignore`, `instances/toy/toy1.pmp`, `docs/INSTANCE_FORMAT.md`.
Test: `git status` clean; toy instance optimum known by hand (= 6).
Acceptance: repo opens, plan readable, toy documented.

**Stage 1 — Instance parser + distances.**
Goal: read instance, expose `d(i,j)`.
Files: `instance.{h,c}`, `main.c` (load + print summary).
Test: parse toy, print N,M,p and a few distances.
Acceptance: distances match hand values on toy.

**Stage 2 — Brute-force evaluator (oracle).**
Goal: given a set of open sites, compute objective directly.
Files: extend `instance.c` / small `eval.c`.
Test: enumerate all C(4,2) site pairs of toy → min = 6.
Acceptance: matches hand optimum; reused later to validate cuts.

**Stage 3 — S matrix.**
Goal: for each client, sites sorted by increasing distance.
Files: `sortsites.{h,c}`.
Test: toy S rows correct; complexity O(NM log M).
Acceptance: `S[i][r]` = r-th closest site to client i.

**Stage 4 — Separation (Alg 1 + 2).**
Goal: compute `k̃_i`, OPT(SP_i) (eq.18), cut (eq.20) for a given ȳ.
Files: `separation.{h,c}`.
Test: feed an integer ȳ; cut RHS equals true allocation distance; compare vs brute force on toy + a random small instance.
Acceptance: O(NM); cuts valid (never cut off the optimum).

**Stage 5 — Phase 1 (LP master + loop).**
Goal: build master in Gurobi, iterate solve→separate→add→round.
Files: `master.{h,c}`, `phase1.{h,c}`, `heuristic.{h,c}`, `Makefile`.
Test: toy and OR-Library pmed (e.g. pmed1) → LB1 = LP-relaxation bound; UB1 from rounding.
Acceptance: loop terminates (no violated cut); LB1 ≤ OPT; UB1 ≥ OPT.

**Stage 6 — Phase 2 (branch-and-Benders-cut).**
Goal: add integrality, lazy callback separates at integer nodes.
Files: `phase2.{h,c}`.
Test: OR-Library small/medium → gap 0%, value matches published OPT.
Acceptance: reaches optimum on OR-Library; `--mode` switch works.

**Stage 7 — Instances + benchmark runner.**
Goal: generators + parsers + batch runner → CSV (LB1, UB1, T1, gap, iter, nodes, Ttot).
Files: `scripts/*.py`.
Test: regenerate RW; parse a couple OR-Library + small TSP files.
Acceptance: CSV reproduces table-style rows on a chosen subset.

**Stage 8 — Preliminary analysis + report + benchmark vs. paper.**
Goal: plots (time vs N, gap vs p), short results discussion; finalize ES brief; **compare our LB1/UB1/gap/Ttot against the paper's published Tables 2–9** for the chosen subset and report deltas (and likely causes: machine, init heuristic, missing enhancements).
Files: `results/*`, `docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md`, `results/comparison_vs_paper.csv`.
Acceptance: numbers reproducible from CSV; per-instance delta table vs paper; report complete.

## 6. Execution order (staged, compressed — run in-session, not a multi-day calendar)

This is a **priority order**, not a calendar. We knock out stages back-to-back in working sessions. The report (Stage 0 + theory) ships first because understanding is the bottleneck.

1. **Stage 0 + theory report** — repo bones + full ES brief (F1→F4, Lagrangian, Benders, separation, Entregas 1–3). ✅ *(done)*
2. **Python prototype** — Phase 1 + Phase 2 on toy + OR-Library → first real results + callback learned + oracle ready.
3. **C Stages 1–4** — parser → distances → brute-force oracle → S matrix → separation (validated against prototype).
4. **C Stage 5** — Phase 1 (LP master + cut loop + rounding).
5. **C Stage 6** — Phase 2 (branch-and-Benders-cut, lazy callback).
6. **Stages 7–8** — instance gen + parsers + benchmark runner + plots + comparison vs. paper.

**Minimal viable deliverable (if time is cut):** Python Phase 1+2 results + C up to Phase 1 + full report + benchmark-vs-paper on a small subset. Phase 2 in C = stretch goal. This is still a strong, honest submission.

## 7. Open decision (blocking C code)
Confirm engine: **C core + Gurobi C API**. (Recommended.) Python prototype: keep or drop?
