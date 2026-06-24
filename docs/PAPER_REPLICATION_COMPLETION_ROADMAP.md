# Roadmap para replicación completa del paper

Objetivo: definir qué falta para pasar desde el estado actual (**núcleo algorítmico replicado + campaña parcial**) a una replicación computacional del paper Duran-Mateluna, Ales & Elloumi (2023) lo más cercana posible.

Regla: no fabricar evidencia. Si un comparador/dataset/código no se obtiene o no se ejecuta, queda `PAPER_REPORTED_ONLY`.

---

## 0. Estado actual resumido

| Área | Estado actual | Evidencia |
|---|---|---|
| Benders core F3/F4 lazy | Implementado | `src/phase1.c`, `src/phase2.c`, `src/separation.c` |
| Algoritmos 1–2 (`ktilde`, cortes) | Implementados y probados | `tests/test_separation_toy.c`, `scripts/verify_cuts.py` |
| Phase 1 LP | Implementada, sin PopStar | `src/phase1.c` |
| Phase 2 branch-and-Benders-cut | Implementada con Gurobi lazy callback | `src/phase2.c`, `src/solver_gurobi.c` |
| Warm-start cortes Phase 1→2 | Implementado | `src/cutpool.c`, `results/warmstart_comparison.csv` |
| OR-Library `pmed1`–`pmed15` | Corrido local | `results/orlib_optima_check.csv` |
| `rl1304` Tabla 2 subset | Corrido local | `results/comparison_vs_paper.csv` |
| Zebra | No implementado / no corrido | sin binario/log/CSV |
| PopStar | No implementado | `src/heuristic.c` usa rounding |
| Constraint reduction | No implementado | sin código |
| Reduced-cost fixing | No implementado | sin código |
| CPLEX | No implementado | solo `src/solver_gurobi.c` |
| Tables 3–9 | No corridas | sin CSV/log |

Conclusión: proyecto actual es defendible para curso como **replicación algorítmica completa + replicación computacional parcial**. No es replicación completa del paper.

---

## 1. Definición de “replicación completa”

Para decir “replicación completa del paper” haría falta:

1. Implementar método central con mismas mejoras relevantes.
2. Ejecutar mismas familias de datos o subconjunto explícitamente equivalente.
3. Reproducir tablas principales del paper:
   - Table 1: F1/F2/F3/F4 formulation comparison.
   - Tables 2–5: TSPLIB small/medium/large/huge + Zebra comparisons.
   - Tables 6–7: BIRCH.
   - Table 8: RW.
   - Table 9: ODM.
   - UFL appendix si se quiere cobertura total.
4. Ejecutar comparadores o declarar imposibilidad:
   - Zebra.
   - PopStar.
   - AvellaB&C.
   - AvellaHeu.
   - IrawanHeu.
5. Usar o emular backend/ambiente del paper:
   - CPLEX 20.1 GenericCallback.
   - Time limits y parámetros paper.
   - Hardware benchmark normalization si se comparan tiempos.
6. Guardar evidencia reproducible:
   - instancias raw + checksums.
   - scripts exactos.
   - logs completos.
   - CSV limpios.
   - commit hash.

Sin Zebra/comparadores, máximo defendible: **replicación del método + reproducción parcial de resultados, con comparadores paper-only**.

---

## 2. Work packages

### WP0 — Congelar baseline reproducible

| Tarea | Entregable | Aceptación | Prioridad |
|---|---|---|---|
| Limpiar `results/benchmark.csv` append-only | CSV sin duplicados o `results/curated/*.csv` | no filas duplicadas por instancia/mode/p | CRITICAL |
| Crear manifiesto de resultados | `results/MANIFEST.md` | cada CSV/log tiene comando generador | CRITICAL |
| Congelar commit base | tag `replication-baseline-*` | `git status` limpio | CRITICAL |
| Separar resultados curados de scratch | `results/curated/`, `results/scratch/` | scripts no pisan curados | HIGH |
| Añadir script de deduplicación/validación | `scripts/validate_results.py` | falla si hay duplicados o missing logs | HIGH |

Notas:
- Antes de correr campañas grandes, resolver append-only/duplicates.
- Mantener `results/benchmark.csv` como scratch o hacerlo regenerable limpio.

---

### WP1 — Alinear implementación con paper algorithmic enhancements

