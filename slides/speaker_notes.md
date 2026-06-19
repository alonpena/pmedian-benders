# Notas del orador — Presentación final (≈15 min, 8 diapositivas)

**Mensaje de alcance:** replicación algorítmica completa del mecanismo central + replicación computacional parcial documentada. No decir “nuestra implementación supera a Zebra”. Decir: el paper reporta esa comparación; Zebra no fue reejecutado localmente.

> Objetivo: comunicar problema, modelo, método y resultados con lenguaje simple pero riguroso.
> Tiempo sugerido por slide entre paréntesis. Todos los números provienen de `results/`.

---

## Slide 1 — Problema y motivación (≈1.5 min)
**Qué decir:** "El problema de las *p*-medianas pregunta: dado un conjunto de clientes y de
ubicaciones candidatas, ¿qué *p* ubicaciones abro para minimizar la suma de distancias de cada
cliente a la abierta más cercana?" Dar un ejemplo concreto: bodegas en una ciudad, o refugios de
emergencia. Recalcar la idea central: **una vez fijadas las ubicaciones, cada cliente decide
trivialmente** (la más cercana); lo difícil es la elección combinatoria.
**Clave a transmitir:** qué decisión real apoya el modelo. No entrar aún en matemática.

## Slide 2 — Dificultad computacional (≈1.5 min)
**Qué decir:** "Es NP-duro: elegir *p* de *M* son combinatorias $\binom{M}{p}$. La formulación
clásica F1 tiene del orden de $N\times M$ variables; para 10.000 puntos son cien millones —
inviable." Luego el giro: "En vez de fuerza bruta, **explotamos estructura**: si fijamos qué
sitios abrir, el problema se separa por cliente."
**Clave:** justificar *por qué* hace falta descomposición; sembrar lagrangiana y Benders.

## Slide 3 — Formulaciones F1/F2/F3/F4 (≈2 min)
**Qué decir:** Recorrer la tabla sin leerla entera. "F1 es la directa pero densa. F2 reescribe el
costo como **suma telescópica de peajes**: cada cliente paga la diferencia entre radios mientras
no aparezca un sitio abierto. F3 es F2 con la matriz mucho más rala — la mejor en la práctica. F4
es la forma compacta con una variable $\theta_i$ por cliente."
**Punto fuerte a enfatizar:** las cuatro tienen **el mismo óptimo y la misma relajación LP**;
lo que cambia es la **densidad**, y eso decide el rendimiento. F3 es la base de Benders.
**Si preguntan:** el objetivo telescópico se verifica con un ejemplo (distancias 2,5,9 → costo
$2+3z^1+4z^2$).

## Slide 4 — Relajación lagrangiana (≈2 min)
**Qué decir:** "Esta es la propuesta teórica de relajación. Relajamos la restricción de
asignación llevándola al objetivo con precios $\lambda_i$. El resultado se separa **por sitio**:
cada sitio tiene una contribución $\beta_j$, y abrimos los *p* más negativos — por inspección,
sin solver." Mencionar: cota inferior $L(\lambda)\le$ óptimo, se mejora con subgradiente; la
recuperación primal asigna cada cliente al sitio abierto más cercano para un UB.
**Clave (para preguntas individuales):** contraste con Benders — lagrangiana separa por sitio,
Benders por cliente; ambas producen cota inferior por caminos distintos.

## Slide 5 — Descomposición de Benders (≈2.5 min, núcleo)
**Qué decir:** "El maestro decide solo $y$ (qué abrir) y estima la distancia de cada cliente con
$\theta_i$. Las variables $z$ desaparecen. Cada vez que el maestro propone una solución, el
subproblema de cada cliente devuelve un **corte** que obliga a $\theta_i$ a no subestimar la
distancia real."
**Los dos mensajes que no pueden faltar:**
1. **Solo cortes de optimalidad.** El subproblema siempre es factible y acotado (podemos hacer
   $z$ grande; objetivo con coeficientes positivos). Por eso su dual nunca es no acotado y
   **nunca hacen falta cortes de factibilidad**. Esto simplifica todo.
2. **Forma cerrada.** El dual se resuelve con una fórmula (el índice $\tilde k_i$), así que el
   corte se separa en $O(NM)$ **sin resolver ningún LP**.
**Validez:** cada corte es una cota inferior válida (no elimina el óptimo) y hay un número finito
de cortes → el branch-and-cut termina con el óptimo exacto.

