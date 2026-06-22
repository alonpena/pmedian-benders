# Replicación parcial y análisis computacional de una descomposición de Benders eficiente para el problema p-mediana

## Portada placeholder

- **Curso:** Optimización Computacional
- **Universidad:** Pontificia Universidad Católica de Valparaíso (PUCV)
- **Tema:** Problema p-mediana y descomposición de Benders
- **Estudiante:** Alonso Peña
- **Fecha:** [COMPLETAR FECHA]
- **Referencia principal:** Duran-Mateluna, C., Ales, Z., & Elloumi, S. (2023). *An efficient Benders decomposition for the p-median problem*, European Journal of Operational Research, 308, 84–96.

## Resumen

Este informe presenta una replicación parcial y auditada de la descomposición de Benders para el problema p-mediana propuesta por Duran-Mateluna, Ales y Elloumi (2023). El proyecto implementa en C, con backend Gurobi, un método estilo F4/branch-and-Benders-cut derivado de la formulación F3 del artículo: el maestro contiene variables de apertura `y_j` y variables de costo por cliente `theta_i`, mientras que los cortes de optimalidad se separan mediante sitios ordenados y el índice `ktilde_i`. La replicación es deliberadamente parcial: se valida el núcleo matemático y computacional, pero no se reimplementan todos los componentes del paper. Los experimentos usan un protocolo con límite externo de 300 segundos mediante wrappers Python y guardan evidencia en CSV, logs y figuras. La evidencia verificada incluye OR-Library pmed1–pmed15, un smoke test de pmed16, TSPLIB `rl1304` y `kroA100`, una línea base monolítica F1, trazas de gap de Fase 1 y una campaña sintética hasta N=5000. No se replica localmente Zebra, PopStar, reduced-cost fixing, constraint reduction, ni las campañas completas BIRCH/RW/ODM o TSPLIB enormes. Por tanto, el resultado debe leerse como una replicación progresiva del núcleo de Benders y no como una reproducción completa del artículo.

---

## 1. Introducción

El problema p-mediana es un modelo clásico de localización: dado un conjunto de clientes y un conjunto de posibles instalaciones, se debe escoger exactamente `p` instalaciones abiertas y asignar cada cliente a una de ellas minimizando el costo total de servicio. En términos económicos, abrir instalaciones representa una decisión estratégica de capacidad o presencia territorial; asignar clientes genera costos operacionales recurrentes. La distancia o costo `d_ij` entre un cliente `i` y una instalación `j` representa esfuerzo de servicio: tiempo de viaje, costo logístico, latencia, distancia social, costo de distribución o dificultad de atención.

Este modelo aparece en localización de plantas y bodegas, diseño de redes logísticas, planificación de servicios públicos, asignación territorial de demanda, diseño de redes de atención, sistemas de emergencia, distribución industrial, clustering medoidal y aplicaciones cibernéticas o de sistemas donde se eligen nodos representantes para reducir costos de comunicación o control. En ingeniería industrial, el p-mediana conecta decisiones de inversión con desempeño operacional: decidir dónde abrir centros afecta directamente la suma de costos de asignación.

Desde el punto de vista de optimización computacional, el problema es desafiante porque combina decisiones binarias de apertura con asignación de muchos clientes. Las formulaciones enteras clásicas pueden crecer rápidamente, sobre todo por variables `x_ij` para cada par cliente-sitio. Por ello, el artículo de Duran-Mateluna et al. estudia formulaciones fuertes y una descomposición de Benders que evita materializar parte de la estructura de asignación/radio, reemplazándola por variables agregadas y cortes generados dinámicamente.

El objetivo de este proyecto es implementar y evaluar una replicación parcial del núcleo del método: formulación base, comparación con una línea monolítica F1, relajación y cotas, separación de cortes, Fase 1 LP, Fase 2 branch-and-Benders-cut, experimentos con timeout externo de 300 segundos y discusión crítica de lo que sí y no fue replicado.

## 2. Descripción del problema p-mediana

Sean:

- `I = {1,...,n}` el conjunto de clientes o puntos de demanda.
- `J = {1,...,m}` el conjunto de sitios candidatos para abrir instalaciones.
- `p` el número exacto de instalaciones a abrir, con `p >= 1`.
- `d_ij >= 0` el costo o distancia de asignar el cliente `i` al sitio `j`.