| Tarea | Estado actual | Implementación requerida | Aceptación | Prioridad |
|---|---|---|---|---|
| PopStar initial solution | NOT_IMPLEMENTED | Obtener/implementar PopStar o wrapper reproducible | `UB1` comparable al paper; logs de `UB^h` | HIGH para 1:1 |
| Rounding heuristic | VERIFIED_LOCAL | Mantener | test unitario y log `UB1` | DONE |
| Constraint reduction | NOT_IMPLEMENTED | Al final Phase 1, conservar cortes hasta mayor índice saturado por cliente | reducción de cortes reportada, mismo óptimo | MEDIUM |
| Reduced-cost fixing | NOT_IMPLEMENTED | Leer reduced costs LP y fijar `y_j` si criterio paper aplica | número de variables fijadas logueado; no cambia óptimo | MEDIUM |
| Memory-reduced sorted `S` | PARTIAL | Paper sugiere `N x (M-p)`/reducciones; repo usa full `N x M` | memory profile antes/después | MEDIUM para large |
| CPLEX backend | NOT_IMPLEMENTED | `src/solver_cplex.c` con GenericCallback/lazy equivalent | compila y reproduce pmed1/rl1304 p5 | HIGH para timing paper |
| Time limit parameter | NOT_IMPLEMENTED | `--time-limit SEC` pasa a solver param | hard timeout local + solver status | HIGH |
| Solver status handling | PARTIAL | Registrar OPTIMAL/TL/MEM/GAP explícito | CSV status no ambiguo | HIGH |

Dependencias:
- RCF necesita acceso a reduced costs del LP final.
- Constraint reduction necesita metadata de cortes por cliente/radio.
- CPLEX requiere licencia/header.
- PopStar puede ser bloqueo por fuente/licencia.

---

### WP2 — Implementar modelos monolíticos para Table 1

| Modelo | Estado actual | Tarea | Aceptación |
|---|---|---|---|
| F1 | Branch-local/prototipo parcial | Implementar solver monolítico C/Gurobi/CPLEX para F1 | reproduce small cases, logs vars/constraints/time |
| F2 | No implementado | Implementar variables `z_i^k`, constraints `d<=D_i^k` | validates vs Benders on small cases |
| F3 | Solo Python oracle | Implementar monolítico sparse F3 | validates vs Benders on paper Table 1 subset |
| F4 all cuts upfront | No implementado upfront | Implementar all-cuts compact model | validates vs lazy Benders on small cases |

Table 1 target:
- OR-Library `pmed26`, `pmed31`, `pmed35`, `pmed38`, `pmed39`, `pmed40`.
- Paper time limit: 600s.
- Need raw instances `pmed26/31/35/38/39/40` in repo or downloader.

Acceptance:
- CSV: `results/table1_formulations.csv`.
- Columns: `instance,N,p,formulation,nvars,nconstr,nnz,status,obj,best_bound,gap,time_s,nodes,solver`.
- If hardware differs, times marked machine-dependent.

Priority: MEDIUM for full paper, LOW for course.

---

### WP3 — Data acquisition and provenance

| Dataset | Needed | Current | Tasks | Acceptance |
|---|---|---|---|---|
| OR-Library pmed1–40 | pmed raw files + optima | pmed1–15 in `instances/`; evidence pmed17–40 archived but raw missing | Add downloader/checksums for pmed1–40 | `instances/orlib/pmed1..40.txt/.pmp`, checksum manifest |
| TSPLIB small | `rl1304`, `fl1400`, `u1432`, `vm1748` | raw files exist for some; `.pmp` only `rl1304` grid and `kroA100` | Generate all paper p-values | `instances/tsplib/<name>_p<p>.pmp` |
| TSPLIB medium/large/huge | paper Tables 3–5 | mostly absent | Acquire TSPLIB coords, convert, check memory | manifest + generated `.pmp` or streaming support |
| BIRCH | paper data | only synthetic generator | Locate exact paper/Avella/Irawan BIRCH data or recreate with documented generator if paper allows | provenance doc; no claim if not exact |
| RW | paper random matrices | only `rw12` | Implement generator matching Resende/Werneck seeds/specs or obtain files | reproducible seeds + matrices |
| ODM | BD3773 with forbidden assignments | absent | Add parser/model support for forbidden assignments | small ODM validation + BD3773 run |
| UFL/KG | Appendix | absent | Add UFL parser/model extension | optional appendix replication |

Priority:
- OR-Library/TSPLIB small: HIGH.
- TSPLIB large/huge: MEDIUM/HIGH if hardware available.
- BIRCH/RW/ODM: MEDIUM.
- UFL: LOW.

