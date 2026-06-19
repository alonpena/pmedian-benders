# Análisis de brechas contra la pauta — Proyecto final (Optimización Computacional, PUCV)

> Auditoría del repositorio contra `docs/Pauta_entregaFinal.pdf`. Objetivo: maximizar el
> puntaje del informe (25 pts) y de la presentación oral (10 pts) **sin fabricar resultados**.
> Cada criterio lista: qué pide la pauta · evidencia en el repo · evidencia faltante · riesgo ·
> acción recomendada · archivos exactos. Estado al 2026-06-19.

Leyenda de riesgo: 🟢 bajo (cubierto) · 🟡 medio (cubierto pero con caveat) · 🔴 alto (falta evidencia dura).

---

## A. Informe, implementación y resultados (25.0 pts)

### A1. Presentación del problema y motivación — 3.0 pts
- **Pauta:** problemática clara para alguien externo; contexto, decisiones, relevancia; apoyo en literatura, esquemas, mapas, ejemplos.
- **Evidencia repo:** definición y motivación (logística, k-medoids, emergencias) en `docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md` §1–2; paper de referencia `docs/Benders_decom_pMedian.pdf`. Reescrito formal en `report/sections/01_motivacion.tex`.
- **Falta:** una figura/esquema propio del sistema (cliente→sitio más cercano) ayuda; el `toy1` sirve de ejemplo numérico.
- **Riesgo:** 🟢
- **Acción:** incluir el ejemplo `toy1` (N=4, óptimo=6) como figura/diagrama en el informe; citar Kariv & Hakimi (NP-dureza), ReVelle & Swain, Duran-Mateluna et al. (2023).
- **Archivos:** `report/sections/01_motivacion.tex`, `report/sections/02_definicion.tex`, `instances/toy/toy1.pmp`.

### A2. Formulación final del modelo — 3.0 pts
- **Pauta:** formulación final con conjuntos, parámetros, variables, objetivo, restricciones, rol de cada bloque; incorporando correcciones de entregas previas.
- **Evidencia repo:** F1 (ReVelle & Swain), F2 (Cornuejols et al.), F3 (Elloumi), F4 (compacta de cortes) completas en `report/sections/03_formulaciones.tex`; base teórica en brief §3–4, §8.
- **Falta:** dejar explícito **cuál es la formulación final usada** (F3 como base de Benders → maestro F4 generado perezosamente). Ya explicitado en la sección.
- **Riesgo:** 🟢
- **Acción:** mantener notación consistente (conjuntos $[N],[M]$, radios $D^k_i$) en todo el informe; tabla comparativa F1–F4 (variables/restricciones/densidad).
- **Archivos:** `report/sections/03_formulaciones.tex`.

### A3. Relajación lagrangiana (propuesta teórica) — 3.0 pts
- **Pauta:** restricciones complicantes + justificación, lagrangiano, multiplicadores, dual lagrangiano, interpretación de la cota, subgradiente y recuperación primal conceptual. **No exige implementación.**
- **Evidencia repo:** desarrollo completo en `report/sections/04_lagrangiana.tex` (relaja asignación (3), $\beta_j(\lambda)$, dual $\max_\lambda L(\lambda)$, subgradiente, recuperación primal); brief §5.
- **Falta:** nada sustantivo; es teórica y está completa.
- **Riesgo:** 🟢
- **Acción:** enfatizar el contraste lagrangiana (separa por **sitio**) vs Benders (separa por **cliente**) — ambos dan cota inferior.
- **Archivos:** `report/sections/04_lagrangiana.tex`.

### A4. Descomposición de Benders / método final — 5.0 pts (mayor peso)
- **Pauta:** qué queda en maestro, qué en subproblema, qué variables conectan, qué cortes se generan y **por qué la descomposición es válida**.
- **Evidencia repo:** maestro, $SP_i$ primal, $DSP_i$ dual, derivación del corte (16), forma cerrada (17)–(20), separación $O(NM)$, optimalidad vs factibilidad — en `report/sections/05_benders.tex` y `06_separacion.tex`. **Implementado y verificado**: separador C validado a mano (toy1), por test unitario y contra oráculo Python (0 diffs) — `docs/AUDIT.md` afirmaciones 14–15, `tests/test_separation_toy.c`, `scripts/verify_cuts.py`. Prueba de que es branch-and-Benders-cut real: `results/logs/pmed1.pmp_p5_full.log` (`lazy_cuts=90`, `is_branch_and_benders_cut=YES`).
- **Falta:** nada crítico. Punto fuerte del proyecto.
- **Riesgo:** 🟢
- **Acción:** destacar el argumento de validez: $SP_i$ **siempre factible y acotado** ⇒ **solo cortes de optimalidad**; el maestro converge porque hay un número finito de cortes (20) distintos.
- **Archivos:** `report/sections/05_benders.tex`, `report/sections/06_separacion.tex`, `src/separation.c`, `src/phase2.c`, `docs/AUDIT.md`.

### A5. Instancias, datos y caso base — 2.5 pts
- **Pauta:** describir instancias, fuentes, supuestos, parámetros, tamaño; al menos **un caso base** verificable.
- **Evidencia repo:** OR-Library pmed1–15 (Beasley 1990), TSPLIB rl1304/kroA100 (Reinelt 1991), RW asimétrica (rw12), toy1. Formato en `docs/INSTANCE_FORMAT.md`. Caso base **toy1** (óptimo a mano = 6) y **pmed1** (óptimo oficial 5819). Supuesto de distancia euclidiana truncada (floor) documentado y validado. Regla de aristas duplicadas en `docs/ADR/0002-orlib-duplicate-edges.md`.
- **Falta:** familias BIRCH/ODM/RW grandes y TSP medianas/grandes **no ejecutadas** (marcado UNVERIFIED en `docs/AUDIT.md`).
- **Riesgo:** 🟡 (caso base sólido; cobertura de familias parcial — declararlo).
- **Acción:** describir el alcance real (OR-Library completa + rl1304 hasta p=500 + validación asimétrica rw12) y declarar honestamente lo no corrido.
- **Archivos:** `report/sections/08_instancias.tex`, `docs/INSTANCE_FORMAT.md`, `docs/ADR/0002-orlib-duplicate-edges.md`, `instances/`.

