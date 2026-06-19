# Auditoría final de entrega

> Última auditoría antes de la entrega del Proyecto Final (Optimización Computacional, PUCV).
> Fecha: 2026-06-19. Repo: `github.com/alonpena/pmedian-benders` (privado), rama `main`.
> Commit base de esta auditoría: `cf021d6` (el commit final que la incluye se referencia abajo).

## Estado del repositorio
- Rama: `main`, sincronizada con `origin/main` tras el commit final.
- Compila el núcleo en C sin warnings; `make test` y `scripts/verify_cuts.py` en verde.
- Todos los números de informe/figuras provienen de `results/` (CSV/logs). Sin fabricación.

## Lo que está PLENAMENTE verificado (evidencia dura)
| Afirmación | Evidencia |
|---|---|
| Separador C = derivación a mano = oráculo Python (0 diffs) | `make test` PASS; `results/logs/verify_cuts_oracle_diff.log` (`diffs=0`) |
| OR-Library pmed1–15 al óptimo oficial, delta=0 | `results/orlib_optima_check.csv` |
| rl1304: 9/9 óptimos = paper (Tabla 2) | `results/comparison_vs_paper.csv` |
| Fase 2 = branch-and-Benders-cut real (lazy>0) | `results/logs/pmed1...log` (`lazy_cuts=90`), `rl1304_p5` (`lazy_cuts=1850`) |
| Warm-start reduce nodos (223→1, 632→7, 352→1) | `results/warmstart_comparison.csv` |
| $\tilde k_i$ / OPT(SP) / corte exactos en toy1 | `tests/test_separation_toy.c` PASS |
| F3 oráculo = C en kroA100 (30539) | `docs/AUDIT.md` #10 |
| Núcleo sin warnings | `make clean && make pmedian` |

## Lo que está PARCIALMENTE verificado
| Tema | Estado | Detalle |
|---|---|---|
| Complejidad $O(NM)$ | implementada, no medida a escala | correcta hasta $N=1304$; sin timing aislado a $>10^4$ |
| Comparación con el paper | solo Tabla 2 (rl1304) | Tablas 3–9 no transcritas ni corridas |
| Ventaja wall-time del warm-start | solo nodos/cortes | mixto en sub-segundo; no probado a gran escala |
| $UB_1$ vs paper | diferencia explicada | sin PopStar; afecta $UB_1$, no $LB_1$ |

## Lo que NO se intentó (declarado, no presentado como propio)
- Reejecución de **Zebra** (tiempos del paper).
- Familias **TSP grandes, BIRCH, RW grande, ODM**.
- **Reduced-cost fixing**, **constraint reduction**, **PopStar** (verificado ausente en `src/`).
- Backend **CPLEX/SCIP** (solo Gurobi compilado).

## Comandos de reproducción exactos
```bash
export GUROBI_HOME=/Library/gurobi1200/macos_universal2
export DYLD_LIBRARY_PATH=$GUROBI_HOME/lib

make test                                   # núcleo + verificación separador (toy=6)
make pmedian                                # binario
python scripts/verify_cuts.py               # C == Python (0 diffs)

./pmedian instances/orlib/pmed1.pmp --mode full --opt 5819
python scripts/run_benchmark.py             # OR-Library -> orlib_optima_check.csv
python scripts/compare_paper.py             # rl1304 -> comparison_vs_paper.csv
python scripts/plot_results.py              # 4 figuras
```

## Archivos a ENTREGAR (evaluación del curso)
- **Informe (PDF):** compilar `overleaf/report/main.tex` en Overleaf.
- **Diapositivas (PDF):** compilar `overleaf/slides/main.tex`.
- **Notas de defensa:** `docs/DEFENSA_ORAL.md` (uso interno del grupo).
- **Repositorio:** enlace a `github.com/alonpena/pmedian-benders` (código + `results/` + `docs/`).

## Archivos a SUBIR a Overleaf
**Proyecto informe** (`overleaf/report/`):
```
main.tex
sections/01_motivacion.tex ... 11_reproducibilidad.tex, 02b_literatura.tex, anexo_codigo.tex
figures/plot_a_bounds_orlib.png, plot_b_time_vs_N.png, plot_c_gap_vs_pM.png, plot_d_iter_nodes_vs_p.png
```
**Proyecto diapositivas** (`overleaf/slides/`): `main.tex`.
Instrucciones completas: `overleaf/README_OVERLEAF.md`.

## Riesgos conocidos
1. **Compilación Overleaf no probada localmente** (sin toolchain TeX en la máquina). Verificación
   solo estructural (entornos, `$`, macros, inputs, figuras). → Compilar en Overleaf y revisar.
2. **1 TODO abierto:** figura/esquema del sistema en §1 (se imprime al final del PDF). No bloquea.
3. **Cobertura experimental parcial:** 1 de 8 tablas del paper. Declarado en informe y matriz.
4. **Preguntas individuales (40% oral):** preparar con `docs/DEFENSA_ORAL.md` (14 preguntas).
5. **Choque de notación** $\theta_i$ (pMP) vs $\eta$/$\theta(x)$ (curso): puenteado en §5; un
   glosario lo cerraría (opcional).

## Veredicto
**READY WITH RISKS.** El contenido es correcto, verificado y honesto; los riesgos son de
compilación final (Overleaf), de cobertura experimental declarada y de preparación oral —ninguno
es un defecto de fidelidad ni de fabricación.
