# Project requirements

## 1. Academic objective

Build a defensible computational optimization project for PUCV Optimización Computacional. Evidence must be reproducible from repository commands, CSV files, logs, and tests.

## 2. Paper objective and what is being replicated

Target paper: Duran-Mateluna, Ales & Elloumi (2023), “An efficient Benders decomposition for the p-median problem”.

Project objective: progressively approach a rigorous replication of the paper. Current local work is a partial but evidence-backed replication of the central Benders decomposition method; missing paper components are roadmap items, not permanent exclusions.

Replicated locally in current audited state:

- p-median Benders master with `y_j` and `theta_i`.
- Phase 1 LP relaxation with cut generation.
- Phase 2 binary branch-and-Benders-cut with lazy callbacks.
- Closed-form separation using sorted sites and `ktilde_i`.
- Selected benchmark subsets with CSV/log traceability.

## 3. Course alignment

Required course dimensions:

- Formulation: p-median model and F3-derived Benders reformulation.
- Structure: master/subproblem decomposition and customer-wise separability.
- Cotas: Phase 1 lower/upper bounds and final optimality evidence.
- Benders: optimality cuts, lazy constraints, and callback proof.
- Computational results: curated benchmark CSVs, logs, and plots only from local runs.

## 4. Current verified state

Implemented in C with Gurobi backend:

- Instance parser for internal `.pmp` coordinate/matrix format.
- Distance oracle and sorted-site structures.
- Separation routine for violated Benders optimality cuts.
- Phase 1 LP master, rounding upper bound, cut pool.
- Phase 2 MIP master with Gurobi lazy callbacks.
- Warm-start from Phase 1 cuts.
- CSV/log utilities.

Locally verified experiments:

- `toy1`.
- OR-Library `pmed1`–`pmed15`.
- TSPLIB `rl1304` Table 2 subset.
- TSPLIB `kroA100`.
- Warm/cold comparison.
- Separator tests.
- Branch-local external 300-second Benders campaign when `results/benders_300s_campaign.csv` and `results/logs/benders_300s/*.log` are present.

Current audited missing/not-yet-run components:

- Zebra.
- PopStar.
- Constraint reduction.
- Reduced-cost fixing.
- Monolithic C benchmark.
- Large/huge TSPLIB campaigns.
- BIRCH campaign.
- RW large campaign.
- ODM campaign.

## 5. Target replication roadmap

The project goal is not merely to document limitations. The goal is to progressively approach rigorous replication of Duran-Mateluna, Ales & Elloumi (2023).

Future experimental branches may implement or run:

- External 300-second benchmark campaign.
- Monolithic F1 baseline in C.
- Potentially F3/F4 monolithic baseline if feasible.
- Larger OR-Library and TSPLIB campaigns.
- Synthetic stress tests.
- Gap trace logging.
- PopStar or alternative warm-start heuristic if time allows.
- Zebra only if source/build is available and reproducible.

## 6. Branch policy

Experimental implementations should happen in separate branches:

- `exp/monolithic-baselines`
- `exp/large-instance-campaign`
- `exp/synthetic-stress`
- `exp/gap-logging`
- `exp/popstar-or-warmstart`
- `exp/zebra-comparison` only if Zebra source/build is available

## 7. Required experimental protocol

- Do not modify the mathematical Benders core for benchmark bookkeeping.
- Use separate experiment branches.
- Do not overwrite curated CSVs without backup.
- Any result described as 300 seconds / 5 minutes must be produced by an external wrapper using `subprocess.run(..., timeout=300)`.
- Store numerical results in `results/*.csv`.
- Store raw command output in `results/logs/*.log` or experiment-specific log subdirectories.
- Treat Zebra comparisons as paper-reported only unless Zebra is implemented or run locally.
- Missing components are not forbidden; they require implementation/run evidence before claims.

## 8. Required metrics

For Benders campaigns, collect when available:

- `family`
- `instance`
- `N`
- `p`
- command
- solver status
- timeout flag
- objective value
- `LB1`
- `UB1`
- final gap
- `T1`
- `T2`
- total wall time
- Phase 1 iterations
- branch-and-bound nodes
- lazy cuts
- separation calls
- known-optimum match flag
- optimum delta
- raw log path

Unavailable fields must be recorded as `NA`, never fabricated.

## 9. Required plots

Expected figure outputs for report use:

- gap vs time
- gap vs iteration
- runtime vs `N`
- nodes vs `N`
- cuts vs `N`
- monolithic vs Benders runtime, only after monolithic baseline exists
- warm vs cold nodes

Plots must be generated from CSV evidence only.

## 10. Required caveats

Mandatory caveats for current audited state:

- Current local state is a partial replication of the paper’s core Benders method.
- Hardware, solver, and initialization differ from the paper.
- Runtime comparisons against the paper are machine-dependent.
- Zebra has not yet been rerun locally.
- PopStar and reduction techniques are not yet implemented.
- Large/huge benchmark families remain roadmap items until CSV/log evidence is added.
- Future branches may remove these limitations if implementation/run evidence is committed.

## 11. Claim discipline and forbidden claims

Do not claim any roadmap item as completed unless there is code plus CSV/log/test evidence.

Forbidden until supported by new evidence:

- “We outperform Zebra.”
- “We replicated the full paper.”
- “We implemented PopStar.”
- “We implemented reduced-cost fixing.”
- “We implemented constraint reduction.”
- “We compared against a monolithic C baseline.”
- “We ran BIRCH, ODM, RW large, or huge TSPLIB.”
- “The 5-minute protocol was used” for any row not produced by a 300-second timeout wrapper.

## 12. Immediate priority

Current task: make the current Benders results defensible under the professor’s 5-minute protocol using an external 300-second wrapper, `results/*.csv`, and raw logs. This does not replace future monolithic baseline work, large-instance campaigns, synthetic stress tests, gap trace logging, PopStar/warm-start work, or Zebra comparison if reproducible source/build becomes available.
