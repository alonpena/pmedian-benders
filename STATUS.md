# STATUS — pmedian-benders

_Snapshot: 2026-06-17 (post finishing-pass). Sobrescrito en cada actualización._

## Estado global

**Núcleo completo y validado + finishing pass.** Etapas 0–8 + 6 tareas de cierre.
Fase 1 (LP + cortes + redondeo) y Fase 2 (branch-and-Benders-cut con lazy callback,
**confirmado**: pmed1 lazy_cuts=513, is_branch_and_benders_cut=YES) en C funcionan y
alcanzan el óptimo. Prototipo Python = oráculo. **Warm-start** (método del paper)
implementado, clean-start tras `--coldstart`. **Comparación vs paper Tabla 2 (rl1304):
9/9 OPT exactos.** Evidencia por afirmación en `docs/AUDIT.md`.

### Finishing pass (todo commiteado)
1. EDGE RULE: `docs/ADR/0002` + `docs/orlib_pmed_format_spec.txt` (regla del spec de Beasley) + `tests/test_parse_orlib.py` (instancia hecha a mano, NO pmed1).
2. CALLBACK PROOF: `results/logs/*.log` con separation_calls/lazy_cuts/nodes; WARN si cuts==0.
3. WARM-START: `src/cutpool.{h,c}`; `results/warmstart_comparison.csv` (nodos 632→7). Caveat wall-time en STATUS/AUDIT.
4. PAPER COMPARISON: `results/comparison_vs_paper.csv` (rl1304, 9/9 OPT match). OR-Library → `results/orlib_optima_check.csv` (no está en tablas del paper).
5. PLOTS: 4 PNGs solo de CSVs reales (`results/plot_a..d_*.png`).
6. SELF-AUDIT: `docs/AUDIT.md` (evidencia por afirmación, UNVERIFIED donde no hay artefacto).

> NOTA callback: lazy_cuts > 0 confirmado, NO degenera a B&B normal.

| Etapa | Estado |
|-------|--------|
| 0 esqueleto | ✅ |
| Prototipo Python (oráculo) | ✅ toy=6, pmed1=5819 |
| 1 parser + distancias | ✅ |
| 2 fuerza bruta (oráculo) | ✅ |
| 3 matriz S | ✅ |
| 4 separación O(NM) | ✅ cross-check vs prototipo |
| 5 Fase 1 (LP) | ✅ |
| 6 Fase 2 (B&Benders-cut) | ✅ pmed1–15 = óptimo oficial |
| 7 generadores + parsers + runner | ✅ orlib, tsplib, rw, birch |
| 8 análisis + plots + comparación | ✅ figuras + comparison CSV + brief |

## Cómo construir y ejecutar

```bash
export GUROBI_HOME=/Library/gurobi1200/macos_universal2
export DYLD_LIBRARY_PATH=$GUROBI_HOME/lib

make test                 # tests del núcleo (Etapas 1-4), toy opt=6
make pmedian              # binario principal (Gurobi autodetectado)

./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819
./pmedian instances/toy/toy1.pmp   --mode phase1 -v

# prototipo Python (oráculo)
.venv/bin/python prototype/pmp_benders.py instances/toy/toy1.pmp --mode all

# benchmark + comparación + plots
.venv/bin/python scripts/run_benchmark.py
.venv/bin/python scripts/plot_results.py
```

## Resultados clave

- 15/15 OR-Library pmed1–15: Fase 2 = óptimo oficial, delta 0. `results/comparison_vs_paper.csv`.
- kroA100 (TSP): C = prototipo F3 = 30539.
- `results/benchmark.csv`, `results/plot_*.png`.

## Próximos pasos (enhancements / si hay tiempo)

1. **Warm-start de Fase 2** con los cortes de Fase 1 (hoy Fase 2 parte limpia; correcto pero no aprovecha Fase 1).
2. **Reduced-cost fixing** y **constraint reduction** (brief 9.2) — document-only por ahora.
3. **Backend abierto** (SCIP/HiGHS) en `src/solver_scip.c` para repro sin licencia (interfaz ya aislada).
4. **Instancias grandes** (TSP >1000, BIRCH): activar `gen_birch.py` a escala; medir tiempo de construcción de S por separado (brief 7.8).
5. Transcribir Tablas 2–9 del paper si se obtiene el PDF (rellenar columnas `paper_*` en el comparison CSV).

## ASSUMPTIONs abiertas

- OR-Library aristas duplicadas = última-ocurrencia-gana (verificado en pmed1; spot-check al usar otras).
- Distancia euclidiana **floored** también para TSPLIB (canónico usa nint); elegida por consistencia con el paper.
- Backend único Gurobi 12.0.0; CPLEX no disponible (header ausente).

## Comando para retomar

```bash
cd /Users/apena/benders-pmedian && export DYLD_LIBRARY_PATH=/Library/gurobi1200/macos_universal2/lib
make pmedian && .venv/bin/python scripts/run_benchmark.py
```