La decisión consiste en escoger un subconjunto `P ⊆ J` con `|P| = p` y asignar cada cliente `i` a un sitio abierto `j ∈ P`. El costo de un cliente queda dado por la menor distancia a un sitio abierto:

```text
c_i(P) = min_{j in P} d_ij.
```

El objetivo global es:

```text
min_{P subset J, |P|=p} sum_{i in I} min_{j in P} d_ij.
```

La dificultad intuitiva es combinatoria: existen `binom(m,p)` subconjuntos posibles de instalaciones. Además, para cada subconjunto debe evaluarse la asignación más barata de todos los clientes. Aunque la asignación para un conjunto fijo de instalaciones es simple, elegir el conjunto óptimo no lo es. En instancias grandes, el número de combinaciones y la interacción entre apertura y asignación hacen necesaria una formulación matemática y un algoritmo de solución eficiente.

## 3. Formulación clásica F1

La formulación clásica de asignación usa variables:

- `y_j = 1` si se abre una instalación en el sitio `j`; `0` en caso contrario.
- `x_ij = 1` si el cliente `i` se asigna al sitio `j`; `0` en caso contrario. En la variante fuerte usada como baseline local, `x_ij` puede ser continua en `[0,1]` porque la estructura de asignación y las variables `y` binarias inducen soluciones enteras de asignación en el óptimo.

Modelo F1:

```text
min   sum_{i in I} sum_{j in J} d_ij x_ij
s.a.  sum_{j in J} x_ij = 1              para todo i in I
      x_ij <= y_j                        para todo i in I, j in J
      sum_{j in J} y_j = p
      x_ij >= 0                          para todo i,j
      y_j in {0,1}                       para todo j
```

La primera restricción obliga a asignar cada cliente a un sitio. La restricción `x_ij <= y_j` impide asignar clientes a instalaciones cerradas. La restricción de cardinalidad controla la decisión estratégica: exactamente `p` instalaciones se abren.

F1 es pedagógicamente importante porque expresa el problema de manera directa: apertura más asignación. También permite construir una línea base computacional. Sin embargo, crece con `n*m` variables de asignación y `n*m` restricciones de enlace. Para instancias con `n=m=5000`, F1 tendría 25 millones de variables `x_ij` y 25 millones de restricciones de enlace, antes de considerar detalles de memoria del solver. Por eso sirve como punto de partida, pero no como único enfoque escalable.

En el proyecto se implementó una línea base experimental `--mode monolithic-f1` en una rama separada. Se resolvieron cinco instancias pequeñas/medianas bajo timeout externo de 300 segundos: `toy1`, `pmed1`, `pmed2`, `pmed6` y `kroA100`. Todas fueron resueltas óptimamente, pero el tamaño del modelo crece rápido: para `pmed6` (`N=200`) el modelo tiene 40.200 variables, 40.201 restricciones y 120.200 no ceros.

## 4. Formulación F3/F4 y relación con el paper

El artículo trabaja con formulaciones basadas en distancias ordenadas. Para cada cliente `i`, se consideran distancias distintas ordenadas a los sitios candidatos. La formulación F3 introduce lógica de radios mediante variables asociadas a niveles de distancia, usualmente denotadas `z_i^k`, que capturan si el costo de asignación del cliente supera cierto umbral. Esta estructura evita algunas debilidades de la formulación de asignación directa y sirve como base para una reformulación más eficiente.

La implementación local no pretende reimplementar todos los componentes del artículo. El núcleo matemático implementado corresponde a una variante estilo F4/branch-and-Benders-cut derivada de F3. En lugar de mantener explícitamente todas las variables de radio, el maestro usa:

- `y_j`: decisión de apertura del sitio `j`.
- `theta_i`: variable continua que representa una cota inferior sobre el costo de servicio del cliente `i` dado el patrón de aperturas.

El objetivo del maestro es minimizar `sum_i theta_i`. Los cortes de Benders fuerzan a que cada `theta_i` sea suficientemente grande según los sitios abiertos. Así, los costos por cliente se aproximan sistemáticamente mediante cortes válidos generados por separación. El valor real de asignación de un cliente no se calcula mediante variables `x_ij` permanentes, sino por separación cerrada usando distancias ordenadas.

