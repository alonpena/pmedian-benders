# Project requirements

## 1. Academic objective

Build a defensible computational optimization project for PUCV Optimización Computacional. Evidence must be reproducible from repository commands, CSV files, logs, and tests.

## 2. Paper objective and what is being replicated

Target paper: Duran-Mateluna, Ales & Elloumi (2023), “An efficient Benders decomposition for the p-median problem”.

Local objective: rigorous partial replication of the central Benders decomposition method, not full reproduction of every benchmark table or competing method.

Replicated locally:

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

## 4. Implemented core

Implemented in C with Gurobi backend:

- Instance parser for internal `.pmp` coordinate/matrix format.
- Distance oracle and sorted-site structures.
- Separation routine for violated Benders optimality cuts.
- Phase 1 LP master, rounding upper bound, cut pool.
- Phase 2 MIP master with Gurobi lazy callbacks.
- Warm-start from Phase 1 cuts.
- CSV/log utilities.

## 5. Missing paper components

Not implemented or not run locally:

- Zebra.
- PopStar.
- Constraint reduction.
- Reduced-cost fixing.
- Monolithic C benchmark.
- BIRCH campaign.
- RW large campaign.
- ODM campaign.
- Huge TSPLIB campaign.

## 6. Required experimental protocol

- Do not modify the mathematical Benders core for benchmark bookkeeping.
- Use separate experiment branches.
- Do not overwrite curated CSVs without backup.
- Any result described as 300 seconds / 5 minutes must be produced by an external wrapper using `subprocess.run(..., timeout=300)`.
- Store numerical results in `results/*.csv`.
- Store raw command output in `results/logs/*.log` or experiment-specific log subdirectories.
- Treat Zebra comparisons as paper-reported only unless Zebra is implemented or run locally.

## 7. Required metrics

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

## 8. Required plots

Expected figure outputs for report use:

- gap vs time
- gap vs iteration
- runtime vs `N`
- nodes vs `N`
- cuts vs `N`
- monolithic vs Benders runtime, only after monolithic baseline exists
- warm vs cold nodes

Plots must be generated from CSV evidence only.

## 9. Required caveats

Mandatory caveats:

- This project is a partial local replication of the paper’s core method.
- Hardware, solver, and initialization differ from the paper.
- Runtime comparisons against the paper are machine-dependent.
- Zebra was not rerun locally.
- PopStar and reduction techniques are not implemented.
- Large/huge benchmark families remain out of local scope unless new CSV/log evidence is added.

## 10. Forbidden claims

Forbidden unless new evidence is committed:

- “We outperform Zebra.”
- “We replicated the full paper.”
- “We implemented PopStar.”
- “We implemented reduced-cost fixing.”
- “We implemented constraint reduction.”
- “We compared against a monolithic C baseline.”
- “We ran BIRCH, ODM, RW large, or huge TSPLIB.”
- “The 5-minute protocol was used” for any row not produced by a 300-second timeout wrapper.