### A6. Experimentos computacionales — 4.0 pts
- **Pauta:** diseño ordenado; comparación con base; crecimiento del problema; selección justificada; tiempos, gaps, cotas, iteraciones, cortes.
- **Evidencia repo:** `results/benchmark.csv` (20 corridas), `results/orlib_optima_check.csv` (15/15 óptimo, delta=0), `results/comparison_vs_paper.csv` (rl1304, 9/9 óptimos coinciden con el paper), `results/warmstart_comparison.csv` (warm vs cold), 4 figuras `results/plot_*.png`, prueba de callback en `results/logs/*.log`.
- **Falta:** comparación directa contra Zebra (no ejecutado; tiempos del paper son ajenos). Comparación contra F3 entero como "modelo base" solo vía oráculo Python pequeño.
- **Riesgo:** 🟡 (rico en métricas propias; "base" comparada es óptimo oficial / paper, no un solver base corrido por nosotros salvo prototipo).
- **Acción:** presentar (a) escalamiento $T_{tot}$ vs $N$, (b) gap Fase 1 vs $p/M$, (c) nodos vs $p$, (d) warm vs cold; declarar que Zebra no se reejecutó.
- **Archivos:** `report/sections/09_experimentos.tex`, `results/*.csv`, `results/plot_*.png`, `scripts/run_benchmark.py`, `scripts/compare_paper.py`.

### A7. Resultados, insights y conclusiones — 3.0 pts
- **Pauta:** analizar (no solo reportar); patrones, ventajas/limitaciones, comparación de escenarios, aprendizajes para el problema real.
- **Evidencia repo:** insights ya escritos: Fase 1 resuelve o casi resuelve muchas instancias (gap≈0); warm-start reduce nodos drásticamente (pmed1 223→1) pero el wall-time es mixto en sub-segundo; sin PopStar el UB1 es peor que el del paper aunque el LB1 coincide; el costo se concentra en Fase 2 / construcción de S a gran escala.
- **Falta:** discusión de límites a gran escala es **conceptual** (no medimos >10⁴ puntos).
- **Riesgo:** 🟡
- **Acción:** conectar con el problema real (localización/clustering): cotas tempranas útiles para decisiones; honestidad sobre lo no medido.
- **Archivos:** `report/sections/10_resultados.tex`, `results/warmstart_comparison.csv`, `results/comparison_vs_paper.csv`.

### A8. Calidad del informe y reproducibilidad — 1.5 pts
- **Pauta:** organización, redacción, notación consistente, tablas/figuras legibles; reproducibilidad: archivos, parámetros, solver, tiempos límite, configuración.
- **Evidencia repo:** `report/` modular (LaTeX), notación unificada; `report/sections/11_reproducibilidad.tex` con comandos exactos; `Makefile` (autodetección Gurobi), `docs/AUDIT.md` (evidencia por afirmación + comando), `docs/SOLVER_NOTES.md`. Logs por corrida en `results/logs/`.
- **Falta:** compilar el PDF final (`pdflatex`) y verificar figuras incrustadas.
- **Riesgo:** 🟢
- **Acción:** compilar `report/main.tex`, revisar que las 4 figuras `plot_*.png` se incrusten; checklist final (ver abajo y `slides/speaker_notes.md`).
- **Archivos:** `report/main.tex`, `report/sections/11_reproducibilidad.tex`, `Makefile`, `docs/AUDIT.md`.

---

## B. Presentación oral (10.0 pts: 6.0 grupal + 4.0 individual)

| Criterio (pauta) | Pts | Diapositiva que lo cubre | Riesgo |
|---|---|---|---|
| Claridad del problema y motivación | 1.2 | Slide 1 (Problema y motivación) | 🟢 |
| Modelo y decisiones principales | 1.0 | Slide 3 (F1–F4) | 🟢 |
| Descomposición / método | 1.3 | Slides 4–5 (Lagrangiana, Benders) | 🟢 |
| Resultados computacionales | 1.5 | Slide 7 (Resultados) | 🟢 |
| Insights, discusión, conclusiones | 0.7 | Slide 8 (Conclusiones) | 🟢 |
| Calidad comunicacional y tiempo | 0.3 | 8 slides para ~15 min; notas en `slides/speaker_notes.md` | 🟢 |

- **Individual (4.0):** preguntas. Riesgo 🟡 → preparar dominio de: por qué solo cortes de optimalidad, derivación de (18)/(20), complejidad $O(NM)$, rol de la matriz $S$, diferencia lagrangiana/Benders. Cubierto en `slides/speaker_notes.md`.

---

## Resumen de riesgos y prioridades

| Prioridad | Ítem | Acción |
|---|---|---|
| P1 | Compilar `report/main.tex` y `slides/main.tex` | verificar LaTeX + figuras |
| P2 | Declarar alcance honesto de familias/Zebra | ya en `09`/`10` y `AUDIT.md` |
| P3 | Figura del sistema (toy1) | opcional, sube A1 |
| P4 | Ensayar respuestas individuales | `slides/speaker_notes.md` |

**Sin fabricación:** todo número del informe proviene de `results/` (CSV/logs) o se marca placeholder/UNVERIFIED. Lo no medido (Zebra, BIRCH/ODM/RW grande, TSP grande) se declara explícitamente.
