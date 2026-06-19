# Plan de mejora del informe — ordenado por impacto en la nota

> Objetivo: maximizar calidad académica, rigor teórico y fidelidad de replicación.
> **No** escribir código nuevo. Preservar todo lo correcto ya escrito; estas son
> ediciones quirúrgicas. Prioridad por impacto en la pauta (`docs/Pauta_entregaFinal.pdf`)
> y en la alineación con el curso (`docs/Course Notes/`). Estado de ejecución al final.

Leyenda: ✅ aplicado en este pase · ⬜ pendiente (acción del autor).

---

## CRITICAL — mueven los criterios de mayor peso (Benders 5.0 + Formulación 3.0)

**C1. Puente "Benders del curso → Benders del pMP".** ✅
Conectar la forma canónica del Cap. 3 ($\min c^\top x+\eta$, recurso $\theta(x)$ convexo,
corte $\eta\ge\pi^{\star\top}(b-Ax)$, $\Pi$ con finitos puntos/rayos extremos ⇒ terminación
finita) con el caso pMP ($\eta\equiv\sum_i\theta_i$). Sección 05.

**C2. Subsección "¿Por qué este Benders es mejor que el clásico?"** ✅
Cinco razones: (a) parte de la formulación fuerte **F3**; (b) el subproblema tiene
estructura especial; (c) no se resuelve ningún LP; (d) separación en forma cerrada
$O(NM)$; (e) subproblema siempre factible y acotado ⇒ **solo cortes de optimalidad**.
Sección 05 (nueva subsección).

**C3. "Por qué F2 mejora a F1" y "Por qué F3 mejora a F2" como subsecciones nombradas.** ✅
F2 con la mayor extensión: idea de radio/umbral de distancia + objetivo telescópico
**antes** del álgebra. Sección 03.

**C4. Vocabulario de dualidad del curso.** ✅
Insertar y **nombrar**: dualidad débil ($\theta(\lambda)\le z^\star$; $b^\top y\le c^\top x$),
dualidad fuerte ($v(P)=v(D)$ ⇒ el corte de optimalidad es exacto en $\bar y$), punto
extremo ↔ corte de optimalidad, rayo extremo ↔ corte de factibilidad (aquí inexistente).
Secciones 04 y 05.

---

## HIGH — encuadre de replicación y método (Formulación 3.0 + Experimentos 4.0)

**H1. Reencuadre global como replicación/validación del paper.** ✅
Narrativa: teoría del curso → formulaciones → **contribución del paper** → implementación
→ validación → experimentos. Nueva subsección "Contribución del paper" en Sección 01.

**H2. Sección de literatura con las referencias que el propio paper cita.** ✅
ReVelle \& Swain (1970, F1), Cornuejols–Nemhauser–Wolsey (1980, F2), Elloumi (2010, F3),
García–Labbé–Marín (2011, Zebra), Benders (1962), Fischetti et al. (2017, UFL). Nueva
sección 02bis (`02b_literatura.tex`).

**H3. Dos fases = método del paper (Sección 3.5); warm-start ≠ preprocesamiento.** ✅
Estado explícito: Fase 1 = relajación LP con loop de cortes (Algoritmo 3); Fase 2 =
branch-and-Benders-cut que **hereda los cortes de Fase 1**. Warm-start = heredar
cortes/cotas, **no** preprocesamiento de $S$/$D_i^k$ (eso es construcción de $S$, etapa
aparte). Sección 07.

**H4. Encuadrar OR-Library/TSPLIB como benchmarks estándar del paper.** ✅
Una frase en Sección 08 dejando claro que aparecen porque el paper las usa, no como eje.

---

## MEDIUM — pulido conceptual y comunicacional

**M1. Brecha de integridad nombrada.** ✅ ($\text{gap}=v(\text{MILP})-v(\text{LP})\ge0$;
F1–F4 misma relajación ⇒ misma brecha; la fortaleza práctica viene de la densidad).
Secciones 03 y 10.

**M2. Arquitectura B\&B nombrada.** ✅ (nodos, poda $LB\ge UB$, branch-and-cut,
branch-and-Benders-cut con el término del Cap. 3). Secciones 05/07/09.

**M3. Encuadre "implementación = evidencia" + frase OO correcta.** ✅
"diseño modular con encapsulación por structs e interfaces, inspirado en principios de
orientación a objetos" (C no es OO). Sección 07.

**M4. Paso de Polyak con el símbolo del curso.** ✅ Sección 04.

**M5. `docs/DEFENSA_ORAL.md` con las 8 preguntas más probables.** ✅

---

## LOW — opcional, sube presentación (A1) si hay tiempo

**L1. Figura/esquema del sistema (toy1: clientes → sitio abierto más cercano).** ⬜
Marcado con `\todo{FALTA: figura esquema del sistema}` en Sección 01.

**L2. Ejemplo numérico de subgradiente lagrangiano (una iteración) en `toy1`.** ⬜
Opcional; el desarrollo teórico ya está completo.

**L3. Glosario de notación (1 página) unificando $\theta_i$, $\eta$, $\theta(x)$.** ⬜
Mitiga choque de símbolos curso ($\eta$) vs paper ($\theta_i$).

---

## Requisitos de salida (Overleaf) — estado

- ✅ Paquetes estándar (amsmath, amssymb, booktabs, graphicx, hyperref, babel-spanish,
  enumitem, geometry, xcolor, listings). Sin shell-escape, sin dependencias exóticas.
- ✅ Figuras movidas a `report/figures/` con rutas relativas (`figures/plot_*.png`);
  `main.tex` autocontenido, compila top-to-bottom con `pdflatex` ×2.
- ✅ Excerptos de código en **Anexo** (no en el cuerpo) para acelerar compilación y foco.
- ✅ Macro `\todo{...}` (rojo inline) + lista consolidada al final de `main.tex`.
- ✅ Sin números fabricados: cada tabla cita su archivo en `results/`.

## Pendientes para el autor
- ⬜ L1, L2, L3 (opcionales, baja prioridad).
- ⬜ Compilar en Overleaf (no hay toolchain local) y revisar incrustación de las 4 figuras.
- ⬜ Decidir si se transcriben más tablas del paper (Tablas 3–9) — hoy fuera de alcance,
  declarado en `docs/AUDIT.md`.
