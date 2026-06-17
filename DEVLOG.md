# DEVLOG — pmedian-benders

Append-only. Timestamps in local time (America/Santiago). Newest entries at bottom.

---

## 2026-06-17 — Stage 0.5: kickoff, environment, solver notes

**Plan of attack (5 lines):**
1. Unpack provided zips into repo, reorganize to PLAN.md layout (docs/, src/, instances/toy/, ...), `git init`.
2. Verify toolchain + Gurobi license; document real header signatures in `docs/SOLVER_NOTES.md`.
3. Build Python+Gurobi prototype (F3 + Phase 1 + Phase 2 lazy callback); validate toy (opt=6) + 1 OR-Library instance → first real numbers + oracle.
4. C Stages 1–4: instance/distances → brute-force oracle → S matrix → separation (Alg 1&2), cross-checked vs prototype.
5. C Stages 5–6: Phase 1 (LP master + cut loop + rounding), Phase 2 (lazy callback). Then Stages 7–8 instances/benchmark/report.

**Done:**
- Reorganized flat dump into PLAN structure. `git init`. Created docs/ADR, src, prototype, scripts, instances/{toy,orlib,tsplib}, results/logs, tests.
- Toolchain: Apple clang 21.0.0, GNU Make 3.81, Python 3.14.5, git 2.38.0. All present.
- Gurobi: three installs in `/Library/` (10.0.1, 11.0.2, 12.0.0). Using **12.0.0**. License `/Users/apena/gurobi.lic` academic, expires 2027-06-15. Verified: trivial C model (`/tmp/gtest.c`) compiles `-lgurobi120` and solves (objval=10). gurobipy in `.venv` also solves OK.
- Wrote `docs/SOLVER_NOTES.md` from the **installed** `gurobi_c.h`: exact signatures for env/model/var/constr/attr/param + callback flow (`CB_ARGS`, `GRB_CB_MIPSOL=4`, `GRB_CB_MIPSOL_SOL=4001`, `GRBcblazy`, `LazyConstraints` param). CPLEX header absent → CPLEX backend deferred.
- `.venv` created; installed gurobipy + numpy.

**Decisions / ASSUMPTIONs:**
- ASSUMPTION: keep the Python prototype (PLAN §7 open question). It is the correctness oracle and callback reference; low cost, high value. Logged here as confirmed.
- ASSUMPTION: default+only verified backend = Gurobi 12.0.0. SCIP/HiGHS open backend deferred (document-only) unless time permits; solver layer kept thin so it can be added.
- Distances: Euclidean **floored** (paper convention) for coord instances; integer matrix for RW. Store integer distances as `long`, accumulate objective as `double`.

**Next:** build `prototype/pmp_benders.py` (F3 ref + Phase 1 + Phase 2), validate toy=6.

## 2026-06-17 — Stage: Python prototype (oracle) DONE

- Wrote `prototype/pmp_benders.py`: instance parser (A/B), d(i,j) floored euclid, S matrix, separation O(NM) (Alg.2 k̃_i, ec.18, ec.20 cut), F3 reference oracle, brute force, Phase 1 (LP master + cut loop + rounding), Phase 2 (lazy callback branch-and-Benders-cut).
- Validated **toy1**: brute=6, F3=6, Phase1 LB1=UB1=6 (iter=3), Phase2=6. All agree with hand optimum.
- Wrote `scripts/parse_orlib.py` (graph -> all-pairs shortest path -> Variante B matrix).
- Fetched OR-Library **pmed1** from `https://www.brunel.ac.uk/~mastjjb/jeb/orlib/files/pmed1.txt` (brunel `people.brunel` host now 404s; `www.brunel` works).
- **Bug found + fixed (duplicate edges):** pmed1 has 2 parallel edges with differing costs ({19,20}=[22,30], {30,70}=[5,74]). Taking the *min* (natural for shortest path) gave optimum 5718; OR-Library's official `pmedopt.txt` says **5819**. Local-search test confirmed: min->5718, max/last-wins->5819. OR-Library convention = **last occurrence overwrites**. Fixed parser to overwrite. Verified Dijkstra==Floyd-Warshall on the matrix (two independent SP algos) before concluding the issue was edge-merge policy, not SP.
- After fix, **pmed1**: F3=5819, Phase1 LB1=UB1=5819 (iter=6), Phase2=5819 cuts=582 nodes=471. Matches official optimum.

ASSUMPTION: OR-Library duplicate-edge policy = last-occurrence-wins (documented in parser). Holds for pmed1; will spot-check other pmed files when used.

**Next:** C Stages 1-4 (instance/distances, brute-force oracle, S matrix, separation), cross-checked vs this prototype.