La relación con el paper es central pero parcial: se replica el mecanismo algorítmico del maestro, subproblema/separación, cortes de optimalidad, Fase 1 y Fase 2 con lazy constraints. No se replican PopStar, Zebra, reduced-cost fixing ni constraint reduction.

## 5. Descomposición de Benders implementada

### 5.1 Maestro

El maestro mantiene variables `y_j` y `theta_i`:

```text
min   sum_{i in I} theta_i
s.a.  sum_{j in J} y_j = p
      cortes de optimalidad de Benders
      0 <= y_j <= 1   en Fase 1
      y_j in {0,1}    en Fase 2
      theta_i >= 0
```

En Fase 1, `y` es continua y se resuelve una relajación LP con generación iterativa de cortes. En Fase 2, `y` es binaria y Gurobi explora el árbol branch-and-bound. En soluciones enteras candidatas, el callback separa cortes violados como lazy constraints.

### 5.2 Subproblema y separación

Fijado un vector `\bar y`, el costo de cada cliente es separable: el cliente `i` solo necesita saber qué sitios están abiertos o parcialmente abiertos y cuáles son sus distancias. La implementación precomputa para cada cliente una lista `S_i` de sitios ordenados por distancia creciente. Luego calcula un índice `ktilde_i` que identifica el punto relevante de separación en la lista ordenada.

El separador construye un corte de la forma general:

```text
theta_i + sum_j a_ij y_j >= b_i
```

Los coeficientes dependen de las diferencias entre distancias ordenadas. No es necesario resolver un LP de subproblema con el solver para cada cliente; el subproblema tiene solución cerrada explotada por el código.

### 5.3 Cortes de optimalidad y ausencia de cortes de factibilidad

Los cortes generados son cortes de optimalidad: elevan `theta_i` cuando el maestro subestima el costo real del cliente. No se requieren cortes de factibilidad en esta implementación estándar del p-mediana cuando `p >= 1`, porque siempre existe al menos una instalación abierta y todo cliente puede asignarse a alguna instalación. Por tanto, el subproblema de asignación por cliente es factible y acotado para cualquier solución maestra que satisfaga `sum_j y_j = p` y `y_j >= 0`.

### 5.4 Justificación computacional

La descomposición elimina la necesidad de mantener explícitamente todas las variables `x_ij` de asignación en el maestro. También evita materializar todas las variables de radio de la formulación F3/F4. En su lugar, el maestro conserva `m+n` variables principales y agrega cortes solo cuando son necesarios. Computacionalmente, esto traslada trabajo desde el tamaño del modelo inicial hacia la separación iterativa de cortes. En las instancias verificadas, esta estrategia permite resolver casos de `N=1304` y sintéticos de `N=5000` bajo el protocolo de 300 segundos.

### 5.5 Cotas, relajación y estados experimentales

La Fase 1 resuelve una relajación LP del maestro Benders: `y_j` puede tomar valores fraccionales en `[0,1]`. El valor objetivo de ese maestro relajado, después de agregar cortes válidos, entrega una cota inferior `LB` sobre el problema entero, porque relaja la integralidad y porque los cortes añadidos subestiman de forma válida la función de costo por cliente. En la implementación, la columna `LB1` corresponde al valor de la relajación de Fase 1 al terminar el proceso de separación.

La cota superior `UB` proviene de una solución factible entera construida por redondeo o, en Fase 2, de incumbentes enteros del MIP. Como cualquier solución factible abre exactamente `p` instalaciones y asigna todos los clientes, su costo es una cota superior válida. El gap de Fase 1 se interpreta como `(UB-LB)/UB` cuando `UB>0`.

Debe distinguirse entre cinco conceptos: (i) la cota de la relajación LP; (ii) la cota inferior del maestro Benders con cortes; (iii) la cota superior incumbente; (iv) el gap MIP interno de Gurobi en un modelo entero; y (v) el estado experimental de una fila CSV, por ejemplo `OPT_MATCH` o `OPTIMAL_NO_KNOWN`. `OPT_MATCH` significa que el objetivo local coincide con un óptimo conocido suministrado; `OPTIMAL_NO_KNOWN` significa que el solver reportó optimalidad local, pero no se comparó contra un valor externo confiable.

