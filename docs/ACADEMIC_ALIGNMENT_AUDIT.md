# Auditoría de alineación académica — Informe final (Optimización Computacional, PUCV)

> Revisor: investigador senior de Investigación de Operaciones.
> Objetivo: medir el informe contra la **estructura intelectual del curso**
> (Estructura → Relajación → Dualidad → Cotas → Descomposición → Algoritmo →
> Validación computacional) y contra la **fidelidad de replicación** del paper
> Duran-Mateluna, Ales \& Elloumi (2023). La implementación es **evidencia**, no
> la contribución. Fuentes: `report/`, `docs/Course Notes/*.md`, `docs/AUDIT.md`,
> `PMEDIAN_BENDERS_PROJECT_BRIEF.md`. Estado: pre-upgrade (2026-06-19).

---

## PARTE A — Alineación con la estructura del curso

Cadena pedagógica esperada y dónde vive en el informe:

| Eslabón del curso | Sección(es) del informe | ¿Cubierto? |
|---|---|---|
| ESTRUCTURA (qué acopla) | 01 motivación, 02 definición, 03 (F1 análisis estructural) | 🟡 implícito |
| RELAJACIÓN (LP y lagrangiana) | 03 (relajación LP), 04 lagrangiana | 🟡 LP poco explícita |
| DUALIDAD (débil/fuerte, ptos/rayos extremos) | 05 Benders (dual SP), 04 (dual lagrangiano) | 🔴 vocabulario ausente |
| COTAS (LB/UB, gap, brecha integridad) | 09–10 resultados | 🟡 sin marco conceptual |
| DESCOMPOSICIÓN (maestro/subproblema) | 05 Benders, 06 separación | 🟢 fuerte |
| ALGORITMO (dos fases, B\&Bc) | 07 implementación | 🟢 fuerte |
| VALIDACIÓN COMPUTACIONAL | 09 experimentos | 🟢 fuerte |

### Evaluación sección por sección

**01_motivacion.tex**
1. *Concepto enseñado:* localización discreta, NP-dureza, motivación de descomponer.
2. *Concepto del curso:* "Estructura" (Cap. 1) — qué decisiones acoplan.
3. *¿Implementación-pesada?* No.
4. *¿Rigor de posgrado?* Suficiente como motivación.
5. *Falta:* enunciar de entrada que el trabajo es **replicación/validación** del paper, no un proyecto de software; un esquema/figura del sistema.

**02_definicion.tex**
1. Definición formal del pMP; estructura "fija $y$ ⇒ separa por cliente".
2. "Estructura del problema" / restricciones complicantes.
3. No.
4. Sí.
5. Falta nombrar explícitamente "variables complicantes" con el lenguaje del Cap. 3 (decisiones de diseño $x$ vs operacionales $y$).

**03_formulaciones.tex (F1–F4)**
1. Modelado MILP; formulaciones fuertes vs débiles; misma relajación LP, distinta densidad.
2. "Programación entera y formulaciones" + "brecha de integridad" (Cap. 1).
3. No.
4. Casi: falta conectar con **"formulación fuerte ⇒ relajación LP ajustada ⇒ menos nodos B\&B"** (vocabulario exacto del Cap. 1, p. 23/27). F2 merece más espacio (idea de radio/umbral + objetivo telescópico antes del álgebra).
5. Falta: (a) decir que F1–F4 comparten relajación LP pero la **fortaleza práctica** viene de la densidad; (b) **por qué F2 mejora a F1** y **por qué F3 mejora a F2** como subsecciones nombradas; (c) la palabra "brecha de integridad".

**04_lagrangiana.tex**
1. Relajación lagrangiana completa (complicantes, $L$, dual, subgradiente, recuperación primal).
2. Cap. 2 entero.
3. No (es teórica, como pide la pauta).
4. Sí — es el capítulo más alineado con el curso.
5. Falta menor: usar el símbolo del curso ($\theta(\lambda)$ para la función dual; paso de **Polyak** explícito $\alpha_k=\beta\frac{UB-\theta(\lambda^k)}{\lVert s^k\rVert^2}$), y **dualidad débil** $\theta(\lambda)\le z^\star$ nombrada como tal.

**05_benders.tex**
1. Maestro, $SP_i$ primal, $DSP_i$ dual, corte, optimalidad vs factibilidad.
2. Cap. 3 entero.
3. No.
4. Sí en lo específico del pMP; **pero** desconectado del **andamiaje canónico del curso**: el Cap. 3 enseña Benders sobre la forma $\min c^\top x+\eta$, recurso $\theta(x)$, corte de optimalidad $\eta\ge\pi^{\star\top}(b-Ax)$, $\Pi=\{\pi\ge0:B^\top\pi\le d\}$ con **finitos puntos/rayos extremos** ⇒ terminación finita.
5. **Falta (ALTA):** un puente explícito "Benders genérico del curso → Benders del pMP" usando $\eta\equiv\sum_i\theta_i$, puntos extremos ⇒ cortes de optimalidad, rayos extremos ⇒ (aquí inexistentes) cortes de factibilidad; y la subsección **"¿por qué este Benders es mejor que el clásico?"**.