---

### WP4 — Full Benders campaign runner

Current `scripts/run_benchmark.py` only OR-Library and appends. Need paper-grade runner.

Tasks:

1. Create `scripts/run_paper_campaign.py`.
2. Support manifest-driven experiments:
   ```yaml
   table: 2
   family: TSPLIB-small
   instance: rl1304
   p: 5
   opt: 3099073
   time_limit: 300
   method: benders
   solver: gurobi
   ```
3. Enforce per-run time limit.
4. Capture stdout/stderr/log path.
5. Write one row per run, no append duplicates unless `run_id` differs.
6. Store solver status, gap, objective, best bound, nodes, cuts, warm cuts, memory if possible.
7. Refuse to overwrite curated results unless `--force`.

Acceptance:
- `results/paper_campaign_runs.csv` clean primary key: `(table,family,instance,p,method,solver,run_id)`.
- `results/logs/paper_campaign/<run_id>.log` exists for each row.
- Validation script passes.

Priority: CRITICAL before serious replication.

---

### WP5 — Reproduce Table 2 fully

Paper Table 2 small TSP includes more than `rl1304`:
- `rl1304`
- `fl1400`
- `u1432`
- `vm1748`

Tasks:
1. Transcribe Table 2 values with source line/page reference.
2. Generate `.pmp` for all paper p-values.
3. Run Benders with paper-like time limit.
4. Store `results/table2_tsp_small.csv`.
5. Compare OPT/LB1/UB1/gap; mark times machine-dependent.
6. Zebra columns: only local if Zebra actually runs; otherwise paper-only columns separated.

Acceptance:
- All local Benders rows have logs.
- `delta_OPT=0` or documented mismatch with diagnosis.
- No local Zebra claim unless Zebra run evidence exists.

Priority: HIGH.

---

### WP6 — Reproduce Tables 3–5 TSPLIB medium/large/huge

Tasks:
1. Acquire exact TSPLIB instances.
2. Check memory of full `S` (`N*M*sizeof(int+long)`): likely bottleneck huge.
3. Implement memory-reduced or streaming separation if needed.
4. Run with time limit matching paper.
5. Store separate CSVs:
   - `results/table3_tsp_medium.csv`
   - `results/table4_tsp_large.csv`
   - `results/table5_tsp_huge.csv`
6. Record failures as `TIME_LIMIT`, `MEMORY_LIMIT`, `NOT_RUN`, not blank.

Acceptance:
- At least exact `OPT` matches for solved instances.
- For failures, logs prove status.
- Hardware/memory documented.

Priority: MEDIUM/HIGH. Risk: high hardware/memory.

---

### WP7 — Reproduce BIRCH Tables 6–7

Tasks:
1. Determine exact BIRCH source used by paper.
2. If unavailable, do not call synthetic generator “paper BIRCH”. Use “BIRCH-like synthetic”.
3. Implement/import exact instances or exact generator + seeds.
4. Run local Benders.
5. Comparator AvellaHeu/IrawanHeu: obtain code/data or mark paper-only.

Acceptance:
- `results/table6_birch.csv`, `results/table7_birch_large.csv`.
- Provenance doc proves exact or labels approximate.

Priority: MEDIUM.

---

### WP8 — Reproduce RW Table 8

Tasks:
1. Implement RW generator exactly per Resende & Werneck spec:
   - integer uniform `[1,n]`
   - symmetric/asymmetric as paper
   - seeds/p-values paper.
2. Add seed manifest.
3. Run Benders.
4. PopStar comparator: only if PopStar implemented/obtained.

Acceptance:
- `results/table8_rw.csv`.
- Each row has seed + matrix checksum.
- If no PopStar, comparator paper-only.

Priority: MEDIUM.

---

### WP9 — Implement ODM Table 9 support

Current solver assumes every client can assign to every site. ODM has forbidden assignments.

Tasks:
1. Extend instance format for forbidden pairs or infinite distances.
2. Check whether closed-form Benders cut remains valid with forbidden assignments; adapt if paper specifies.
3. Add parser for BD3773.
4. Validate on tiny ODM toy.
5. Run BD3773.

Acceptance:
- Toy ODM exact validation.
- `results/table9_odm.csv`.

Priority: LOW/MEDIUM. Risk: model change.

---

### WP10 — Comparator replication