## 6. Algoritmo computacional

Pseudocódigo de alto nivel:

```text
Entrada: instancia p-mediana (I, J, d, p)
Salida: objetivo, sitios abiertos, cotas, tiempos, cortes, nodos

1. Cargar instancia.
2. Construir o consultar matriz/distancia d_ij.
3. Para cada cliente i:
      ordenar sitios por distancia y guardar S_i.

4. Fase 1: relajación LP del maestro
      crear maestro con y_j continuas en [0,1] y theta_i >= 0
      agregar sum_j y_j = p
      inicializar pool de cortes vacío
      repetir:
          resolver maestro LP
          obtener solución (bar y, bar theta)
          para cada cliente i:
              calcular ktilde_i usando S_i y bar y
              evaluar si theta_i subestima el costo
              si hay violación:
                  generar corte de optimalidad
                  agregar corte al maestro y al pool
          construir una solución factible por redondeo para actualizar UB
          actualizar LB con valor del maestro LP
          calcular gap de Fase 1 si UB está disponible
      hasta que no existan cortes violados o se alcance límite interno

5. Fase 2: maestro binario branch-and-Benders-cut
      crear maestro con y_j binarias y theta_i >= 0
      cargar cortes del pool de Fase 1 como warm-start
      resolver MIP con Gurobi
      en cada solución entera candidata:
          leer y, theta del callback
          separar cortes por cliente
          agregar cortes violados como lazy constraints
      terminar cuando Gurobi certifica optimalidad o el wrapper externo termina

6. Registrar:
      objetivo final, LB1, UB1, gap reportado, T1, T2, Ttot,
      iteraciones, nodos B&B, cortes lazy, llamadas de separación,
      status, timeout_flag y ruta del log.
```

La idea central es que los cortes aproximan progresivamente la función de recourse o valor de asignación. Al comienzo el maestro puede subestimar el costo porque `theta_i` no está suficientemente restringida. Cada corte elimina una subestimación específica sin enumerar todas las posibles configuraciones desde el inicio.

## 7. Implementación

El solver principal está implementado en C. El backend de optimización es Gurobi mediante una capa delgada `solver_gurobi.c`. El repositorio contiene:

- Parser de instancias `.pmp` en formato coordenadas o matriz.
- Oráculo de distancia.
- Estructuras de sitios ordenados `S_i`.
- Separador de cortes.
- Fase 1 LP.
- Fase 2 MIP con lazy callbacks de Gurobi.
- Pool de cortes para warm-start.
- Scripts Python para campañas, conversión, visualización y auditoría.

Los experimentos comparables usan wrappers Python con `subprocess.run(..., timeout=300)`, de modo que el límite de 5 minutos es externo al solver. Esto evita confundir parámetros internos de Gurobi con el protocolo experimental.

La evidencia se guarda en CSV y logs. Cada fila experimental tiene una ruta a un log crudo cuando corresponde. Durante la auditoría se verificó que los logs contienen ejecución real del solver: líneas de instancia, licencia Gurobi, Fase 1, Fase 2 y callback.

El flujo experimental se organizó por ramas. Esto protege el núcleo Benders verificado, pero implica que no todos los CSV/figuras viven simultáneamente en una sola rama. La reproducción debe considerar el mapa de ramas indicado en `docs/EXPERIMENTAL_HANDOFF_FOR_REPORT.md`.

### 7.1 Mapa de evidencia y reproducibilidad

Para preparar este informe se consolidó evidencia desde ramas experimentales hacia `report/evidence/` y `report/figures/`. El índice `report/FINAL_EVIDENCE_INDEX.md` lista, para cada artefacto, la rama fuente, la ruta original, el commit y la ruta consolidada. La validación `report/FINAL_EVIDENCE_VALIDATION.md` comprueba que los CSV, figuras y documentos citados existan en la rama final o en su copia consolidada. Por tanto, el texto del informe usa preferentemente rutas `report/evidence/csv/...` y `report/figures/...`, aunque conserva referencias históricas a ramas cuando son necesarias para reproducción.

## 8. Protocolo experimental

