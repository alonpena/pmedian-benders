# Autonomous experimental pipeline plan

## Scope

Produce reproducible experimental evidence for the p-median Benders replication. Do not write final academic narrative. Do not touch `main`. Do not modify verified Benders core unless a reproducible bug is documented.

## Global safeguards

- Start each phase by recording branch, commit, phase name, expected modified files, and expected outputs.
- Check for uncommitted work before every code-editing phase. Never mix unrelated experimental states.
- If context/memory usage indicator is unavailable, record that fact and continue only while visible context remains manageable.
- If context usage exceeds 70%, create `docs/HANDOFF_CONTEXT_<phase>.md`, commit completed work, and stop.
- If any phase fails due to compilation, tests, memory, missing instances, parse errors, or repeated build failures, create a failure handoff and stop.
- Long campaigns use external 300-second timeout wrappers. Runs expected over 30 minutes require `RUNNING_EXPERIMENT.md` before launch.
- For long-running experiments, commit wrapper/scripts first or create a restore-point commit before launch.
- At phase end, show `git status --short --branch`, `git log --oneline -5`, and `git diff --stat`.

## Phase 0: initial verification

Inputs read:

- `.skills.md`
- `docs/PROJECT_REQUIREMENTS.md`
- `docs/BENDERS_300S_CAMPAIGN.md`
- `results/benders_300s_campaign.csv`

Outputs:

- `docs/AUTONOMOUS_PIPELINE_PLAN.md`

No code changes.

## Phase 1: Benders 300s campaign visualizations

Branch: continue from current clean branch unless policy requires a plotting-only branch.

Create:

- `scripts/plot_benders_300s.py`
- `docs/BENDERS_300S_VISUALIZATION_HANDOFF.md`
- `results/figures/benders_300s_runtime_by_instance.png`
- `results/figures/benders_300s_nodes_by_instance.png`
- `results/figures/benders_300s_lazy_cuts_by_instance.png`
- `results/figures/benders_300s_runtime_vs_N.png`
- `results/figures/benders_300s_status_summary.png`

Data source: `results/benders_300s_campaign.csv`. Generate only feasible figures if columns are missing; document missing columns.

## Phase 2: gap trace logging

Branch: `exp/gap-trace-integration`.

Review before editing:

- `docs/dev_wip/gap_logging_wip.patch`
- `src/logging.h`
- `src/logging.c`

Goal: non-invasive Phase 1 trace logging with columns `iteration,elapsed_time,LB,UB,gap,cuts_added,total_cuts`.

Run:

- `make clean && make`
- `make test`
- small trace campaign: `toy1`, `pmed1`, `pmed6`, and `rl1304 p=5` only if quick.

Outputs:

- `results/gap_traces/*_phase1.csv`
- `results/figures/gap_vs_iteration_pmed1.png`
- `results/figures/bounds_vs_iteration_pmed1.png`
- `docs/GAP_TRACE_HANDOFF.md`

## Phase 3: monolithic F1 baseline

Branch from clean state: `exp/monolithic-baselines`.

Implement experimental mode `--mode monolithic-f1` without changing Benders core.

Formulation:

- binary `y_j`
- assignment `x_ij` continuous or binary per classical strong formulation
- objective `sum_i sum_j d_ij x_ij`
- `sum_j y_j = p`
- `sum_j x_ij = 1` for each customer
- `x_ij <= y_j`

Use external 300-second wrapper. Initial instances: `toy1`, `pmed1`, `pmed2`, `pmed6`, `kroA100` only if viable.

Outputs:

- `results/monolithic_f1_300s.csv`
- `results/logs/monolithic_f1/`
- `docs/MONOLITHIC_F1_BASELINE_HANDOFF.md`

Compile/test before commit.

## Phase 4: Benders vs Monolithic F1 plots

Only if Phase 3 CSV is valid.

Create:

- `scripts/plot_benders_vs_monolithic.py`
- `results/figures/benders_vs_monolithic_runtime.png`
- `results/figures/benders_vs_monolithic_gap.png`
- `results/figures/benders_vs_monolithic_nodes.png`
- `docs/BENDERS_VS_MONOLITHIC_HANDOFF.md`

## Phase 5: real paper-instance campaign inventory

Branch: `exp/large-instance-campaign`.

Create:

- `docs/PAPER_REPLICATION_MATRIX.md`

Inventory OR-Library `pmed1`–`pmed40`, available TSPLIB, BIRCH, RW, ODM. Classify as `READY`, `NEEDS_PREPROCESSING`, `NEEDS_DOWNLOAD`, `NOT_SUPPORTED`, or `TOO_LARGE_FOR_NOW`.

Run only READY instances with external 300-second timeout, priority OR-Library complete then TSPLIB small/medium. Do not run huge instances without memory confirmation.

Outputs:

- `results/benders_real_instances_300s.csv`
- `results/logs/real_instances_300s/`
- `docs/REAL_INSTANCE_CAMPAIGN_HANDOFF.md`

## Phase 6: synthetic stress test

Branch: `exp/synthetic-stress`.

Create:

- `scripts/gen_synthetic_euclidean.py`
- `scripts/run_synthetic_stress_300s.py`
- `instances/synthetic/`
- `results/synthetic_stress_300s.csv`
- `results/logs/synthetic_stress_300s/`
- `docs/SYNTHETIC_STRESS_HANDOFF.md`

Generate Euclidean instances for `N = 100, 250, 500, 1000, 2000, 5000`, `p = 5%, 10%, 20%`, fixed seed, floored Euclidean distances.

Figures:

- runtime vs `N`
- lazy cuts vs `N`
- nodes vs `N`
- timeout summary

## Phase 7: final experimental handoff

Branch: `exp/final-experimental-handoff`.

Create:

- `docs/EXPERIMENTAL_HANDOFF_FOR_REPORT.md`

Include implemented work, executed runs, compared models, replicated paper instances, exclusions, final tables, final figures, reproduction commands, permitted claims, forbidden claims, and report recommendations.

No final academic report narrative.
