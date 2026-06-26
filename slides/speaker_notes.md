# Notas del orador — defensa final (≈12–15 min, 11 slides)

Mensaje central:

> Implementé y verifiqué el mecanismo Benders central del paper: F3 como base, F4 vía lazy cuts, separación cerrada O(NM), Phase 1, Phase 2 y warm-start por cortes. La evidencia local valida correctitud y rendimiento en campañas acotadas; no ejecuté Zebra ni PopStar.

No decir:

- “nuestra implementación supera localmente a Zebra”
- “replicamos completamente el paper”
- “PopStar fue usado”

Sí decir:

- “el paper reporta mejora frente a Zebra”
- “yo comparo localmente contra F1 parcial y contra óptimos/valores del paper para validar correctitud”
- “objetivo igual sirve para correctitud; tiempo/nodos/lazy cuts sirven para performance”

---

## Slide 1 — Problema de decisión

Abrir exactamente `p` sitios para minimizar distancia total cliente → sitio abierto más cercano.
Ejemplo rápido: bodegas/refugios/k-medoids.

Frase clave:

> Si ya sé qué sitios abrir, la asignación es trivial. Lo difícil es elegir los sitios.

Eso prepara Benders.

## Slide 2 — Por qué F1 no escala

Explicar F1 como modelo natural del curso: `x_ij`, `y_j`, asignación, enlace.
Problema: `N*M` variables y restricciones. Con `10^4 x 10^4`, se vuelve enorme.

Conectar con consejo del profesor:

> La idea para performance no fue “cambiar de solver”; fue reformular y explotar estructura.

## Slide 3 — F1–F4

No leer tabla completa. Decir:

- F1 directa pero grande.
- F2 cambia asignaciones por radios.
- F3 mantiene fortaleza, pero matriz más rala.
- F4 usa `theta_i`, pero cargada completa es densa; se usa como lazy cuts.

Frase para defender:

> Mismo óptimo y misma relajación LP no significa mismo rendimiento: densidad manda.

## Slide 4 — Lagrangiana

Breve. Sirve para mostrar contenido de curso.
Relajo asignación, obtengo problema por sitio: abrir `p` sitios con menor beta.

Contraste importante:

> Lagrangiana separa por sitio; Benders fija `y` y separa por cliente.

## Slide 5 — Benders

Núcleo conceptual. Ir lento.

Maestro:

- decide `y_j`
- estima costos con `theta_i`
- recibe cortes

Subproblema:

- uno por cliente
- calcula distancia inducida por `ybar`

Por qué no feasibility cuts:

> No hay capacidad ni asignaciones prohibidas; con `p>=1` todo cliente puede conectarse. Entonces `SP_i` siempre factible y acotado. Solo optimality cuts.

## Slide 6 — Corte cerrado / Algoritmo 2

Esta es slide más importante para preguntas.

Explicar `S_i`: sitios ordenados por distancia para cliente `i`.
Calcular `ktilde_i`:

1. recorro sitios desde cerca a lejos;
2. acumulo masa `ybar`;
3. cuando acumulo 1, encontré primer radio cubierto;
4. `ktilde` es último radio no cubierto.

Frase clave:

> Aquí está la mejora del paper: Benders sin resolver LPs de subproblema. El corte sale por fórmula.

## Slide 7 — Implementación/verificación

Defender código:

- `sortsites.c`: matriz `S`
- `separation.c`: `ktilde`, `OPT(SP_i)`, corte
- `phase1.c`: LP + cuts + rounding
- `phase2.c`: branch-and-Benders-cut con lazy cuts

Verificación:

- mano en toy
- test C
- oráculo Python
- 0 diferencias

Frase:

> Antes de creer tiempos, validé el separador. Si el separador falla, todo lo demás es humo.

## Slide 8 — Protocolo experimental

Objetivo de esta slide: disciplinar claims.

Puntos:

- timeout externo 300s
- CSV + logs
- Benders 26 filas
- OR-Library pmed1–pmed40 consolidado
- rl1304 9 puntos del paper
- F1 baseline parcial
- sintético N=5000

