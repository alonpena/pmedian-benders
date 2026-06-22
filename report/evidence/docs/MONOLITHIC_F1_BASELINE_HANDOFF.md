# Monolithic F1 baseline handoff

## Phase

FASE 3 — Monolithic F1 baseline.

## Branch

- `exp/monolithic-baselines`
- Base for branch: `1de348e`
- Restore-point/code commit before campaign: `92381db`

## Implementation

Added experimental CLI mode:

```bash
./pmedian <instance.pmp> --mode monolithic-f1
```

Files:

- `src/monolithic_f1.h`
- `src/monolithic_f1.c`
- `src/main.c`
- `Makefile`
- `scripts/run_monolithic_f1_300s.py`

## Formulation

Implemented classical strong F1-style monolithic p-median baseline:

- `y_j` binary, one per candidate facility.
- `x_ij` continuous in `[0,1]`, one per client/facility assignment.
- Objective: `min sum_i sum_j d_ij x_ij`.
- Cardinality: `sum_j y_j = p`.
- Assignment: `sum_j x_ij = 1` for every client `i`.
- Linking: `x_ij <= y_j` for every pair `(i,j)`.

No F3/F4 monolithic model was implemented.

## Campaign command

```bash
make clean && make
python3 scripts/run_monolithic_f1_300s.py
make clean && make && make test
```

Wrapper uses `subprocess.run(..., timeout=300)` per instance.

## Outputs

CSV:

- `results/monolithic_f1_300s.csv`

Logs:

- `results/logs/monolithic_f1/toy1.log`
- `results/logs/monolithic_f1/pmed1.log`
- `results/logs/monolithic_f1/pmed2.log`
- `results/logs/monolithic_f1/pmed6.log`
- `results/logs/monolithic_f1/kroA100.log`

## CSV schema

`instance,N,p,status,obj,gap,runtime,nodes,model_vars,model_cons,model_nnz,timeout_flag,log_path`

## Results summary

| instance | N | p | status | obj | gap | runtime | nodes | vars | cons | nnz | timeout |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| toy1 | 4 | 2 | OPTIMAL | 6 | 0 | 0.024817 | 1 | 20 | 21 | 52 | 0 |
| pmed1 | 100 | 5 | OPTIMAL | 5819 | 0 | 0.436110 | 1 | 10100 | 10101 | 30100 | 0 |
| pmed2 | 100 | 10 | OPTIMAL | 4093 | 0 | 0.441374 | 1 | 10100 | 10101 | 30100 | 0 |
| pmed6 | 200 | 5 | OPTIMAL | 7824 | 0 | 6.991906 | 1 | 40200 | 40201 | 120200 | 0 |
| kroA100 | 100 | 10 | OPTIMAL | 30539 | 0 | 0.461514 | 1 | 10100 | 10101 | 30100 | 0 |

## Compile/test result

Passed after implementation and after campaign:

```bash
make clean && make && make test
```

Both tests printed `RESULT: PASS`.

## Defensible claims

- A local monolithic F1 baseline exists and solves the five listed small/medium instances with external 300-second timeout.
- The F1 baseline matches Benders objective values for the overlapping instances in existing Benders CSV (`toy1`, `pmed1`, `pmed2`, `pmed6`, `kroA100`).
- pmed6 is much larger in model size than pmed1/pmed2/kroA100 under F1 due to `N*M` assignment/linking terms.

## Claims not allowed

Do not claim:

- full paper replication;
- monolithic F3/F4 baseline;
- Zebra comparison;
- superiority of either method without Phase 4 joined plots/tables;
- scalability of monolithic F1 beyond these five rows;
- machine-independent runtime conclusions.

## Next step

FASE 4 can now compare `results/benders_300s_campaign.csv` against `results/monolithic_f1_300s.csv` for overlapping instances only.
