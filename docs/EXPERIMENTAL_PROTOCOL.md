# Experimental protocol — pmedian-benders

Objetivo: reconstruir resultados defendibles sin fabricar evidencia y sin correr campaña enorme.

## 0. Reglas

1. No afirmar resultado si no queda en `results/*.csv` o `results/logs/*.log`.
2. `results/benchmark.csv` es append-only: para regenerar limpio, respaldar/borrar antes.
3. Zebra no se ejecuta: no hay protocolo local para Zebra.
4. No hay parámetro interno de time limit en `./pmedian`; usar wrapper externo si se requiere límite.
5. No correr large/huge TSP, BIRCH, RW grande u ODM salvo decisión explícita y tiempo disponible.

## 1. Entorno

```bash
make info
make clean && make
make test
.venv/bin/python scripts/verify_cuts.py
.venv/bin/python tests/test_parse_orlib.py
```

Esperado:

- Compilación sin warnings visibles.
- `make test`: `RESULT: PASS` en ambos tests.
- `verify_cuts.py`: `PASS`, 0 diffs.
- `test_parse_orlib.py`: `RESULT: PASS`.

## 2. Smoke tests obligatorios

```bash
./pmedian instances/toy/toy1.pmp --p 2 --mode full --opt 6
./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819
./pmedian instances/tsplib/kroA100.pmp --mode full
```

Esperado:

| Instancia | Esperado |
|---|---|
| toy1 | opt=6 |
| pmed1 | opt=5819, `OPTIMAL_MATCH`, lazy cuts > 0 |
| kroA100 | opt=30539, lazy cuts > 0 |

## 3. Time limit 300 s externo

El binario no implementa `--time-limit`. Usar Python wrapper:

```bash
.venv/bin/python - <<'PY'
import subprocess, os
cmd = ["./pmedian", "instances/orlib/pmed1.pmp", "--mode", "full", "--opt", "5819"]
env = dict(os.environ, DYLD_LIBRARY_PATH="/Library/gurobi1200/macos_universal2/lib")
subprocess.run(cmd, env=env, timeout=300, check=True)
PY
```

Para varias instancias, aplicar mismo wrapper por instancia. No mezclar timeouts con resultados de CSV sin documentar.

## 4. OR-Library benchmark defendible

Para regenerar OR-Library completo limpio:

```bash
mkdir -p results/archive
cp results/benchmark.csv results/archive/benchmark.before_orlib.csv 2>/dev/null || true
cp results/orlib_optima_check.csv results/archive/orlib.before_orlib.csv 2>/dev/null || true
rm -f results/benchmark.csv results/orlib_optima_check.csv
.venv/bin/python scripts/run_benchmark.py
```

Esperado:

- `results/orlib_optima_check.csv` con 15 filas.
- `pmed1`–`pmed15`.
- `status=OPT_MATCH` todas.
- `delta=0` todas.

Riesgo: `results/benchmark.csv` queda solo con lo corrido después del borrado. Si se necesitan también `rl1304` y `kroA100`, correr secciones 5 y 6 antes de graficar.

## 5. TSPLIB / paper Table 2 subset

```bash
.venv/bin/python scripts/compare_paper.py
```

Esperado:

- `results/comparison_vs_paper.csv`.
- 9 filas para `rl1304`.
- `delta_OPT=0` todas.
- `opt_comparison=OK` todas.

Nota: tiempos no comparables directamente con paper por máquina/solver.

## 6. TSPLIB pequeña `kroA100`

```bash
./pmedian instances/tsplib/kroA100.pmp --mode full
```

Esperado:

- `opt=30539`.
- Callback lazy con cortes > 0.
- Log: `results/logs/kroA100.pmp_p10_full.log`.

`kroA100` no es comparación principal del paper; sirve como validación geométrica y contra oráculo F3/prototipo.

## 7. Warm-start vs cold-start

Manual:

```bash
./pmedian instances/orlib/pmed1.pmp  --mode full --opt 5819
./pmedian instances/orlib/pmed1.pmp  --mode full --opt 5819 --coldstart
./pmedian instances/orlib/pmed6.pmp  --mode full --opt 7824
./pmedian instances/orlib/pmed6.pmp  --mode full --opt 7824 --coldstart
./pmedian instances/orlib/pmed11.pmp --mode full --opt 7696
./pmedian instances/orlib/pmed11.pmp --mode full --opt 7696 --coldstart
```

Registrar manualmente:

- `nodos_B&B`
- `cortes_lazy`
- `T2`
- `warm_cuts`

Fuente actual: `results/warmstart_comparison.csv`.

Defender solo reducción de nodos/cortes. No defender mejora general de tiempo.

## 8. Plot regeneration

Requiere `results/benchmark.csv` y `results/orlib_optima_check.csv` coherentes.

```bash
.venv/bin/python scripts/plot_results.py
```

Produce:

- `results/plot_a_bounds_orlib.png`
- `results/plot_b_time_vs_N.png`
- `results/plot_c_gap_vs_pM.png`
- `results/plot_d_iter_nodes_vs_p.png`

Copiar a report/Overleaf si se regeneran:

```bash
cp results/plot_*.png report/figures/
cp results/plot_*.png overleaf/report/figures/
```

## 9. Monolítico vs Benders

No ejecutar como comparación final: no hay solver monolítico C defendible.

Existe:

- brute force para instancias chicas en `src/instance.c` / tests.
- prototipo Python con F3 oracle (`prototype/pmp_benders.py`) para validación pequeña.

No existe:

- benchmark monolítico C contra Benders con límite 300 s.

Si profesor pregunta: “No lo implementamos como experimento comparativo; usamos F3/prototipo solo como oráculo en casos chicos.”

## 10. Resultados que no se deben regenerar sin plan

No correr por defecto:

- Zebra
- TSP > 10^4
- BIRCH grande
- RW grande
- ODM

Estado: fuera de alcance local.
