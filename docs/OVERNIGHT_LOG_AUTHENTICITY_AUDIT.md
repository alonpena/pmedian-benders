# Overnight log authenticity audit

## Scope

Checked whether logs contain evidence of actual solver execution, not only fabricated CSV rows.

## Log signatures checked

Expected authentic signatures:

- command line or instance line;
- parsed instance dimensions `N`, `M`, `p`;
- Gurobi license/output lines or solver result line;
- Benders Phase 1 line for Benders runs;
- Benders Phase 2 + callback line for full Benders runs;
- monolithic result line for monolithic F1 runs.

## Findings

### Benders 300s logs

Branch: `exp/requirements-and-300s-benchmark`.

Sample `pmed1` log contains:

- `COMMAND: ./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819`
- `TIMEOUT_SECONDS: 300`
- `Instancia ... N=100 M=100 p=5`
- Gurobi license lines
- `[Fase 1] ...`
- `[Fase 2] ...`
- `[CALLBACK] warm_cuts=337 separaciones(MIPSOL)=3 cortes_lazy=90 nodos_B&B=1`

Verdict: authentic solver execution evidence.

### Real instance logs

Branch: `exp/large-instance-campaign`.

Sample `pmed1` log contains same wrapper metadata and Benders Phase 1/2/callback evidence.

Verdict: authentic solver execution evidence.

### Synthetic logs

Branch: `exp/synthetic-stress`.

Sample `euclidean_N100_p5pct` log contains:

- command line;
- `TIMEOUT_SECONDS: 300`;
- `Instancia ... N=100 M=100 p=5 (coords)`;
- Gurobi lines;
- Phase 1 and Phase 2 lines;
- callback proof line.

Verdict: authentic solver execution evidence.

### Monolithic F1 logs

Branch: `exp/monolithic-baselines`.

Sample `pmed1.log` contains:

- `Instancia instances/orlib/pmed1.pmp: N=100 M=100 p=5`
- Gurobi license lines
- `[MONOLITHIC_F1] status=OPTIMAL status_code=0 obj=5819.000000 ...`

Verdict: authentic solver execution evidence.

Caution: monolithic logs do not include wrapper metadata (`COMMAND`, `TIMEOUT_SECONDS`, `RETURNCODE`). Timeout enforcement is present in wrapper source and CSV, but future logs should include metadata for stronger forensic traceability.

### Gap trace logs

Branch: `exp/gap-trace-integration`.

Sample `pmed1_p5_phase1.log` contains:

- instance dimensions;
- Gurobi license lines;
- `[Fase 1] LB1=5819.0000 UB1=5819.0 iter=6 cuts=337 T1=...`

Verdict: authentic Phase 1 execution evidence.

## Suspicious items

No fabricated-row evidence found. Main weakness: monolithic logs are less verbose about wrapper timeout metadata.

## Verdict

Log authenticity audit passes with one caution about monolithic log metadata.
