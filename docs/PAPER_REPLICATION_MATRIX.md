# Matriz de replicación del paper

> Paper: **Duran-Mateluna, Ales \& Elloumi (2023)**, *An efficient Benders decomposition for
> the p-median problem*, EJOR 308(1), 84–96.
> Solo evidencia. Sin fabricación. Estado: commit `cf021d6`, 2026-06-19.
> Entorno de las corridas: Apple M1, Gurobi 12.0.0, distancia euclidiana floor.

Leyenda: ✅ sí · 🟡 parcial · ❌ no.

---

## Tabla maestra

| # | Contribución científica | §Paper | ¿Implem.? | ¿Verif.? | Evidencia en código | Evidencia experimental | Evidencia faltante | Riesgo en defensa |
|---|---|---|---|---|---|---|---|---|
| 1 | Formulación **F3** (radios, igualdad) como base | 2 | ✅ | ✅ | maestro deriva de F3: `src/phase1.c`, `src/phase2.c` (vars $y$,$\theta$, $\sum y=p$); F3 oráculo `prototype/pmp_benders.py:solve_F3` | kroA100 C=oráculo F3=30539 (`docs/AUDIT.md` #10) | F3 entero no se pasa al solver (se usa su Benders) — por diseño | bajo |
| 2 | **Descomposición de Benders** (maestro $\theta_i$ + cortes) | 3 | ✅ | ✅ | `src/phase2.c` maestro + callback; corte ec.20 en `src/separation.c` | 15/15 OR-Library óptimo; 9/9 rl1304 (`results/comparison_vs_paper.csv`) | — | bajo |
| 3 | **Rutina de separación** (Alg. 1) | 3.3 | ✅ | ✅ | `separation_all` `src/separation.c:65` | `make test` PASS; verify 0 diffs | — | bajo |
| 4 | Cálculo de **$\tilde k_i$** (Alg. 2) | 3.3 | ✅ | ✅ | `separation_k_tilde` `src/separation.c:10` | test unitario toy1 ($\tilde k_2=2$) PASS | — | bajo |
| 5 | Separación **$O(NM)$ en forma cerrada** | 3.3 | ✅ | 🟡 | $\tilde k_i$ en $O(M)$ por cliente, sin LP (`src/separation.c`) | correcta a $N{=}1304$; complejidad **no medida** a gran escala | timing aislado de separación a $>10^4$ puntos | medio (afirmar complejidad, no escala) |
| 6 | **Fase 1**: LP maestro + loop de cortes (Alg. 3) | 3.5 | ✅ | ✅ | `phase1_run` `src/phase1.c:44`; redondeo `src/heuristic.c` | $LB_1$ coincide con paper en rl1304 ($\pm1$) | — | bajo |
| 7 | **Fase 2**: branch-and-Benders-cut (lazy) | 3.5 | ✅ | ✅ | `phase2_run`+`p2_lazy_fn` `src/phase2.c:36,85`; `GRBcblazy` | `results/logs/*.log`: `lazy_cuts=90/1850`, `is_branch_and_benders_cut=YES` | — | bajo |
| 8 | **Warm-start** = heredar cortes de Fase 1 | 3.5 | ✅ | ✅ | `phase2_run(...,const CutPool*warm)` precarga `src/phase2.c:64-77`; `cutpool_add` `src/phase1.c:39` | `results/warmstart_comparison.csv` (nodos 223→1, 632→7, 352→1) | ventaja en **wall-time** a gran escala no probada (mixto en sub-segundo) | bajo (reducción de nodos sólida; honesto en tiempo) |
| 9 | **Solo cortes de optimalidad** (SP siempre factible/acotado) | 3.2 | ✅ | ✅ | separador solo agrega cortes de optimalidad (sin rama de factibilidad) `src/separation.c`, `src/phase2.c` | gap 0 en todas las instancias cerradas; sin cortes de factibilidad jamás | argumento teórico (no medible) — soportado por terminación exacta | bajo |
| 10 | Experimentos **OR-Library** | 4 | ✅ | ✅ | runner `scripts/run_benchmark.py` | `results/orlib_optima_check.csv` 15/15 delta=0 | familias pmed16+ (N≥400) no corridas | bajo |
| 11 | **Comparación contra tablas del paper** | 4 (Tabla 2) | 🟡 | ✅ | `scripts/compare_paper.py` (Tabla 2 rl1304 transcrita) | `results/comparison_vs_paper.csv` 9/9 OPT, delta=0; $LB_1$ ±1 | Tablas 3–9 (TSP med/gr, BIRCH, RW, ODM) **no** transcritas ni corridas | medio (cobertura = 1 tabla de 8) |
| 12 | Superación a **Zebra** (orden de magnitud) | 4 | ❌ | ❌ | — (no se ejecuta Zebra) | tiempos de Zebra son del paper, no nuestros | corrida propia de Zebra | alto si se afirma como propio → **declarado UNVERIFIED** |
| 13 | **Reduced-cost fixing** | 3.5 | ❌ | n/a | ausente (grep `src/` sin coincidencias) | — | implementación + medición $p/M<20\%$ | bajo si se declara no implementado |
| 14 | **Constraint reduction** | 3.5 | ❌ | n/a | ausente (grep `src/` sin coincidencias) | — | implementación | bajo si se declara no implementado |
| 15 | Heurística inicial **PopStar** | 3.5 | ❌ (sustituida) | ✅ (sustituto) | redondeo uniforme reemplaza PopStar `src/heuristic.h:2` | $UB_1$ peor que paper donde paper usa PopStar (rl1304 p=10/100/300) — coherente | PopStar real | bajo (diferencia explicada: afecta $UB_1$, no $LB_1$) |
| 16 | Backend **CPLEX** (el del paper) | 4 | ❌ (Gurobi) | ✅ (Gurobi) | `src/solver_gurobi.c` (capa aislada `src/solver.h`) | resultados con Gurobi 12.0.0 | corrida con CPLEX | bajo |
| 17 | Instancias **gran escala** (TSP $>10^4$, BIRCH 89k, ODM) | 4 | ❌ | ❌ | núcleo soporta matriz/coords pero no se corrió | — | corridas a escala | medio (no afirmar escalabilidad como medida) |

---

## Verificación explícita (ítems pedidos)

- **F3 formulation** — ✅ implementada y verificada (oráculo F3 = C en kroA100=30539).
- **Benders decomposition** — ✅ maestro $\sum\theta_i$ + cortes; óptimo exacto en todo lo corrido.
- **Separation routine** — ✅ `separation_all`, verificada 3 vías (mano, test C, oráculo Python 0 diffs).
- **ktilde computation** — ✅ `separation_k_tilde`, test unitario exacto en toy1.
- **O(NM) separation** — ✅ implementada; 🟡 complejidad asintótica **no medida** a gran escala (correcta hasta N=1304).
- **Phase 1 LP cut loop** — ✅ `phase1_run`; $LB_1$ concuerda con paper.
- **Phase 2 branch-and-Benders-cut** — ✅ callback lazy real (`lazy_cuts>0`, `is_branch_and_benders_cut=YES`).
- **Warm-start inheritance** — ✅ herencia de cortes de Fase 1 (no preprocesamiento); reduce nodos drásticamente.
- **Optimality cuts only** — ✅ sin cortes de factibilidad jamás (SP siempre factible/acotado).
- **OR-Library experiments** — ✅ 15/15 al óptimo oficial, delta=0.
- **Comparison vs paper tables** — 🟡 solo Tabla 2 (rl1304), 9/9 OPT; Tablas 3–9 no.
- **Zebra status** — ❌ no ejecutado; tiempos del paper, declarados UNVERIFIED.
- **Reduced-cost fixing status** — ❌ no implementado (verificado por ausencia en `src/`).
- **Constraint reduction status** — ❌ no implementado (verificado por ausencia en `src/`).

---

## Síntesis de fidelidad

- **Núcleo del paper (ítems 1–10): replicado y verificado.** Es la contribución central
  (F3 → Benders → separación cerrada $O(NM)$ → dos fases → solo optimalidad).
- **Cobertura experimental: parcial honesta.** OR-Library completa + Tabla 2 del paper; el resto
  declarado no corrido.
- **Mejoras opcionales (RCF, constraint reduction, PopStar, CPLEX, gran escala): no implementadas**,
  verificado por ausencia en código, declarado en todos los documentos.
- **Riesgo de defensa mayor:** afirmar superación a Zebra o escalabilidad medida. Mitigado:
  ambos marcados UNVERIFIED en `docs/AUDIT.md` y aquí.