**06_separacion.tex**
1. Forma cerrada del dual, $\tilde k_i$, $O(NM)$, verificación 3 vías.
2. Núcleo del paper (no hay capítulo equivalente; es la contribución).
3. Algo (pseudocódigo C), pero justificado.
4. Sí.
5. Falta: enmarcar la forma cerrada como **"el subproblema tiene estructura especial ⇒ no se resuelve LP"** (condición del Cap. 3, p. 26, "subproblema con estructura especial que lo hace rápido").

**07_implementacion.tex**
1. Arquitectura, mapa matemática→C, dos fases.
2. Algoritmo (branch-and-Benders-cut, Cap. 3 p. 28).
3. **Sí, implementación-pesada** (apropiado aquí, pero debe quedar marcado como "evidencia").
4. N/A (es ingeniería).
5. Falta: (a) frase de encuadre "diseño modular con encapsulación por structs e interfaces, inspirado en principios de orientación a objetos" (C no es OO); (b) distinguir **warm-start = heredar cortes/cotas de Fase 1**, NO preprocesamiento de $S$/$D_i^k$; (c) decir que el esquema de dos fases **es el método del paper (Sección 3.5)**.

**08_instancias.tex**
1. Familias, supuestos, caso base.
2. "Instancias y datos" (pauta A5).
3. No.
4. Sí.
5. Falta: aclarar que OR-Library aparece **porque el paper la usa como benchmark estándar**, no como eje del trabajo.

**09_experimentos.tex / 10_resultados.tex**
1. Validación: óptimos, cotas, nodos, cortes, warm-start.
2. "Cotas + buenas soluciones" / validación computacional (pauta A6–A7).
3. No.
4. Sí, con datos reales trazables.
5. Falta: nombrar **brecha de integridad**, **LB/UB**, **gap** con el vocabulario del curso; presentar la validación como "la teoría predice X, el experimento confirma X".

**11_reproducibilidad.tex**
1. Entorno, comandos, trazabilidad, honestidad.
2. Reproducibilidad (pauta A8).
3. Sí (apropiado).
4. N/A.
5. Sin brechas.

---

## PARTE B — Auditoría de replicación del paper

¿El informe está centrado en el **paper** o derivó hacia OR-Library / software?

| Tema científico | ¿Dónde se explica? | Estado |
|---|---|---|
| 1. Contribución científica del paper | 01 (1 párrafo) | 🟡 superficial — falta sección dedicada |
| 2. Por qué F2 mejora a F1 | 03 (mencionado) | 🟡 sin subsección nombrada |
| 3. Por qué F3 mejora a F2 | 03 (mencionado: densidad/esparsidad) | 🟡 correcto pero breve |
| 4. Por qué Benders sobre F3 > Benders clásico | — | 🔴 **AUSENTE — ALTA PRIORIDAD** |
| 5. Procedimiento de separación $O(NM)$ | 06 (completo) | 🟢 fuerte |
| 6. Por qué solo cortes de optimalidad | 05 §5.6 (completo) | 🟢 fuerte |

**Veredicto:** el informe **no** derivó hacia software (la implementación está bien
acotada como evidencia), pero **sí** está sub-enmarcado como replicación: OR-Library
recibe protagonismo de tabla sin que se diga que es el benchmark del paper, y falta la
pieza central de venta del paper (**por qué este Benders supera al clásico**).

**Acciones HIGH PRIORITY:**
- Añadir subsección **"Contribución del paper"** (eje narrativo).
- Añadir subsección **"¿Por qué este Benders es mejor que el clásico?"** (5 razones).
- Renombrar subsecciones de F2/F3 a **"Por qué F2 mejora a F1"** / **"Por qué F3 mejora a F2"**.
- Encuadrar OR-Library/TSPLIB como **benchmarks estándar del paper**.

---

## PARTE C — Integración de vocabulario del curso