## Slide 6 — Implementación (≈1.5 min)
**Qué decir:** "Núcleo en C independiente del solver, una capa delgada para Gurobi, y un oráculo
en Python para validar." Mostrar el mapeo matemática→módulo sin leerlo todo: "$\tilde k_i$ y el
corte están en `separation.c`; las dos fases en `phase1.c` y `phase2.c`." Explicar las dos fases:
Fase 1 resuelve el LP del maestro con cortes y redondeo; Fase 2 es branch-and-Benders-cut con un
callback de *lazy constraints*.
**Enfatizar fuerte:** "El separador, que es el corazón del método, lo **verificamos por tres vías
independientes**: lo derivamos a mano en una instancia chica, lo comparamos con un test unitario
en C, y lo cruzamos contra el oráculo Python — con **cero diferencias**." Esto da credibilidad a
todos los resultados.

## Slide 7 — Resultados (≈2 min)
**Qué decir:** "En las 15 instancias OR-Library alcanzamos el **óptimo oficial exacto**, brecha
cero. En `rl1304`, con hasta 1304 puntos y *p* hasta 500, reproducimos los **9 óptimos del
paper** exactamente." Mostrar que el callback es real: cortes lazy > 0 (no degenera a B&B normal).
Luego warm-start: "Heredar los cortes de Fase 1 baja los nodos de cientos a uno o siete." Ser
**honesto**: "El tiempo de pared es mixto en estas instancias sub-segundo, porque precargar
cientos de cortes a veces cuesta más de lo que ahorra; el beneficio se espera en instancias
grandes, que no medimos."
**Insight a remarcar:** muchas instancias ya quedan resueltas en Fase 1 ($LB_1=UB_1=$ óptimo); la
Fase 2 solo certifica.

## Slide 8 — Conclusiones (≈1.5 min)
**Qué decir:** Cerrar con aprendizajes, no con números.
- "La formulación importa más que el solver: mismo óptimo y misma cota LP, pero la densidad
  decide qué es resoluble."
- "La combinación separación $O(NM)$ en forma cerrada + solo cortes de optimalidad hace el método
  simple y rápido."
- "Las buenas cotas tempranas son útiles para decidir con tiempo limitado en un caso real."
**Limitaciones (decirlas, suma credibilidad):** escala probada hasta $N=1304$; no reejecutamos
Zebra ni las familias enormes; PopStar, reduced-cost fixing y constraint reduction quedaron fuera
del alcance. La comparación con Zebra es literatura del paper, no resultado local.
Terminar invitando preguntas.

---

## Preparación para preguntas individuales (40% de la nota oral)
Dominar para responder en vivo:
1. **¿Por qué solo cortes de optimalidad?** Porque $SP_i(\bar y)$ es siempre factible (se puede
   hacer $z$ grande) y acotado (coeficientes $\ge 0$, minimización); su dual nunca es no acotado.
2. **¿Cómo se obtiene el corte sin resolver el dual?** Por la solución cerrada: se calcula
   $\tilde k_i$ (último radio no cubierto) recorriendo la matriz $S$ (Alg. 2, $O(M)$), y de ahí
   $\OPT(SP_i)$ y los coeficientes $D^{\tilde k+1}_i - d_{ij}$.
3. **¿Por qué $O(NM)$?** $\tilde k_i$ cuesta $O(M)$ por cliente; $N$ clientes → $O(NM)$ por
   separación, sin LP.
4. **¿Qué conecta maestro y subproblema?** Las $y$ (qué sitios abrir) van del maestro al
   subproblema; los cortes (cotas de $\theta_i$ en función de $y$) vuelven al maestro.
5. **¿Lagrangiana vs Benders?** Lagrangiana relaja la asignación y separa por sitio; Benders fija
   $y$ y separa por cliente. Ambas dan cota inferior.
6. **¿Por qué F3 y no F1/F2/F4?** Misma cota LP que todas, pero matriz rala → el solver la maneja
   mejor; F4 entera es lenta por densidad, por eso generamos sus cortes al vuelo.
7. **¿Cómo sabemos que el código es correcto?** Separador verificado por mano + test + oráculo
   Python (0 diffs); 15/15 óptimos OR-Library; 9/9 óptimos `rl1304` vs paper.

---

## Lista de chequeo manual antes de exponer / entregar
- [ ] `make clean && make pmedian` sin warnings.
- [ ] `make test` → `RESULT: PASS` (ambos tests).
- [ ] `python scripts/verify_cuts.py` → `PASS` (0 diffs).
- [ ] `pdflatex report/main.tex` (×2) compila; las 4 figuras `plot_*.png` se incrustan.
- [ ] `pdflatex slides/main.tex` compila las 8 diapositivas.
- [ ] Números de las tablas del informe/slides coinciden con los CSV en `results/`.
- [ ] Ensayar cronometrado: ~15 min, sin leer las diapositivas.
- [ ] Cada integrante puede responder las 7 preguntas de arriba.
- [ ] Tener a mano `docs/AUDIT.md` por si preguntan por evidencia de algún número.
