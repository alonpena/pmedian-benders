# Defensa oral — 8 preguntas probables del profesor

> Respuestas en español simple pero riguroso, de 3–4 frases, para memorizar.
> Alineadas con el vocabulario del curso (`docs/Course Notes/`). Complementa
> `slides/speaker_notes.md` (que trae 7 preguntas técnicas adicionales).

---

### 1. Explique la intuición de F2 (formulación de radios / umbral de distancia).
F2 deja de preguntar "¿a qué sitio mando cada cliente?" y pregunta "¿a qué **radio** alcanza
su sitio abierto más cercano?". Para cada cliente se ordenan sus distancias distintas
$D^1_i<D^2_i<\dots$ y la variable $z^k_i$ vale 1 mientras el cliente **aún no esté cubierto**
al radio $D^k_i$. El costo se arma como una **suma telescópica**: se parte pagando el radio
mínimo $D^1_i$ y se suma el incremento $D^{k+1}_i-D^k_i$ por cada anillo todavía no cubierto.
Es como pagar peajes crecientes hasta que aparece un sitio abierto, y ahí se deja de pagar.

### 2. ¿Por qué dos fases y no resolver el MILP directo?
Porque la formulación compacta F4 con todos los cortes es **densa** y pasársela entera al
solver es lento. La Fase 1 resuelve solo la **relajación lineal** del maestro agregando cortes
hasta que no haya violados: entrega buenas cotas $LB_1$ (la relajación) y $UB_1$ (redondeo).
La Fase 2 impone integralidad y resuelve con branch-and-Benders-cut, **heredando** los cortes
de Fase 1. Así se separa el trabajo barato (cotas) del caro (probar optimalidad).

### 3. ¿Qué es exactamente el warm-start aquí? ¿No es preprocesamiento?
Warm-start significa que la Fase 2 **arranca con el conjunto de cortes ya generados en la
Fase 1**, en vez de partir con el maestro vacío. Es transferencia de información entre fases,
exactamente el "warm start" que el Cap. 3 menciona como aceleración. **No** es preprocesamiento:
la construcción de la matriz $S$ y de los radios $D^k_i$ es una etapa previa, común a ambas
fases, y no tiene nada que ver con el warm-start.

### 4. ¿Por qué solo se necesitan cortes de optimalidad y nunca de factibilidad?
Porque el subproblema de cada cliente $SP_i(\bar y)$ es **siempre factible** (siempre se puede
poner $z$ grande) y **acotado** (objetivo con coeficientes positivos que se minimiza). En el
lenguaje del curso: el dual nunca es no acotado, así que su poliedro $\Pi$ no aporta **rayos
extremos**, solo **puntos extremos**. Los rayos extremos generan cortes de factibilidad y los
puntos extremos generan cortes de optimalidad; sin rayos, solo hay cortes de optimalidad.

### 5. ¿Qué representa la variable $\theta_i$ del maestro?
$\theta_i$ es la **estimación** del maestro de la distancia de asignación del cliente $i$ (su
distancia al sitio abierto más cercano). Cumple el rol del recurso $\theta(x)$ del Benders
clásico, pero desagregado por cliente: el costo total del maestro es $\sum_i\theta_i$. Cada
corte es una cota inferior lineal que impide que $\theta_i$ **subestime** la distancia real;
al acumular cortes, $\theta_i$ converge a la distancia verdadera.

### 6. ¿Qué queda en el maestro y qué en el subproblema?
En el **maestro** quedan las decisiones complicantes: las binarias $y_j$ (qué sitios abrir),
la restricción $\sum_j y_j=p$ y las variables $\theta_i$. En el **subproblema** queda lo fácil:
fijado $\bar y$, calcular la distancia de cada cliente —que se separa en $N$ problemas
independientes—. Las variables que **conectan** ambos niveles son las $y$: bajan del maestro
al subproblema, y los cortes (cotas de $\theta_i$ en función de $y$) suben de vuelta.

### 7. ¿Por qué la separación es $O(NM)$ y no requiere resolver un LP?
Porque el dual del subproblema tiene **solución cerrada**. Basta calcular un índice $\tilde k_i$
—el último radio donde el cliente no está cubierto— recorriendo sus sitios del más cercano al
más lejano con la matriz $S$, lo que cuesta $O(M)$ por cliente. Con $\tilde k_i$ se obtienen de
inmediato el valor óptimo y los coeficientes del corte. Sobre $N$ clientes da $O(NM)$ por
separación, **sin** llamar al solver para resolver ningún LP.

### 8. ¿Por qué F3 es mejor que F2 si tienen el mismo óptimo y la misma relajación LP?
Porque F3 reescribe la cobertura usando los sitios a distancia **exactamente** $D^k_i$ en lugar
de "$\le D^k_i$", aprovechando que las $z^k_i$ son monótonas. Eso hace que cada $y_j$ aparezca
en muchas menos restricciones: la matriz queda **mucho más rala**. Misma cota LP, misma brecha
de integridad, pero el solver explota la esparsidad y resuelve más rápido. Es un caso claro del
principio del curso: dos formulaciones del mismo conjunto pueden rendir muy distinto.

---

## Recordatorio de notación (por si preguntan en la pizarra)
- Maestro genérico del curso: $\min c^\top x+\eta$, con $\eta\ge\theta(x)$ (recurso).
- En el pMP: $x\to y$ (binarias de apertura), $\eta\to\sum_i\theta_i$.
- Corte de optimalidad genérico: $\eta\ge\pi^{\star\top}(b-Ax)$ (de un punto extremo $\pi^\star$).
- Corte de optimalidad del pMP: $\theta_i\ge D^{\tilde k_i+1}_i-\sum_{j:d_{ij}\le D^{\tilde k_i}_i}(D^{\tilde k_i+1}_i-d_{ij})\,y_j$.
- Cotas: $LB\le z^\star\le UB$; gap $=\frac{UB-LB}{|UB|}$; brecha de integridad $=v(\text{MILP})-v(\text{LP})$.