| Tema del curso | Presente | Falta | Sección (post-upgrade) |
|---|---|---|---|
| Calidad de la relajación LP | 🟡 parcial | nombrarla "formulación fuerte/débil" | 03 |
| Cotas inferior/superior (LB/UB) | 🟡 en tablas | marco conceptual | 03, 09, 10 |
| Dualidad (general) | 🟡 en SP dual | conectar con Cap. 1 | 05 |
| Dualidad **débil** | 🔴 | $\theta(\lambda)\le z^\star$, $b^\top y\le c^\top x$ | 04, 05 |
| Dualidad **fuerte** | 🔴 | $v(P)=v(D)$ ⇒ corte de optimalidad exacto | 05 |
| Puntos extremos | 🔴 | corte de optimalidad ↔ punto extremo del dual | 05 |
| Rayos extremos | 🔴 | corte de factibilidad ↔ rayo extremo (aquí inexistente) | 05 |
| Cortes de factibilidad | 🟡 mencionado | contraste explícito con el curso | 05 |
| Cortes de optimalidad | 🟢 | — | 05, 06 |
| Relajación lagrangiana | 🟢 | — | 04 |
| Optimización por subgradiente | 🟢 | paso de Polyak con símbolo del curso | 04 |
| Branch-and-Bound | 🔴 | nombrar arquitectura B\&B (nodos, poda LB≥UB) | 05, 07, 09 |
| Branch-and-cut / branch-and-Benders-cut | 🟡 | usar el término del Cap. 3 p. 28 | 05, 07 |
| Filosofía de descomposición | 🟡 | "trasladar dificultad a interacción maestro–subproblema" | 05 |
| Brecha de integridad | 🔴 | $\text{gap}=v(\text{MILP})-v(\text{LP})$ | 03, 10 |

**Veredicto:** la mitad del vocabulario dual/cotas del curso no aparece con su nombre.
El contenido técnico es correcto, pero el informe **no habla el idioma conceptual del
curso**. Corregible con inserciones quirúrgicas (no requiere reescritura).

---

## PARTE D — Auditoría de afirmaciones de implementación

| Afirmación | Verificable en código | Veredicto |
|---|---|---|
| ¿Implementación orientada a objetos? | C no es OO | **FALSO si se afirma** — pero **no se afirma** en el informe actual (grep sin coincidencias). Encuadre correcto: "diseño modular con encapsulación por structs e interfaces". |
| Diseño modular procedural con capas de abstracción | `src/solver.h` (interfaz opaca `Solver`/`SolverCB`), `src/*.c` | **VERDADERO** — `struct Solver` opaco, núcleo sin headers del solver. |
| Warm-start = heredar cortes de Fase 1 (método del paper) | `src/phase2.c:64–77` (`phase2_run(..., const CutPool *warm)` precarga `warm->cuts` como restricciones), `src/cutpool.c`, `src/phase1.c:39` (`cutpool_add`) | **VERDADERO**. Es transferencia de información de Fase 1, **no** preprocesamiento de tablas de distancia / $D_i^k$ / matriz $S$. |
| ¿"Warm-start" se refiere a preprocesamiento? | — | **NO**. La construcción de $S$ (`sortsites_build`) es preprocesamiento aparte, anterior a ambas fases; no es lo que se llama warm-start. La distinción debe quedar **explícita** en el texto. |
| Separación $O(NM)$ implementada (Alg. 1 y 2) | `src/separation.c` (`separation_k_tilde`, `separation_client`, `separation_all`) | **VERDADERO** y verificado 3 vías (`docs/AUDIT.md` 14–15). |
| Fase 2 es branch-and-Benders-cut real | `src/phase2.c:36–44` callback + `results/logs/*.log` (`lazy_cuts>0`) | **VERDADERO**. |
| Cada algoritmo documentado ↔ código real | Mapa en `07_implementacion.tex` coincide con archivos/funciones | **VERDADERO** (revisado símbolo por símbolo). |
| MIPGap $=10^{-10}$ | `src/phase2.c:80` | **VERDADERO**. |
| Distancia euclidiana floor | `src/instance.c` `instance_dist` | **VERDADERO**. |

**Afirmaciones que NO se pueden verificar desde el código fuente (declarar o evitar):**
- Tiempos de **Zebra** (no se ejecutó; son del paper).
- Escalabilidad a $>10^4$ puntos (no corrida).
- Ventaja en **wall-time** del warm-start a gran escala (solo medida reducción de nodos en sub-segundo; ya declarado UNVERIFIED en `docs/AUDIT.md`).
- PopStar, reduced-cost fixing, constraint reduction (no implementados).
- Backends CPLEX/SCIP (no compilados).

**Conclusión Parte D:** ninguna afirmación falsa presente; el único riesgo es el de
**lenguaje** ("OO") y el de **ambigüedad** (warm-start vs preprocesamiento). Ambos se
corrigen con texto, sin tocar código.

---

## Síntesis

- El informe es **técnicamente correcto** y bien soportado por datos reales.
- Brechas dominantes: **(i)** no habla el vocabulario dual/cotas del curso; **(ii)** falta
  el puente "Benders del curso → Benders del pMP"; **(iii)** falta la venta científica
  del paper (por qué F2>F1, F3>F2, y por qué este Benders > clásico); **(iv)** encuadre
  como replicación, no como software.
- Todo es **corregible por adición/edición quirúrgica**, preservando lo ya escrito.
- Plan priorizado en `docs/REPORT_UPGRADE_PLAN.md`.
