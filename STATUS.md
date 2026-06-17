# STATUS — pmedian-benders

_Snapshot: 2026-06-17. Sobrescrito en cada actualización._

## Estado global

**Núcleo completo y validado.** Etapas 0–8 implementadas. Fase 1 (LP + cortes +
redondeo) y Fase 2 (branch-and-Benders-cut con lazy callback) en C funcionan y
alcanzan el óptimo en todo el subconjunto probado. Prototipo Python = oráculo.

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
