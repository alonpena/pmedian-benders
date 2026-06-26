# Alineación punto por punto con pauta de entrega final

Fuente pauta: `/Users/apena/Downloads/Pauta_entregaFinal (1).pdf`.

Regla de auditoría: solo se consideran claims respaldados por el informe, código, CSV/logs y archivos de evidencia locales (`report/REPORT_TABLES.md`, `report/FINAL_EVIDENCE_VALIDATION.md`, `report/evidence/*`).

## A. Informe, implementación y resultados — 25 pts

| Criterio pauta | Puntaje | Evidencia en informe/repositorio | Estado | Observación crítica |
|---|---:|---|---|---|
| Presentación del problema y motivación | 3.0 | `report/sections/01_motivacion.tex`, `02_definicion.tex`; referencias canónicas ReVelle & Swain, Kariv & Hakimi, Beasley, TSPLIB; caso industrial logística/refugios/k-medoids | CUBIERTO | Problema queda entendible para externo: decisión, sistema, relevancia. |
| Formulación final del modelo | 3.0 | `03_formulaciones.tex`; F1-F4; conjuntos clientes/sitios; parámetros `d_ij`, `p`; variables `x_ij`, `y_j`, `z_i^k`, `theta_i`; rol de restricciones | CUBIERTO | Índices corregidos: `z_i^k`, `k=1,...,K_i-1`. Se aclara que solver C usa maestro Benders + cortes F4 como `lazy constraints`, no F4 completa cargada. |
| Relajación lagrangiana | 3.0 | `04_lagrangiana.tex`; restricción complicante `sum_j x_ij = 1`; multiplicadores `lambda_i`; función `L(lambda)`; `beta_j`; dual lagrangiano; subgradiente; recuperación primal conceptual | CUBIERTO | Pauta no exige implementación. Está presentada como propuesta teórica y contraste con Benders. |
| Descomposición de Benders o método final | 5.0 | `05_benders.tex`, `06_separacion.tex`, `07_implementacion.tex`; maestro, subproblema por cliente, variables de conexión `y_j/theta_i`, optimality cuts, no feasibility cuts, Algoritmo 2 `ktilde_i`, `O(NM)` | CUBIERTO FUERTE | Núcleo validado contra derivación manual, test C e implementación Python de referencia (`results/logs/verify_cuts_oracle_diff.log`, 0 diferencias). |
| Instancias, datos y caso base | 2.5 | `08_instancias.tex`, `02_definicion.tex`; `toy1`; OR-Library pmed1-pmed40; TSPLIB rl1304/kroA100; RW local; grilla sintética; supuestos floor y duplicate edges | CUBIERTO | Caso base claro: `toy1`, óptimo 6, cortes a mano. Procedencia y decisiones de datos incluidas en texto. |
| Experimentos computacionales | 4.0 | `09_experimentos.tex`; Benders 300s; OR-Library pmed1-pmed40; rl1304; baseline F1 (monolithic model) parcial; synthetic stress N=5000; warm-start; logs callback | CUBIERTO FUERTE | Comparación con modelo base incluida solo donde existe evidencia (F1 parcial). No se afirma benchmark F1-F4 completo. |
| Resultados, insights y conclusiones | 3.0 | `10_resultados.tex`; patrones Phase 1, correctitud, warm-start, PopStar ausente, escala probada, Zebra paper-only, limitaciones | CUBIERTO | Resultados analizados, no solo reportados. Se separa correctitud (objetivos) de performance (tiempos/nodos/lazy constraints). |
| Calidad informe y reproducibilidad | 1.5 | `11_reproducibilidad.tex`; comandos; hardware/software; Gurobi; timeout externo 300s; `report/REPORT_TABLES.md`; `report/FINAL_EVIDENCE_VALIDATION.md`; `scripts/validate_results.py`; `scripts/paperbench.py` | CUBIERTO | PDF compila sin referencias `??`. Lenguaje técnico estandarizado: `NP-hard`, `warm-start`, `lazy constraints`, `monolithic model`. |

### Resultado esperado sección A

Estado global: **CUBIERTO**.

Riesgos residuales:

1. Zebra no ejecutado localmente: debe mantenerse como resultado de literatura del paper.
2. PopStar no implementado: afecta comparación de `UB1` con paper.
3. Baseline F1 es parcial: no presentar como campaña completa F1-F4.
4. Synthetic stress hasta `N=5000` no es benchmark del paper ni tiene óptimos externos conocidos.

## B. Presentación oral — 6 pts grupal + 4 pts respuestas individuales

| Criterio pauta | Puntaje | Evidencia en slides | Estado | Observación crítica |
|---|---:|---|---|---|
| Claridad del problema y motivación | 1.2 | Slides 1-2 | CUBIERTO | Inicia con decisión real y por qué F1 no escala. |
| Modelo y decisiones principales | 1.0 | Slide 3 | CUBIERTO | F1-F4 resumidas sin exceso algebraico; aclara monolithic model y F4 vía `lazy constraints`. |
| Descomposición o método utilizado | 1.3 | Slides 4-7 | CUBIERTO FUERTE | Benders explicado por intuición: qué se separa, por qué, cómo vuelven los cuts. Slide 6 dedicada a `ktilde_i` y `O(NM)`. |
| Resultados computacionales | 1.5 | Slides 8-10 | CUBIERTO | Incluye caso base/validación, OR-Library, rl1304, F1 baseline parcial, synthetic stress, warm-start, tiempos/nodos/lazy constraints. |
| Insights, discusión y conclusiones | 0.7 | Slide 11 | CUBIERTO | Cierra con qué funcionó, limitaciones y trabajo futuro. |
| Calidad comunicacional y tiempo | 0.3 | 11 slides + `slides/speaker_notes.md` | CUBIERTO | Deck optimizado para 12-15 min. Evita sobrecarga de ecuaciones. |

### Preguntas individuales: foco de estudio

Prioridad alta para Alonso:

1. Explicar `ktilde_i` sin mirar apuntes.
2. Justificar por qué no hay feasibility cuts.
3. Distinguir `monolithic model` vs Benders con `lazy constraints`.
4. Explicar por qué F3 mejora performance aunque tenga misma LP relaxation que F1/F2/F4.
5. Explicar por qué objetivo igual valida correctitud, pero performance se discute con tiempos/nodos/lazy constraints.
6. Defender alcance: Zebra/PopStar paper-only, no resultados locales.

## Veredicto de alineación

**Alineación con pauta: ALTA.**

El informe y las slides hacen alusión a todos los criterios evaluados. No quedan brechas mayores. La entrega es defendible si se mantiene disciplina de claims durante la presentación oral.
