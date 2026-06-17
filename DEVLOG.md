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

## 2026-06-17 — C Stages 1-4 DONE (instance, brute oracle, S matrix, separation)

- `src/instance.{h,c}`: parser (Variante A coords floored-euclid / Variante B matriz), d(i,j) as long, eval_open_set, brute_force (recursive C(M,p)).
- `src/sortsites.{h,c}`: matriz S (N*M) via qsort de pares (dist,site), empate estable. O(NM log M).
- `src/separation.{h,c}`: Alg.2 k̃_i en O(M), separation_client (ec.18 OPT + ec.20 cut), separation_all (Alg.1) con callback cut_sink.
- `tests/test_core.c` + `Makefile` (autodetecta Gurobi 12.0.0). `make test`.
- **toy1 PASS:** distancias a mano, brute opt=6, S[0]=[0,1,2,3], separacion(y*)=6, cortes no recortan el optimo.
- **rw12** (RW asimetrica generada, M=12): C brute opt=16 set{0,4,11} == prototype. separacion(y*)=16.
- **Cross-check separador C vs prototipo** (sum OPT en y=p/M uniforme), coincidencia exacta:
  toy=6.0, rw12=20.5, pmed1=7263.35. Confirma que el separador C reproduce el oraculo Python.
- `scripts/gen_rw.py`: generador RW (matriz aleatoria entera [1,n], asimetrica opc.).

**Next:** Stage 5 — solver layer (src/solver.h + solver_gurobi.c) + Phase 1 (LP master + cut loop + rounding) en C, validar LB1/UB1 en toy y pmed1 contra prototipo.

## 2026-06-17 — C Stages 5-6 DONE (solver layer + Phase 1 + Phase 2)

- `src/solver.{h,c=solver_gurobi.c}`: capa delgada (add_vars, add_constr, optimize, get_x, node_count, lazy callback). Backend Gurobi 12.0.0, firmas segun SOLVER_NOTES. `__stdcall grb_cb` -> on MIPSOL llama lazy_fn.
- `src/heuristic.{h,c}`: redondeo (abre p mayores y, evalua exacto).
- `src/phase1.{h,c}`: maestro LP (y in [0,1], theta>=0, sum y=p), loop separar/agregar/redondear. Devuelve LB1,UB1,iter,ncuts.
- `src/phase2.{h,c}`: maestro MIP (y binarias) + lazy callback que corre Alg.1 y agrega cortes (ec.20) con GRBcblazy.
- `src/logging.{h,c}`: wall_seconds + append a results/benchmark.csv.
- `src/main.c`: CLI `pmedian <inst> [--p P] [--mode phase1|full] [-v] [--opt V]`.
- Makefile: target `pmedian` (autolink Gurobi). Build limpio sin warnings.

**Resultados (todos OPTIMAL_MATCH vs optimo oficial):**
| inst | N | p | LB1 | UB1 | F2 opt | nodes |
|------|---|---|-----|-----|--------|-------|
| toy1 | 4 | 2 | 6 | 6 | 6 | 1 |
| rw12 | 12| 3 | 15 | 16 | 16 | 11 |
| pmed1|100| 5 | 5819| 5819| 5819 | 223 |
| pmed2|100|10 | 4088.5|4116| 4093 | 479 |
| pmed3|100|10 | 4240.5|4250| 4250 | 327 |
| pmed6|200| 5 | 7783.5|7867| 7824 | 632 |

Coincide con prototipo (rw12: LB1=15 UB1=16 en ambos). C reproduce el oraculo.

**Next:** Stages 7-8 — parsers TSP-Library + gen_birch, runner de benchmark, comparacion vs Tablas del paper, plots, finalizar brief.

## 2026-06-17 — C Stages 7-8 DONE (instances, benchmark, analysis) — CORE COMPLETE

- `scripts/parse_tsplib.py` (EUC_2D coords -> Variante A), `scripts/gen_birch.py` (clusters 2D), `scripts/run_benchmark.py` (runner -> benchmark.csv + comparison_vs_paper.csv), `scripts/plot_results.py` (3 figuras).
- **OR-Library pmed1-15** (N=100/200/300, p=5..100): Fase 2 = optimo oficial en las 15, delta=0. `results/comparison_vs_paper.csv`.
- **TSP-Library kroA100** (coords): C Fase 2 = prototipo F3 = 30539. Valida camino geometrico.
- Figuras: time_vs_N (todo <0.2s), gap1_vs_p (brecha F1 chica), nodes_vs_p.
- Brief: agregada seccion "11-bis Resultados de la replicacion" (resultados reales, hallazgo de aristas duplicadas, comparacion honesta vs paper con celdas NA por PDF ausente).
- `STATUS.md` escrito (handoff). README status table 0-8 = hecho.
- Cleanliness: `make clean && make pmedian` OK; pmedian/build/gurobi.log ignorados; sin artefactos staged.

**Core del paper replicado y validado.** Pendientes = enhancements (warm-start F2, RCF, constraint reduction, backend SCIP, instancias grandes) — document-only por Pareto cut.

## 2026-06-17 — Finishing pass

### Task 1: EDGE RULE justified + tested
- Copied paper PDF to docs/Benders_decom_pMedian.pdf.
- Found AUTHORITATIVE rule on OR-Library's own pmedinfo.html (Beasley): "Read each edge line IN TURN: set c(i,j)=k ... only the last such cost is used." Saved docs/orlib_pmed_format_spec.txt. Rule is independent of the 5819 target (it's the maintainer's documented Floyd-prep). Wrote docs/ADR/0002.
- tests/data/dup_edge.orlib (hand-made, KNOWN answer): last-wins => p-median p=1 = 13; min rule => 4. tests/test_parse_orlib.py PASS, discriminates the two rules. Does NOT depend on pmed1.
