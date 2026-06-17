# AUDIT — evidencia por afirmación

> Este documento es **evidencia para que el humano la lea**, no un veredicto.
> Cada afirmación lista el archivo que la prueba y el comando exacto para
> reproducirla. Lo que **no** se puede probar con un artefacto se marca
> `UNVERIFIED`. Prefijo de entorno en todos los comandos del binario:
> `export DYLD_LIBRARY_PATH=/Library/gurobi1200/macos_universal2/lib`

## Entorno
- Gurobi 12.0.0, licencia académica (expira 2027-06-15). Apple M1. Apple clang 21.
- Backend único Gurobi. CPLEX/SCIP: **no** usados.

---

## Afirmaciones VERIFICADAS

| # | Afirmación | Evidencia (archivo) | Comando para reproducir |
|---|-----------|---------------------|--------------------------|
| 1 | toy1 óptimo = 6 (a mano), núcleo C concuerda | salida de `make test` (`tests/test_core.c`) "RESULT: PASS", incluye "toy opt = 6" | `make test` |
| 2 | Separador C ≡ oráculo Python (suma OPT en y=p/M): toy 6.0, rw12 20.5, pmed1 7263.35 | DEVLOG 2026-06-17 (C Stages 1-4); línea `[xcheck]` de test_core | `./build/test_core instances/orlib/pmed1.pmp` y comparar con `prototype/pmp_benders.py` |
| 3 | OR-Library pmed1–15: Fase 2 = óptimo oficial, delta=0 (15/15) | `results/orlib_optima_check.csv` (col delta=0, status OPT_MATCH); `instances/orlib/pmedopt.txt` | `python scripts/run_benchmark.py $(for n in $(seq 1 15);do echo pmed$n;done)` |
| 4 | pmed1 = 5819 con regla de aristas correcta | `results/orlib_optima_check.csv` fila pmed1; `tests/test_parse_orlib.py` PASS | `python tests/test_parse_orlib.py` |
| 5 | Regla aristas duplicadas = última-gana, justificada por el spec (no por 5819) | `docs/orlib_pmed_format_spec.txt` (texto de Beasley); `docs/ADR/0002` | n/a (cita textual del spec) |
| 6 | Fase 2 ES branch-and-Benders-cut (cortes lazy reales) | `results/logs/pmed1.pmp_p5_full.log`: `lazy_cuts=513`, `is_branch_and_benders_cut=YES`, `separation_calls=...` | `./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819` |
| 7 | Warm-start reduce drásticamente nodos y cortes lazy | `results/warmstart_comparison.csv` (warm vs cold: pmed6 632→7 nodos) | `./pmedian instances/orlib/pmed6.pmp --mode full --opt 7824` y `... --coldstart` |
| 8 | Paper Tabla 2 (rl1304): 9/9 OPT coinciden, delta=0 | `results/comparison_vs_paper.csv` (col delta_OPT=0) | `python scripts/compare_paper.py` |
| 9 | El paper usa euclidiana FLOORED (no nint TSPLIB) | `results/comparison_vs_paper.csv` rl1304 p=5 our_opt=3099073=paper_OPT | `./pmedian instances/tsplib/rl1304_p5.pmp --mode full --opt 3099073` |
| 10 | kroA100 (TSP coords): C Fase 2 = oráculo F3 = 30539 | DEVLOG (Stages 7-8) | `./pmedian instances/tsplib/kroA100.pmp --mode full` vs `python prototype/pmp_benders.py instances/tsplib/kroA100.pmp --mode f3` |
| 11 | 4 figuras generadas solo de CSVs reales | `results/plot_a_bounds_orlib.png`, `plot_b_time_vs_N.png`, `plot_c_gap_vs_pM.png`, `plot_d_iter_nodes_vs_p.png` | `python scripts/plot_results.py` |
| 12 | Build limpio, sin warnings introducidos | salida de `make pmedian` (sin `warning:`) | `make clean && make pmedian` |
| 13 | our_LB1 ≈ paper_LB1 (Fase 1) en rl1304 | `results/comparison_vs_paper.csv` (paper_LB1 vs our_LB1, ±1) | `python scripts/compare_paper.py` |

---

## Afirmaciones UNVERIFIED (no probadas con artefacto en este repo)

- **UNVERIFIED — superación a Zebra "un orden de magnitud":** no ejecutamos Zebra.
  Los tiempos de Zebra en `comparison_vs_paper.csv`/Tabla 2 son del paper, no nuestros.
- **UNVERIFIED — ventaja en WALL-TIME del warm-start en general:** solo está probada la
  reducción de **nodos y cortes** (`warmstart_comparison.csv`). En instancias sub-segundo
  el wall-time es mixto (a veces warm es más lento por el preload). No se probó en
  instancias grandes donde se espera que el wall-time favorezca a warm.
- **UNVERIFIED — familias RW, BIRCH, ODM y TSP medianas/grandes/huge (Tablas 3–9):**
  no se corrieron. Solo Tabla 2 (small TSP, rl1304) y OR-Library (no tabulado en el paper).
- **UNVERIFIED — our_UB1 vs PopStar:** los UB1 del paper provienen de PopStar; nosotros
  usamos arranque uniforme + redondeo. La diferencia se observa pero no probamos PopStar.
- **UNVERIFIED — backend CPLEX (el del paper) y SCIP:** no compilados (header CPLEX ausente).
- **UNVERIFIED — escalabilidad O(NM) de la separación a gran escala:** la complejidad está
  implementada por diseño (Alg.2 en O(M)), pero no se midió el tiempo de separación aislado
  en instancias de >10^5 puntos.
- **UNVERIFIED — reduced-cost fixing y constraint reduction:** no implementados (document-only).

---

## Notas de honestidad
- Ningún número reportado fue inventado: todos provienen de corridas registradas en
  `results/` o de texto transcrito del PDF (`scripts/compare_paper.py`, trazable).
- Donde el paper reporta familias que no corrimos, las celdas quedan ausentes/UNVERIFIED,
  no rellenadas.