- **Lenguaje:** C para solver principal; Python para wrappers y figuras.
- **Solver:** Gurobi Optimizer 12.0.0 (`gurobi_cl --version`) y logs con licencia académica.
- **Hardware:** Apple M1, 8 GB RAM, macOS/Darwin 25.5.0 (según `report/evidence/metadata/hardware_software_probe.txt`).
- **Límite de tiempo:** 300 segundos externos por instancia.
- **Evidencia:** CSV + logs crudos + figuras PNG.
- **Estados usados:** `OPT_MATCH`, `OPTIMAL_NO_KNOWN`, `OPTIMAL`, `TIMEOUT`, `ERROR`, `PARSE_WARNING`.

Familias y campañas consideradas:

- `toy1`, para validación pequeña.
- OR-Library `pmed1`–`pmed15` en campaña principal.
- OR-Library `pmed16` como smoke test adicional oficial.
- TSPLIB `rl1304` con p-grid `5,10,20,50,100,200,300,400,500`.
- TSPLIB `kroA100` sin óptimo externo suministrado.
- Línea base monolítica F1 en cinco instancias.
- Trazas de gap de Fase 1 en cuatro instancias.
- Estrés sintético euclidiano con `N = 100,250,500,1000,2000,5000` y `p = 5%,10%,20%`.

## 9. Resultados

### 9.1 Campaña Benders 300s

La campaña Benders principal contiene 26 filas: 1 toy, 15 OR-Library y 10 TSPLIB. Los estados fueron 25 `OPT_MATCH` y 1 `OPTIMAL_NO_KNOWN`; no hubo timeouts. El mayor tiempo total observado fue `14.191127` segundos en `rl1304_p10`.

Las 15 instancias OR-Library `pmed1`–`pmed15` coincidieron con óptimos oficiales. Las 9 instancias `rl1304` coincidieron con los óptimos de la tabla del paper incorporados al wrapper. `kroA100` fue resuelta localmente con objetivo 30539, pero se reporta como `OPTIMAL_NO_KNOWN` porque el wrapper no recibió un óptimo confiable externo.

### 9.2 OR-Library

La evidencia local verificó `pmed1`–`pmed15` en la campaña principal. Posteriormente se hizo un smoke test oficial de `pmed16`: se descargó desde OR-Library, se convirtió a `.pmp`, y se resolvió bajo timeout externo de 300 segundos. El resultado fue `OPT_MATCH` con objetivo 8162, coincidente con el óptimo oficial, en `0.793458` segundos. Este smoke test muestra que la expansión a `pmed17`–`pmed40` es factible, pero no autoriza afirmar que la campaña completa pmed1–pmed40 ya esté hecha.

### 9.3 TSPLIB

La evidencia TSPLIB local cubre `rl1304` con 9 valores de `p` y `kroA100`. En `rl1304`, todos los valores del p-grid disponible coincidieron con los óptimos usados como referencia. En `kroA100`, el solver obtuvo una solución óptima local según Gurobi, pero el resultado se clasifica como `OPTIMAL_NO_KNOWN` por no contar con óptimo externo suministrado en el wrapper.

No se ejecutaron localmente TSPLIB grandes o enormes como `d2103`, `pcb3038`, `fl3795`, `rl5934`, `usa13509` o instancias mayores. Existen archivos raw locales para `fl1400`, `u1432` y `vm1748`, pero requieren preprocessing y definición de p-grid antes de usarse en resultados defendibles.

### 9.4 Línea base monolítica F1

La línea base F1 se ejecutó en cinco instancias: `toy1`, `pmed1`, `pmed2`, `pmed6` y `kroA100`. Todas terminaron con `OPTIMAL` y `timeout_flag=0`. El mayor tiempo fue `6.991906` segundos para `pmed6`. La comparación con Benders muestra que, salvo `toy1`, Benders tuvo menor tiempo local en estas cinco instancias. Esta comparación debe interpretarse como evidencia local limitada, no como comparación contra Zebra ni contra el benchmark C del paper.

### 9.5 Trazas de gap

La rama de trazas generó CSVs de Fase 1 para `toy1`, `pmed1`, `pmed6` y `rl1304 p=5`. En `pmed1`, el gap de Fase 1 cerró a 0 en 6 iteraciones; en `rl1304 p=5`, también cerró a 0 en 6 iteraciones. En `pmed6`, la Fase 1 terminó sin cortes violados pero con gap de Fase 1 `0.010614`; esto no es falla de optimalidad global, porque la certificación exacta se obtiene en Fase 2.