| Comparator | Task | Risk | Fallback |
|---|---|---|---|
| Zebra | Find official/source, build, validate on small pMP, run same instances | Very high: source/provenance/build risk | Paper-only claim |
| PopStar | Obtain source or implement algorithm | Medium/high | Keep rounding and say no PopStar |
| AvellaB&C | Obtain exact code or published executable | High | Paper-only |
| AvellaHeu | Obtain/implement | High | Paper-only |
| IrawanHeu | Obtain/implement | High | Paper-only |

Acceptance for any comparator:
- source/provenance documented.
- command line reproducible.
- logs per run.
- same data and time limit.

No source = no local comparator claim.

Priority: HIGH only if objective is true paper benchmark replication. For course: NOT_REQUIRED.

---

### WP11 — Report and slides after extended replication

Tasks:
1. Add “Replication levels” section:
   - algorithmic exact.
   - computational subset.
   - comparator literature-only.
2. For each table, state status:
   - reproduced locally.
   - partially reproduced.
   - paper-only.
3. Add trace footnote per table: source CSV/log.
4. Separate local timing vs paper timing.
5. Never combine local Benders times with paper Zebra times as if same experiment unless normalized and clearly labeled.

Acceptance:
- Every numeric claim has row in `docs/RESULTS_TRACEABILITY.md` or successor.
- Grep for forbidden phrases passes:
  - “we outperform Zebra” absent.
  - “full replication” absent unless actually complete.

Priority: CRITICAL for final defense.

---

## 3. Suggested timeline

### Track A — Course-safe final (1–2 days)

Goal: clean and defensible submission, not full paper replication.

1. Clean dirty results / dedupe benchmark.
2. Freeze current evidence.
3. Ensure report says partial computational replication.
4. Compile Overleaf.
5. Prepare defense around current facts.

Deliverable: ready course submission.

### Track B — Strong partial paper replication (1–2 weeks)

Goal: extend local evidence without impossible comparators.

1. Build manifest-driven runner.
2. Add OR-Library pmed1–40 raw instances + checksums.
3. Reproduce full OR-Library known optima.
4. Reproduce Table 2 all small TSPLIB instances with Benders only.
5. Add clean CSVs and logs.
6. Keep Zebra paper-only.

Deliverable: stronger replication report, still honest.

### Track C — Near-complete algorithmic+experimental replication (3–6 weeks)

Goal: most paper tables, local Benders only.

1. Implement missing enhancements: PopStar, RCF, constraint reduction.
2. Implement time-limit/status/memory logging.
3. Acquire/run TSPLIB medium/large, BIRCH, RW, ODM if feasible.
4. Add exact data provenance.
5. Compare local Benders to paper Benders results; comparators still paper-only unless obtained.

Deliverable: near-complete paper method replication.

### Track D — True 1:1 paper benchmark replication (unknown, high risk)

Goal: reproduce paper tables including comparators.

1. Obtain Zebra and heuristic comparator implementations.
2. Build/test each comparator.
3. Run same datasets/time limits.
4. Reproduce hardware normalization or run all methods on same machine.
5. Publish complete comparison tables.

Blocker: comparator source/provenance may be unavailable. If unavailable, true 1:1 replication impossible.

---

## 4. Critical path

```text
Clean results state
  -> manifest-driven runner
  -> data provenance + checksums
  -> missing algorithmic enhancements
  -> Table 2 full local Benders
  -> Tables 3–9 local Benders
  -> comparator acquisition
  -> final report tables
```

Immediate next tasks if continuing now:

1. Add `scripts/validate_results.py` to catch duplicate rows and missing logs.
2. Create `results/curated/` and move final CSVs there.
3. Create `experiments/paper_campaign.yaml` manifest.
4. Implement `--time-limit` in CLI/solver wrapper.
5. Extend Table 2 beyond `rl1304`.

---

## 5. Stop/go decision gates

| Gate | Question | Go if | Stop/fallback if |
|---|---|---|---|
| G1 | Need course delivery only? | current evidence enough after cleanup | do not chase Zebra |
| G2 | Need full paper tables? | data available + hardware enough | report subset only |
| G3 | Need Zebra claim? | Zebra source builds and runs locally | cite paper only |
| G4 | Need timing comparison? | same solver/hardware or normalized protocol | compare objectives/gaps only |
| G5 | Need huge instances? | memory-reduced S implemented or large RAM available | mark NOT_RUN |

---

## 6. Final rule for defense

Until WP10 is complete, this sentence remains mandatory:

> Zebra no fue reejecutado localmente. La comparación contra Zebra es un resultado reportado por el paper, no un resultado experimental de este repositorio.