Aclarar:

> No mezclé resultados de literatura con resultados locales. Zebra/PopStar quedan como paper-only.

## Slide 9 — Correctitud y escala

Objetivo/óptimo = correctitud.

Decir:

- pmed1–pmed40: 40/40 óptimos oficiales
- rl1304: 9/9 óptimos iguales al paper
- sintético N=5000: stress local, no paper, no óptimo externo

Frase:

> Igualar óptimos prueba que no estoy resolviendo otro problema. No prueba superioridad de rendimiento por sí solo.

## Slide 10 — Performance y estado del arte

Aquí responder consejo del profesor.

Local:

- Benders vs F1 parcial: Benders gana en 4/5, pierde en toy1 por overhead.
- Warm-start reduce nodos fuerte; tiempo mixto en casos subsegundo.

Estado del arte:

> El paper compara contra Zebra y reporta mejora en tiempo. Yo no ejecuté Zebra; por eso no reclamo mejora local frente a Zebra. Mi comparación local de rendimiento es contra F1 parcial y métricas propias: tiempo, nodos, lazy cuts.

Frase importante:

> Para performance importan tiempos/nodos/cuts; el objetivo es control de correctitud.

## Slide 11 — Cierre

Cerrar con tesis:

> La ganancia viene de formular y separar bien, no de apretar “solve”.

Limitaciones dichas voluntariamente:

- no PopStar
- no Zebra local
- no reduced-cost fixing
- no constraint reduction
- no BIRCH/RW grande/ODM
- no huge TSP

Eso suma credibilidad.

---

# Preguntas probables y respuestas cortas

## 1. ¿Por qué solo optimality cuts?
`SP_i` siempre factible y acotado. No hay capacidades ni asignaciones prohibidas; con `p>=1` cada cliente puede asignarse a algún sitio. Entonces el dual no tiene rayos extremos: no feasibility cuts.

## 2. ¿Qué es `ktilde_i`?
Último radio donde el cliente aún no está cubierto por `ybar`. Se calcula recorriendo sitios ordenados por distancia y acumulando `ybar` hasta llegar a 1.

## 3. ¿Por qué O(NM)?
Por cliente recorro a lo más `M` sitios. Hay `N` clientes. No se resuelven LPs de subproblema.

## 4. ¿Qué hizo la idea de performance?
Tres cosas: usar F3 rala como base, no cargar F4 completa sino lazy cuts, y usar separación cerrada del dual. Además warm-start hereda cuts de Phase 1.

## 5. ¿Qué significa PopStar aquí?
Heurística primal usada por el paper para buenas cotas superiores `UB1`. No la implementé; por eso algunos `UB1` locales son peores aunque `LB1` y óptimos coincidan.

## 6. ¿Superas a Zebra?
No puedo afirmar eso localmente. El paper reporta mejora frente a Zebra. Yo no ejecuté Zebra; mi evidencia local valida el mecanismo y compara parcialmente contra F1.

## 7. ¿Qué implementaste realmente?
Solver principal C: Benders/F4 con lazy cuts derivada de F3. F1 monolítica solo baseline parcial. F2/F3/F4 monolíticas completas no están implementadas como campaña.

## 8. ¿Objetivo igual al paper qué demuestra?
Correctitud/modelado: mismo óptimo en las instancias comparadas. Performance se evalúa con tiempo, nodos, lazy cuts, timeouts.

## 9. ¿Qué queda como trabajo futuro?
PopStar, Zebra local, reduced-cost fixing, constraint reduction, ODM, BIRCH/RW grande y huge TSPLIB.

---

# Checklist pre-defensa

```bash
make test
.venv/bin/python scripts/verify_cuts.py
.venv/bin/python scripts/validate_results.py
.venv/bin/python scripts/paperbench.py validate --csv results/curated/paperbench_current.csv
cd report && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
cd ../slides && pdflatex -interaction=nonstopmode main.tex
```

Ensayo:

- 1 min problema
- 2 min formulaciones
- 4 min Benders/separación
- 2 min implementación/verificación
- 3 min resultados/performance
- 1 min límites/cierre