Debe distinguirse entre gap de Fase 1 `(UB-LB)/UB`, gap del CSV Benders calculado respecto de LB1 y objetivo final, y gap MIP de Gurobi en la línea monolítica. No son métricas idénticas.

### 9.6 Estrés sintético

La campaña sintética generó 18 instancias euclidianas determinísticas con semilla `20260622`: `N = 100,250,500,1000,2000,5000` y `p = 5%,10%,20%`. Todas terminaron bajo 300 segundos, sin timeouts. El mayor tiempo fue `44.247668` segundos en `euclidean_N5000_p5pct`, con 292 nodos y 6874 cortes lazy. Como no existen óptimos externos para estas instancias, los estados son `OPTIMAL_NO_KNOWN`; sirven como evidencia de escalabilidad local y estrés computacional, no como replicación de benchmarks del paper.

### 9.7 Respuesta explícita de escalabilidad

Con evidencia local y protocolo de 300 segundos, el método Benders resolvió:

- OR-Library hasta `N=400` en `pmed16` smoke.
- TSPLIB `rl1304` con `N=1304` en varios valores de `p`.
- Instancias sintéticas euclidianas hasta `N=5000`, con máximo observado 44.25 s.

La línea base monolítica F1 solo fue probada hasta `N=200` en OR-Library (`pmed6`) y `N=100` en TSPLIB (`kroA100`). Esto no significa que F1 no pueda resolver más, sino que la evidencia local de F1 es mucho más acotada. El comportamiento observado apoya la intuición de que el maestro Benders, al evitar variables de asignación `x_ij`, escala mejor en estas pruebas locales.

## 10. Visualizaciones

Las figuras recomendadas para el informe están mapeadas en `report/REPORT_FIGURE_MAP.md`. Las más relevantes son:

- Runtime Benders por instancia.
- Nodos Benders por instancia.
- Cortes lazy por instancia.
- Runtime vs `N`.
- Runtime Benders vs monolítico F1.
- Gap vs iteración en `pmed1`.
- Cotas LB/UB vs iteración en `pmed1`.
- Runtime sintético vs `N`.

Para explicación visual de la instancia toy se incluye la figura didáctica `report/figures/toy_pmedian_explanation.png`. La figura muestra cuatro puntos en rectángulo, dos medianas seleccionadas y arcos de asignación con costos. Su función es pedagógica: no es un resultado experimental, sino una ayuda visual para interpretar sitios candidatos, medianas abiertas, clientes asignados y costos de servicio.

## 11. Discusión

La ventaja computacional observada de Benders proviene de separar apertura y evaluación de asignación. El modelo F1 mantiene variables `x_ij` para todos los pares cliente-sitio; Benders conserva un maestro más pequeño y agrega cortes solo cuando detecta subestimaciones. Esto es especialmente relevante cuando `N` y `M` crecen.

La separación por cliente permite explotar estructura: dado `y`, cada cliente se evalúa independientemente usando su lista ordenada de sitios. Los cortes generados aproximan la función de costo de asignación desde abajo. En la Fase 1, esta aproximación produce una cota inferior LP y una cota superior por redondeo. En la Fase 2, las variables binarias y los lazy cuts permiten certificar optimalidad en las instancias resueltas.

El timeout externo de 300 segundos es importante porque hace comparables los experimentos dentro del proyecto. Un resultado sin timeout externo no debe mezclarse con los resultados reportados como campaña 300s.

El estrés sintético es útil porque muestra comportamiento hasta `N=5000`, pero no reemplaza benchmarks del paper. Las instancias sintéticas tienen distribución específica y no tienen óptimos externos. Del mismo modo, `rw12` no representa la campaña RW grande del paper.

La evidencia experimental está dividida por ramas, lo que protege la limpieza del desarrollo pero exige trazabilidad estricta. Esta decisión es defendible si el informe cita rutas, ramas y commits, y si no mezcla resultados no comparables.

## 12. Comparación con el paper

| Componente del paper | Estado local | Evidencia | Comentario |
|---|---|---|---|
| Núcleo Benders F3/F4 | Verified local | `src/phase1.c`, `src/phase2.c`, `src/separation.c`, logs callback | Replicación del mecanismo central, no de todos los refinamientos. |
| Fase 1 | Verified local | `report/evidence/csv/benders_300s_campaign.csv`, gap traces | LP con cortes y cotas LB/UB. |
| Fase 2 branch-and-Benders-cut | Verified local | logs con `[CALLBACK]`, `lazy_cuts` | Lazy constraints de Gurobi. |
| OR-Library | Partial/verified subset | pmed1–pmed15, pmed16 smoke | No está completa pmed1–pmed40. |
| TSPLIB `rl1304` | Verified local | 9 valores de `p` | Coincide con óptimos usados como referencia. |
| `kroA100` | Partial local | CSV Benders y F1 | Sin óptimo externo suministrado. |
| PopStar | Not implemented | docs/audits | Se usa redondeo, no PopStar. |
| Zebra | Paper-only / not available locally | source audit | No ejecución local; no afirmar superioridad. |
| Constraint reduction | Not implemented | matrix audit | Futuro trabajo. |
| Reduced-cost fixing | Not implemented | matrix audit | Futuro trabajo. |
| BIRCH | Not run | source audit | No campaña local exacta. |
| RW | Partial local | `rw12` y generador | No RW grande paper. |
| ODM | Not implemented / not run | matrix audit | Requiere soporte de asignaciones prohibidas. |
| Huge TSPLIB | Not run | source audit | Riesgo de memoria/tiempo. |

## 13. Limitaciones

1. La replicación es parcial, no completa.
2. Zebra no fue construido ni ejecutado localmente.
3. PopStar no fue implementado; se usa redondeo simple para cotas superiores.
4. No se implementaron reduced-cost fixing ni constraint reduction.
5. No se ejecutaron campañas completas BIRCH, RW grande u ODM.
6. No se ejecutaron TSPLIB enormes.
7. Las instancias sintéticas no tienen óptimos externos.
8. Las comparaciones de tiempo dependen de hardware, Gurobi, licencia, carga del sistema y wrappers.
9. Parte de la evidencia vive en ramas separadas.
10. La línea base monolítica F1 es local y limitada; no equivale al benchmark Zebra ni al código C del paper.

## 14. Conclusiones

El proyecto implementa y valida el núcleo de una descomposición de Benders para el problema p-mediana: maestro con `y_j` y `theta_i`, separación cerrada por cliente, cortes de optimalidad, Fase 1 LP y Fase 2 branch-and-Benders-cut con callbacks lazy. La evidencia experimental muestra que el método reproduce óptimos conocidos en OR-Library pmed1–pmed15, en `rl1304` para el p-grid disponible, y en el smoke test oficial `pmed16`. Además, resuelve una grilla sintética hasta `N=5000` bajo el protocolo de 300 segundos.

La comparación con F1 cumple una función pedagógica: muestra cómo el modelo clásico crece con variables de asignación, mientras Benders mantiene un maestro más compacto y agrega información por cortes. Las trazas de gap ayudan a interpretar cotas y relajación, conectando teoría con implementación.

El trabajo no debe presentarse como replicación completa del paper. Faltan componentes relevantes: Zebra, PopStar, reducciones, fixing, BIRCH/RW/ODM completos y TSPLIB enormes. Aun así, como proyecto de Optimización Computacional, la entrega es defendible porque conecta formulación, relajación, cotas válidas, descomposición, implementación, experimentación y auditoría crítica.

## Referencias

- Duran-Mateluna, C., Ales, Z., & Elloumi, S. (2023). *An efficient Benders decomposition for the p-median problem*. European Journal of Operational Research, 308, 84–96. [VERIFICAR FORMATO APA/BIBTEX]
- ReVelle, C. S., & Swain, R. W. (1970). Central facilities location. [VERIFICAR DATOS COMPLETOS]
- Beasley, J. E. (1985/OR-Library). OR-Library p-median benchmark instances. `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/pmedinfo.html` [VERIFICAR CITA]
- Reinelt, G. (1991). TSPLIB—A traveling salesman problem library. [VERIFICAR FORMATO]
- Gurobi Optimization, LLC. Gurobi Optimizer Reference Manual. [VERIFICAR VERSIÓN Y CITA]
