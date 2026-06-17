# Informe teórico — Descomposición de Benders eficiente para el problema de las *p*-medianas

**Curso:** Optimización Computacional (PUCV).
**Paper replicado:** Duran-Mateluna, C., Ales, Z. & Elloumi, S. (2023). *An efficient Benders decomposition for the p-median problem*. European Journal of Operational Research, 308, 84–96.
**Autor:** Alonso Peña Domarchi.

> Este documento es a la vez (a) la base teórica del proyecto de implementación y (b) el material de estudio que integra las tres entregas teóricas del curso. Todas las explicaciones son propias; las ecuaciones reproducen las formulaciones matemáticas del problema (objetos matemáticos, no texto del paper).

---

## 0. Cómo leer este informe

| Sección | Contenido | Entrega del curso |
|---------|-----------|-------------------|
| 1 | Resumen ejecutivo | — |
| 2 | Conceptos previos (todo lo que hay que saber antes) | — |
| 3 | Formulación base F1 | **Entrega 1** |
| 4 | Formulaciones ordenadas F2 y F3 | (apoyo Entrega 1/3) |
| 5 | Relajación lagrangiana del pMP | **Entrega 2** |
| 6 | Descomposición de Benders del pMP | **Entrega 3** |
| 7 | Algoritmo de separación O(NM) | (núcleo del paper) |
| 8 | Reformulación compacta F4 | — |
| 9 | Algoritmo de dos fases | — |
| 10 | Estudio computacional | — |
| 11 | Plan de implementación | ver `PLAN.md` |
| 12 | Checklist de conceptos | — |
| 13 | Preguntas para el profesor | — |

Convención de lectura: cada bloque marcado **Intuición** explica la idea en palabras; cada bloque **Rigor** da la formulación matemática. Si una ecuación aparece, justo después se explica en palabras.

---

## 1. Resumen ejecutivo

**Qué problema resuelve el paper.** El problema de las *p*-medianas (pMP): dado un conjunto de $N$ clientes y $M$ sitios candidatos, con distancias $d_{ij}$ entre cada cliente $i$ y sitio $j$, se deben **abrir exactamente $p$ sitios** de modo que la **suma de las distancias de cada cliente a su sitio abierto más cercano** sea mínima. No hay costos fijos de apertura (eso lo diferencia del problema de localización de instalaciones no capacitado, UFL).

**Por qué importa.** Es un problema fundamental de localización discreta. Aparece en logística (bodegas, plantas), respuesta a emergencias y ayuda humanitaria (ubicación de refugios), y como problema de *clustering* (el *k-medoids*, donde clientes y sitios son el mismo conjunto y se buscan $p$ "centros" representativos).

**Por qué la solución exacta es difícil.** El pMP es **NP-duro** (Kariv & Hakimi, 1979). El número de formas de elegir $p$ sitios entre $M$ es $\binom{M}{p}$, que crece de forma combinatoria. Las formulaciones MILP exactas crecen rápido en variables y restricciones, y para instancias grandes (decenas o cientos de miles de puntos) los solvers genéricos colapsan en memoria o tiempo.

**Qué aportan los autores.** Aplican **descomposición de Benders** a la mejor formulación conocida (F3). El hallazgo clave: el subproblema de Benders del pMP es tan simple que su **dual tiene solución cerrada**, por lo que los **cortes de Benders se separan en tiempo lineal $O(NM)$** sin resolver ningún programa lineal (LP). Envuelven esto en un **algoritmo de dos fases** (relajación + branch-and-cut con cortes perezosos).

**Por qué es eficiente y por qué mejora a Zebra.** El método anterior estado-del-arte, **Zebra** (García, Labbé & Marín, 2011), es un *branch-cut-and-price* sobre F2 que va agregando variables $z$ poco a poco. Sufre problemas de memoria en instancias grandes. La descomposición de Benders aquí propuesta **nunca materializa las variables $z$**: las reemplaza por una variable continua $\theta_i$ por cliente y genera cortes solo cuando se violan. Resultado: **supera a Zebra por un orden de magnitud** en tiempo, no tiene los problemas de memoria, y resuelve **por primera vez a optimalidad** varias instancias enormes (TSP hasta 238.025 puntos, BIRCH hasta 89.600).

---

## 2. Conceptos previos

### 2.1 Problemas de localización discreta
Se elige un subconjunto de ubicaciones (de un conjunto finito de candidatos) donde instalar instalaciones, para atender a un conjunto de clientes. El objetivo típico minimiza costos fijos de apertura + costos de asignación. El pMP es el caso **sin costos fijos**, con número de aperturas **fijado en $p$**, y costos de asignación = distancias.

### 2.2 El pMP, definición formal
**Datos:** clientes $\{C_1,\dots,C_N\}$, sitios $\{F_1,\dots,F_M\}$, distancias $d_{ij}\ge 0$, entero $p$.
**Decisión:** elegir $S\subseteq\{F_1,\dots,F_M\}$ con $|S|=p$.
**Objetivo:** $\min_{|S|=p}\ \sum_{i=1}^N \min_{j\in S} d_{ij}$.

> **Intuición.** "Pongo $p$ antenas; cada casa se conecta a la antena más cercana; quiero minimizar la suma de cables." El truco de todo el problema es que **una vez decididas las antenas, cada cliente elige solo: la más cercana.** Lo difícil es decidir *qué* $p$ antenas.

### 2.3 Clientes vs. sitios; distancia de asignación
- **Cliente:** punto de demanda que debe ser atendido (cada cliente se asigna a exactamente un sitio abierto).
- **Sitio:** ubicación candidata donde se puede abrir una instalación.
- **Distancia de asignación** del cliente $i$ = distancia a su **sitio abierto más cercano**. La función objetivo es la suma de estas distancias.
- En muchas instancias (k-medoids, TSP, BIRCH) clientes y sitios son el **mismo** conjunto de puntos, así $N=M$.

### 2.4 NP-dureza
El pMP es NP-duro: no se conoce algoritmo de tiempo polinomial que lo resuelva a optimalidad en el peor caso. Por eso para instancias grandes históricamente se usaban heurísticas; resolver **exactamente** a gran escala era el desafío abierto que ataca el paper.

### 2.5 MILP, relajación lineal, brecha de integridad
- **MILP** (Mixed-Integer Linear Program): modelo lineal con algunas variables enteras/binarias.
- **Relajación lineal (LP):** se reemplazan las restricciones de integralidad (p. ej. $y_j\in\{0,1\}$) por $0\le y_j\le 1$. El LP resultante se resuelve rápido y da una **cota inferior** del óptimo (en un problema de minimización).
- **Brecha de integridad:** diferencia entre el óptimo entero y el óptimo de la relajación LP. Formulaciones distintas del mismo problema pueden tener **distinta** relajación (más ajustada = mejor cota). F1, F2 y F3 comparten la misma relajación LP, pero rinden muy distinto en la práctica por la **densidad** de su matriz de restricciones.

### 2.6 Branch-and-bound y branch-and-cut
- **Branch-and-bound (B&B):** explora un árbol de subproblemas; en cada nodo resuelve la relajación LP (cota inferior) y ramifica fijando variables; poda ramas cuya cota inferior supera la mejor solución conocida (cota superior).
- **Branch-and-cut:** B&B + agregar **planos cortantes** (desigualdades válidas) que recortan soluciones fraccionarias sin eliminar enteras factibles, ajustando la relajación dentro del árbol.

### 2.7 Descomposición de Benders (idea general)
Introducida por Benders (1962). Parte el problema en:
- **Problema maestro (MP):** decide las variables "difíciles" (aquí: qué sitios abrir, $y$).
- **Subproblema(s) (SP):** con $y$ fijo, resuelve lo "fácil" (aquí: la distancia de cada cliente).

Se itera: el maestro propone $\bar y$; los subproblemas evalúan esa propuesta y devuelven **cortes de Benders** (desigualdades) que el maestro incorpora. Hay dos tipos de cortes:
- **Cortes de optimalidad:** corrigen una **subestimación** del costo (el maestro creía que $\theta_i$ podía ser menor de lo real).
- **Cortes de factibilidad:** eliminan un $\bar y$ que hace **infactible** el subproblema.

> **Clave para este paper:** el subproblema del pMP **siempre es factible y acotado**, por lo que **solo hay cortes de optimalidad, nunca de factibilidad.** Esto simplifica mucho la implementación.

- **Problema de separación:** dado $\bar y$ (y los $\bar\theta_i$ del maestro), decidir si existe un corte **violado** y construirlo. Que esto sea barato es lo que hace o rompe el método.
- **Callbacks:** función propia que el solver (Gurobi/CPLEX) llama durante su branch-and-cut. Para Benders se usa el callback de *lazy constraints* (restricciones perezosas): cada vez que el solver encuentra una solución entera candidata, llama a tu separador; si hay corte violado, lo agregas y el solver continúa. **Eso es "branch-and-Benders-cut".**

### 2.8 Cotas, gap, heurísticas
- **Cota inferior (LB):** valor que el óptimo no puede ser menor (lo da la relajación / el dual).
- **Cota superior (UB):** valor de una solución factible (lo da una heurística o una solución entera).
- **Gap de optimalidad:** $\text{gap}=\frac{UB-LB}{UB}$ (o similar). Gap $0\%$ = óptimo probado.
- **Heurística:** método rápido que da una solución factible (UB) sin garantía de optimalidad. Aquí se usa **PopStar** (Resende & Werneck, 2004), la mejor heurística conocida para pMP, para arrancar con buen UB.

### 2.9 Reduced cost fixing (fijación por costos reducidos)
Tras resolver la relajación LP, cada variable $y_j$ tiene un **costo reducido** $rc_j$ (cuánto empeoraría el objetivo al forzar un cambio unitario). Si, dadas las cotas $LB$ y $UB$, abrir/cerrar un sitio implicaría superar $UB$, esa variable puede **fijarse** (a 0 o a 1) antes de ramificar, reduciendo el árbol. Es efectivo cuando $p$ es pequeño respecto de $M$ (ratio $p/M<20\%$).

---

## 3. Entrega 1 — Formulación base F1

Formulación clásica de ReVelle & Swain (1970). Notación: $[n]=\{1,\dots,n\}$.

**Variables de decisión:**
- $y_j\in\{0,1\}$: vale 1 si el sitio $F_j$ se abre.
- $x_{ij}\in[0,1]$: vale 1 si el cliente $C_i$ se asigna al sitio $F_j$.

**Rigor (F1):**

$$\min \sum_{i=1}^{N}\sum_{j=1}^{M} d_{ij}\,x_{ij}\tag{1}$$

$$\text{s.a.}\quad \sum_{j=1}^{M} y_j = p\tag{2}$$

$$\sum_{j=1}^{M} x_{ij}=1\qquad i\in[N]\tag{3}$$

$$x_{ij}\le y_j\qquad i\in[N],\,j\in[M]\tag{4}$$

$$x_{ij}\ge 0\qquad i\in[N],\,j\in[M]\tag{5}$$

$$y_j\in\{0,1\}\qquad j\in[M]$$

**Explicación en palabras de cada parte:**
- **(1)** Minimiza la suma de distancias cliente–sitio sobre las asignaciones activas.
- **(2)** Abre exactamente $p$ sitios.
- **(3)** Cada cliente se asigna a **exactamente un** sitio.
- **(4)** Un cliente solo puede asignarse a un sitio **abierto** (si $y_j=0$, fuerza $x_{ij}=0$).
- **(5)** No-negatividad de $x$.

**Por qué las variables $x$ pueden relajarse a continuas.**
Con $y$ fijo y minimizando, cada cliente concentra todo su "peso" en el sitio abierto más cercano: la solución óptima de $x$ es automáticamente $0/1$ aunque no lo impongamos. Por eso basta $x_{ij}\ge 0$ (más (3) y (4)); no se necesita $x_{ij}\in\{0,1\}$. Esto reduce mucho el costo de resolver la relajación.

**Análisis estructural y restricciones complicantes (clave para Entregas 2 y 3).**
- La restricción $(2)$ es **global** (acopla todos los $y$).
- Las restricciones $(4)$ **acoplan** $x$ con $y$.
- Si **fijáramos $y$**, el problema se **separa por cliente** y se vuelve trivial (cada cliente elige su sitio abierto más cercano). → Esta observación es la **semilla de Benders** (Sección 6): las $y$ son las variables "complicantes".
- Si en cambio **relajamos $(3)$** (asignación) con multiplicadores, el problema se separa por **sitio**. → Esa es la semilla de la **relajación lagrangiana** (Sección 5).

**Fortalezas y debilidades de F1.**
- *Fortaleza:* intuitiva, directa, relajación LP razonable.
- *Debilidad:* tiene $N\times M$ variables $x$ y $1+N+N\times M$ restricciones. Para $N=M=10^4$ son $\sim 10^8$ variables → **inviable**. Por eso F1 "se vuelve grande" y motiva F2/F3.

---

## 4. Formulaciones ordenadas F2 y F3

### 4.1 Distancias ordenadas y la idea de "radios"
Para cada cliente $i$, en lugar de razonar "¿a qué sitio lo mando?", se razona "¿a qué **radio** alcanza su sitio abierto más cercano?".

**Rigor.** Para cada cliente $i$, sea $K_i\le M$ el número de **distancias distintas** de $i$ a los sitios, y ordénense:
$$D^1_i < D^2_i < \dots < D^{K_i}_i.$$
Variable nueva: $z^k_i$, con $z^k_i = 1$ **si y solo si** no hay sitio abierto a distancia $\le D^k_i$ de $i$ (es decir, el cliente "aún no está cubierto" a ese radio).

### 4.2 El objetivo telescópico (aquí es donde casi todos se bloquean)

**Rigor (F2), Cornuejols, Nemhauser & Wolsey (1980):**

$$\min \sum_{i=1}^{N}\Big[\,D^1_i + \sum_{k=1}^{K_i-1}\big(D^{k+1}_i - D^k_i\big)\,z^k_i\,\Big]\tag{6}$$

$$\text{s.a.}\quad \sum_{j=1}^{M} y_j = p\tag{7}$$

$$z^k_i + \!\!\sum_{j:\,d_{ij}\le D^k_i}\!\! y_j \ge 1\qquad i\in[N],\,k\in[K_i]\tag{8}$$

$$z^k_i\ge 0\qquad i\in[N],\,k\in[K_i]\tag{9}$$

$$y_j\in\{0,1\}$$

**Explicación en palabras del objetivo (6).** La distancia de asignación de un cliente se reconstruye como una **suma telescópica**: se parte asumiendo el radio mínimo $D^1_i$, y por **cada anillo** $k$ en el que el cliente **todavía no fue cubierto** ($z^k_i=1$) se paga el incremento $D^{k+1}_i-D^k_i$ hasta el siguiente anillo.

> **Intuición — peajes crecientes.** Cliente con tres distancias posibles $2,5,9$ → $D^1=2,\ D^2=5,\ D^3=9$. El objetivo de ese cliente es $2 + 3\,z^1 + 4\,z^2$.
> - Sitio más cercano abierto a **5**: ¿hay sitio dentro de radio 2? No → $z^1=1$. ¿Dentro de 5? Sí → $z^2=0$. Costo $=2+3(1)+4(0)=\mathbf{5}$. ✓
> - A **9**: $z^1=1,\ z^2=1$ → $2+3+4=\mathbf{9}$. ✓
> - A **2**: $z^1=0,\ z^2=0$ → $\mathbf{2}$. ✓
> Vas "pagando peajes" mientras no aparezca un sitio abierto; cuando aparece, dejas de pagar.

**Explicación de (8).** Fuerza $z^k_i=1$ cuando **no** hay ningún sitio abierto dentro del radio $D^k_i$ (porque entonces $\sum_{j:d_{ij}\le D^k_i} y_j=0$, y la restricción obliga $z^k_i\ge 1$). Si **sí** hay sitio dentro del radio, la restricción se satisface con $z^k_i=0$, y como el coeficiente de $z^k_i$ en (6) es positivo, el óptimo lo pone en 0.

**Por qué F2 puede ser mucho más chica que F1.** F1 tiene $N\times M$ variables $x$. F2 tiene $K=\sum_i K_i$ variables $z$ y $K+1$ restricciones. Como $K\le N\times M$ (y normalmente $K\ll N\times M$, sobre todo si hay distancias repetidas, p. ej. $N=M$), **F2 nunca es mayor y suele ser mucho menor** que F1. Ambas tienen el **mismo valor de relajación lineal**.

### 4.3 F3: misma formulación, matriz mucho más rala

**Idea (Elloumi, 2010).** Por definición, si el cliente está cubierto a un radio chico, también lo está a radios mayores: $z^{k-1}_i=0 \Rightarrow z^k_i=0$. Es decir, los $z$ son **monótonos decrecientes en $k$**. Esto permite reescribir (8) usando solo los sitios a distancia **exactamente** $D^k_i$ (no "$\le$").

**Rigor (F3):**

$$\min \sum_{i=1}^{N}\Big[\,D^1_i + \sum_{k=1}^{K_i-1}\big(D^{k+1}_i - D^k_i\big)\,z^k_i\,\Big]\tag{10}$$

$$\text{s.a.}\quad \sum_{j=1}^{M} y_j = p\tag{11}$$

$$z^1_i + \!\!\sum_{j:\,d_{ij}=D^1_i}\!\! y_j \ge 1\qquad i\in[N]\tag{12}$$

$$z^k_i + \!\!\sum_{j:\,d_{ij}=D^k_i}\!\! y_j \ge z^{k-1}_i\qquad i\in[N],\,k=2,\dots,K_i\tag{13}$$

$$z^k_i\ge 0\qquad i\in[N],\,k\in[K_i]\tag{14}$$

$$y_j\in\{0,1\}\qquad j\in[M]\tag{15}$$

**Explicación de (12) y (13).**
- **(12)** es exactamente (8) para $k=1$.
- **(13)** dice: $z^k_i$ toma valor 1 si $z^{k-1}_i=1$ (aún no cubierto en el anillo anterior) **y** no hay sitio abierto a distancia **exactamente** $D^k_i$. Al usar "$=$" en vez de "$\le$", **cada $y_j$ aparece en muchas menos restricciones** → la matriz tiene muchísimos más ceros.

**Por qué F3 es más eficiente que F2.** F2 y F3 usan las mismas variables, el mismo objetivo y la **misma relajación lineal**. Pero F3 tiene una matriz de coeficientes **mucho más rala**, lo que el solver explota: rinde **significativamente mejor** en la práctica.

**Por qué se elige F3 como base para Benders.** Es la formulación exacta más eficiente conocida; sobre ella se construye la descomposición.

---

## 5. Entrega 2 — Relajación lagrangiana del pMP (propuesta teórica)

> Esta sección es la **Entrega 2** del curso. La incluyo completa porque el curso la exige y porque es el "hermano dual" de Benders: ambas producen cotas inferiores explotando estructura, pero por caminos distintos.

### 5.1 Identificación de las restricciones complicantes
Partimos de **F1**. Las restricciones de **asignación (3)**, $\sum_j x_{ij}=1$, son las que impiden que el problema se separe limpiamente por sitio. Las **relajamos** (las llevamos al objetivo con multiplicadores), que es la elección lagrangiana clásica para el pMP.

### 5.2 Función lagrangiana
Sea $\lambda_i\in\mathbb{R}$ el multiplicador de la restricción $(3)$ del cliente $i$. La función lagrangiana es:

$$L(\lambda)=\min_{x,y}\ \sum_{i}\sum_{j} d_{ij}x_{ij} + \sum_i \lambda_i\Big(1-\sum_j x_{ij}\Big)$$
$$=\sum_i \lambda_i + \min_{x,y}\ \sum_{j}\sum_{i}\big(d_{ij}-\lambda_i\big)x_{ij}$$

sujeto a $\sum_j y_j=p$, $\ x_{ij}\le y_j$, $\ x_{ij}\ge 0$, $\ y_j\in\{0,1\}$.

### 5.3 El subproblema lagrangiano se separa por sitio
Para $y$ fijo, cada $x_{ij}$ es independiente: conviene poner $x_{ij}=1$ (hasta $y_j$) solo si $(d_{ij}-\lambda_i)<0$. Definamos la **contribución del sitio $j$**:

$$\beta_j(\lambda)=\sum_{i}\min\big(0,\ d_{ij}-\lambda_i\big).$$

Entonces el subproblema se reduce a **elegir los $p$ sitios con $\beta_j(\lambda)$ más negativo**:

$$L(\lambda)=\sum_i \lambda_i + \min_{\substack{y:\ \sum_j y_j=p\\ y_j\in\{0,1\}}}\ \sum_j \beta_j(\lambda)\,y_j .$$

> **Intuición.** Los $\lambda_i$ son "precios" que cada cliente está dispuesto a pagar por ser atendido. Un sitio es atractivo si, a esos precios, "ahorra" dinero a muchos clientes ($\beta_j$ muy negativo). Abrimos los $p$ sitios más atractivos. Esto se resuelve **por inspección** (ordenar y tomar los $p$ mejores), sin solver.

### 5.4 Dual lagrangiano y cota inferior
Para todo $\lambda$, $L(\lambda)\le \text{OPT}(pMP)$ (cota inferior). El **dual lagrangiano** busca la mejor cota:

$$\max_{\lambda}\ L(\lambda).$$

$L(\lambda)$ es cóncava y lineal por tramos → se maximiza con el **método del subgradiente**: en cada iteración, dado $\lambda^t$, se resuelve el subproblema (barato), se obtiene un subgradiente $g^t_i = 1-\sum_j x^t_{ij}$ (violación de la restricción de asignación del cliente $i$), y se actualiza
$$\lambda^{t+1}_i=\lambda^t_i+\alpha_t\,g^t_i,$$
con $\alpha_t$ el **tamaño de paso** (regla típica: $\alpha_t=\mu_t\frac{UB-L(\lambda^t)}{\|g^t\|^2}$, con $\mu_t$ decreciente).

### 5.5 Recuperación primal
La solución $y$ del subproblema puede no ser factible primal (algún cliente sin asignar). Se recupera una solución factible con una **heurística**: dada la $y$ del subproblema, asignar cada cliente a su sitio abierto más cercano → da un **UB**. El par (LB del dual, UB heurístico) acota el óptimo.

### 5.6 Relación con Benders
- **Lagrangiana:** relaja **(3)**, el subproblema se separa **por sitio**, la cota la da $\max_\lambda L(\lambda)$.
- **Benders:** fija **$y$**, el subproblema se separa **por cliente**, la cota la dan los cortes acumulados en el maestro.
Ambas son técnicas duales de cota inferior. En este paper el subproblema de Benders resulta resoluble en forma cerrada, lo que lo hace imbatible aquí; pero conceptualmente la lagrangiana es la alternativa natural que el curso pide analizar primero.

---

## 6. Entrega 3 — Descomposición de Benders del pMP (propuesta teórica)

> Esta sección es la **Entrega 3**: definición del maestro, el subproblema, los tipos de corte y la justificación.

### 6.1 Qué se fija, qué se elimina, qué aparece
Partimos de **F3**. Observación central: **fijado $y=\bar y$, el problema se separa en $N$ subproblemas** (uno por cliente), cada uno calculando la distancia de asignación de ese cliente. Las variables $z$ son la parte "fácil".

Entonces:
- **Se eliminan del maestro todas las variables $z^k_i$.**
- **Se introduce una variable continua $\theta_i$ por cliente**, que representa la distancia de asignación del cliente $i$.

**Maestro (MP):**
$$\min \sum_{i=1}^N \theta_i\quad\text{s.a.}\quad \sum_{j=1}^M y_j=p,\quad \theta_i\ \text{satisface } BD_i\ (i\in[N]),\quad y_j\in\{0,1\}.$$
Donde $BD_i$ es el conjunto de cortes de Benders del cliente $i$ (inicialmente vacío, crece con las iteraciones).

> **Intuición.** El maestro es chiquito: solo decide qué sitios abrir y "estima" la distancia de cada cliente con $\theta_i$. Los cortes van obligando a que $\theta_i$ no subestime la distancia real.

### 6.2 Subproblema primal $SP_i(\bar y)$
Para $\bar y$ fijo, el subproblema del cliente $i$ (derivado de F3) es:

$$\min\ D^1_i + \sum_{k=1}^{K_i-1}\big(D^{k+1}_i-D^k_i\big)z^k_i$$
$$\text{s.a.}\quad z^1_i \ge 1-\!\!\sum_{j:\,d_{ij}=D^1_i}\!\!\bar y_j$$
$$z^k_i - z^{k-1}_i \ge -\!\!\sum_{j:\,d_{ij}=D^k_i}\!\!\bar y_j\qquad k\in\{2,\dots,K_i\}$$
$$z^k_i\ge 0\qquad k\in[K_i]$$

Es siempre **factible** (se puede poner $z$ suficientemente grande) y **acotado** (objetivo con coeficientes $\ge 0$, minimización).

### 6.3 Subproblema dual $DSP_i(\bar y)$
Variables duales $v^k_i$ (una por restricción):

$$\max\ D^1_i + v^1_i\Big(1-\!\!\sum_{j:\,d_{ij}=D^1_i}\!\!\bar y_j\Big) - \sum_{k=2}^{K_i} v^k_i\!\!\sum_{j:\,d_{ij}=D^k_i}\!\!\bar y_j$$
$$\text{s.a.}\quad v^k_i - v^{k+1}_i \le D^{k+1}_i-D^k_i\qquad k\in[K_i-1]$$
$$v^k_i\ge 0\qquad k\in[K_i]$$

### 6.4 El corte de Benders (ecuación 16)
De un punto extremo $\bar v$ del dual $DSP_i(\bar y)$ se obtiene el **corte de optimalidad**:

$$\theta_i \ge D^1_i + \bar v^1_i\Big(1-\!\!\sum_{j:\,d_{ij}=D^1_i}\!\! y_j\Big) - \sum_{k=2}^{K_i}\bar v^k_i\!\!\sum_{j:\,d_{ij}=D^k_i}\!\! y_j\tag{16}$$

**Qué significa (16) en palabras.** Es una **cota inferior lineal de $\theta_i$ en función de $y$**: dice "tu estimación de la distancia del cliente $i$ no puede ser menor que esta expresión, que depende de qué sitios abras". A medida que se agregan cortes para distintos $\bar y$, el maestro va obligando a $\theta_i$ a igualar la distancia real.

**Por qué son cortes de optimalidad y no de factibilidad.** Porque $SP_i(\bar y)$ es **siempre factible y acotado** (Sección 6.2). No hay $\bar y$ que vuelva infactible el subproblema, así que **nunca se necesitan cortes de factibilidad**; todos los cortes corrigen subestimaciones del costo (optimalidad).

---

## 7. Algoritmo de separación O(NM) — el corazón del paper

### 7.1 El problema de separación
Dado $(\bar y,\bar\theta)$ del maestro, decidir para cada cliente $i$ si su corte está **violado** ($\bar\theta_i$ subestima la distancia real) y, de serlo, construir el corte (16).

**Por qué resolver todos los subproblemas "a lo bruto" sería caro.** Hay $N$ subproblemas **por iteración**, y hay muchas iteraciones. Resolver cada uno como un LP (vía dual) sería prohibitivo a gran escala. La gracia: **no hace falta** — hay fórmula cerrada.

### 7.2 Solución óptima del subproblema (ecuación 17)
Como $SP_i$ minimiza con coeficientes $\ge 0$, los $z^k_i$ se hacen lo más chicos posible:

$$\bar z^k_i = \max\Big(0,\ 1-\!\!\sum_{j:\,d_{ij}\le D^k_i}\!\!\bar y_j\Big)\tag{17}$$

**En palabras:** $\bar z^k_i$ es 1 (no cubierto) mientras no haya ningún sitio abierto dentro del radio $D^k_i$; pasa a 0 apenas aparece uno. Por tanto la secuencia $\bar z^1_i,\bar z^2_i,\dots$ es **decreciente** en $k$.

### 7.3 El índice $\tilde k_i$ (Definición 1)
Como los $\bar z^k_i$ son decrecientes, basta identificar el **último anillo estrictamente positivo** (último radio donde el cliente aún no está cubierto):

$$\tilde k_i=\begin{cases}0 & \text{si } \sum_{j:\,d_{ij}=D^1_i}\bar y_j \ge 1\\[4pt]\max\{k\in[K_i]:\ \sum_{j:\,d_{ij}\le D^k_i}\bar y_j < 1\} & \text{en otro caso}\end{cases}$$

> Si $\bar y$ es **binaria**, la distancia de asignación real del cliente $i$ es exactamente $D^{\tilde k_i+1}_i$ (el primer radio donde aparece un sitio abierto).

### 7.4 Valor óptimo del subproblema (ecuación 18)

$$\text{OPT}(SP_i(\bar y))=\begin{cases}D^1_i & \text{si } \tilde k_i=0\\[4pt]D^{\tilde k_i+1}_i - \displaystyle\sum_{j:\,d_{ij}\le D^{\tilde k_i}_i}\big(D^{\tilde k_i+1}_i-d_{ij}\big)\bar y_j & \text{en otro caso}\end{cases}\tag{18}$$

**En palabras:** si ya hay un sitio a la distancia mínima ($\tilde k_i=0$), la distancia es $D^1_i$. Si no, es $D^{\tilde k_i+1}_i$ (el primer radio cubierto) menos un ajuste por sitios fraccionarios más cercanos (relevante solo cuando $\bar y$ es fraccionario, en Fase 1).

### 7.5 Solución dual (ecuación 19)
Por complementariedad de holguras:

$$\bar v^k_i=\begin{cases}D^{\tilde k_i+1}_i-D^k_i & \text{si } k\le\tilde k_i\\ 0 & \text{en otro caso}\end{cases}\tag{19}$$

### 7.6 El corte final (ecuación 20)
Sustituyendo (19) en (16):

$$\theta_i\ge D^1_i\quad\text{si } \tilde k_i=0;\qquad \theta_i\ge D^{\tilde k_i+1}_i-\!\!\sum_{j:\,d_{ij}\le D^{\tilde k_i}_i}\!\!\big(D^{\tilde k_i+1}_i-d_{ij}\big)y_j\ \text{en otro caso.}\tag{20}$$

> **Dato notable del paper:** estas desigualdades coinciden con las que se obtienen sobre **F1** (Cornuejols et al., 1980; Magnanti & Wong, 1981), aunque aquí se derivaron desde **F3**. Los maestros son iguales; los subproblemas, distintos.

### 7.7 Algoritmos 1 y 2, y la complejidad $O(NM)$

**Algoritmo 1 (separación).** Para cada cliente $i$: calcular $\tilde k_i$ (Alg. 2), calcular $\text{OPT}(SP_i)$ con (18), acumular en $UB$; si $\bar\theta_i<\text{OPT}(SP_i)$, agregar el corte (20).

**Algoritmo 2 (cálculo de $\tilde k_i$ en $O(M)$).** Recorre los sitios del cliente del más cercano al más lejano usando la **matriz $S$** ($S_{ir}=$ el $r$-ésimo sitio más cercano a $i$), acumulando $\bar y$ hasta cubrir 1; cuenta los **saltos de radio** (cambios de distancia) hasta ahí.

```
k̃_i ← 0 ;  r ← 1 ;  val ← 1 − ȳ[S_i1]
mientras val > 0 y r < M:
    si d(i, S_i(r+1)) > d(i, S_ir):  k̃_i ← k̃_i + 1
    r ← r + 1
    val ← val − ȳ[S_ir]
devolver k̃_i
```

**Por qué $O(NM)$.** $\tilde k_i$ se calcula en $O(M)$; con $\tilde k_i$, los pasos 4–5 del Alg. 1 cuestan $O(M)$ y $O(1)$. Sobre los $N$ clientes: **$O(NM)$ por separación**, sin resolver ningún LP.

### 7.8 El rol de la matriz $S$ y la memoria
- $S$ ($N\times M$) ordena, para cada cliente, sus sitios por cercanía. Se construye **una sola vez** en preprocesamiento en $O(NM\log M)$ (QuickSort).
- En instancias grandes, **construir $S$ puede tardar más que resolver** (p. ej. ~1100 s para 85.000 puntos).
- **Memoria:** un cliente nunca se asigna a uno de sus $p$ sitios más lejanos, así que $S$ se reduce a $N\times(M-p)$. Además, las distancias $\{d_{ij}\}$ se calculan **a demanda** (no se almacena la matriz completa) para instancias grandes.

---

## 8. Reformulación compacta F4

Escribir **todos** los cortes (20) de una vez da una formulación compacta:

$$\min \sum_{i=1}^N \theta_i\quad\text{s.a.}\quad \sum_{j=1}^M y_j=p,$$
$$\theta_i\ge D^1_i\qquad i\in[N]\tag{21}$$
$$\theta_i\ge D^{k+1}_i-\!\!\sum_{j:\,d_{ij}\le D^k_i}\!\!\big(D^{k+1}_i-d_{ij}\big)y_j\qquad i\in[N],\,k\in[K_i-1]\tag{22}$$
$$y_j\in\{0,1\}\qquad j\in[M]$$

**Explicación de (22).** Cada $\theta_i$ es $\ge D^{k+1}_i$ a menos que se abra un sitio a distancia $\le D^k_i$ de $i$ (en cuyo caso el término sustraído baja la cota).

**Por qué F4 tiene menos variables.** Solo $N+M$ variables ($\theta$ e $y$), menos que F2/F3. **Pero** tiene la misma cantidad de restricciones, la matriz es **tan densa como F2**, y la misma relajación continua.

**Por qué la formulación compacta sola no es necesariamente más rápida.** Empíricamente (Tabla 1 del paper), pasarle F4 **entera** al solver es **más lento** que F2/F3: la densidad mata el rendimiento. La gracia **no** está en la formulación compacta, sino en **generar los cortes (22) sobre la marcha** (perezosamente) dentro del branch-and-cut — que es justo el algoritmo de dos fases.

---

## 9. Algoritmo de dos fases

### 9.1 Fase 1 — relajación lineal del maestro (Algoritmo 3)
Se resuelve el maestro **sin integralidad** (con $y\in[0,1]$), iterando:

1. Arrancar con una solución heurística $y^h$ (PopStar) y su valor $UB^h$.
2. Generar cortes violados desde $y^h$ (Alg. 1).
3. **Mientras** haya cortes violados:
   - Resolver el maestro LP → $(\bar y,\theta)$.
   - $LB_1 \leftarrow \sum_i \theta_i$.
   - Generar cortes violados desde $\bar y$ (Alg. 1).
   - Si $\bar y$ es fraccionaria: **heurística de redondeo** = abrir los $p$ sitios con mayor $\bar y_j$ → solución entera $y^r$ con valor $UB^r$; si mejora, actualizar $UB_1,y_1$.
4. Devolver $LB_1, y_1, UB_1$.

- **Solución inicial (PopStar):** un buen $UB$ inicial reduce mucho las iteraciones. (En nuestra implementación lo reemplazaremos por *greedy*/aleatorio + redondeo.)
- **Heurística de redondeo:** como en Fase 1 casi todas las soluciones del LP son fraccionarias, abrir los $p$ sitios de mayor $y$ produce soluciones factibles que mejoran $UB$.
- **Condición de término:** no se hallan más cortes violados → se obtuvo el valor de la **relajación lineal**.

### 9.2 Fase 2 — branch-and-Benders-cut
Se agregan las restricciones de integralidad sobre $y$ y se resuelve con **branch-and-cut**. En cada **solución entera** que el solver encuentra, un **callback de lazy constraints** ejecuta el separador (Alg. 1) y agrega cortes (20) violados. Mejoras:

- **Reducción de restricciones (constraint reduction):** al final de Fase 1, la mayoría de los cortes no están activos. Para cada cliente $i$ se conserva hasta el mayor índice $\hat k$ asociado a una restricción **saturada** y se eliminan los de índice mayor. (Mejor que eliminar todas las no saturadas.)
- **Reduced cost fixing:** con $LB_1,UB_1$ y los costos reducidos $rc_j$ de la última $y$ fraccionaria: si $LB_1+rc_j>UB_1$ → fijar $y_j=0$; si $LB_1-rc_j>UB_1$ → fijar $y_j=1$. Efectivo cuando $p/M<20\%$.

**Por qué importan estas mejoras.** Reducen el tamaño del maestro y el árbol de B&B, acelerando la prueba de optimalidad. En instancias enormes algunas se desactivan porque su propio costo (tiempo/memoria) supera el beneficio.

---

## 10. Estudio computacional

### 10.1 Familias de instancias
- **OR-Library** (Beasley, 1990): $N=M$ de 100 a 900, $p$ de 5 a 500. Se resuelven en segundos.
- **TSP-Library** (Reinelt, 1991): de 1.304 a 238.025 puntos; coordenadas 2D, distancia euclidiana truncada. Es el banco de prueba principal.
- **BIRCH:** puntos 2D en clusters; 10.000 a 89.600 puntos. Satisfacen desigualdad triangular.
- **RW** (Resende & Werneck, 2004): matrices de distancia **aleatorias**, enteras uniformes en $[1,n]$, posiblemente **asimétricas** (no euclidianas). $N=M\in\{100,250,500,1000\}$. **Difíciles** porque $K$ se acerca a $N\times M$.
- **ODM** (Briant & Naddef, 2004): "optimal diversity management" como pMP con **asignaciones prohibidas** entre ciertos clientes y sitios; $N=3773$.
- **UFL/KG:** instancias del problema de localización **con costos de apertura** (extensión del método).

### 10.2 Qué es Zebra
**Zebra** (García, Labbé & Marín, 2011) es el método exacto estado-del-arte previo: *branch-cut-and-price* sobre F2 que agrega variables $z$ de forma incremental. Resolvía hasta $N=85.900$, pero sufre **falta de memoria** en instancias grandes y **no maneja instancias asimétricas** (RW).

### 10.3 Métricas reportadas
$LB_1, UB_1$ (cotas al final de Fase 1), $T_1$ (tiempo Fase 1), **gap** final, **iter** (separaciones), **nodes** (nodos del B&B), **Ttot** (tiempo total), y la comparación de tiempos con Zebra y heurísticas (normalizando por *benchmark score* de las máquinas).

### 10.4 Qué muestran los resultados
- Supera a Zebra **por un orden de magnitud** en tiempo promedio (p. ej. medianas TSP: 467 s vs 2022 s).
- **No** tiene problemas de memoria donde Zebra sí los tiene.
- Resuelve **por primera vez a optimalidad** instancias enormes (TSP 115.455 y 238.025; BIRCH hasta 89.600).
- $LB_1$ y $UB_1$ de Fase 1 ya son muy buenos: muchas instancias quedan resueltas (o casi) sin entrar a Fase 2.

### 10.5 Dónde brilla y dónde sufre
- **Brilla:** instancias euclidianas/geométricas grandes (TSP, BIRCH); valores de $p$ grandes.
- **Sufre:** instancias **RW** (no euclidianas, $K\approx N\times M$, muchas variables/restricciones) con $p$ chico → gaps grandes y límite de tiempo; algunas instancias con $p$ intermedio donde el árbol de B&B explota.

---

## 11. Plan de implementación (resumen)

El plan completo, la estructura del repositorio y las etapas (0 a 8) están en **`PLAN.md`**. Resumen de la arquitectura:
- **Núcleo en C:** parsing, distancias, matriz $S$, separación (Alg. 1 y 2), loop de Fase 1, redondeo, cotas, logging.
- **Capa de solver (interfaz delgada):** backends **Gurobi** (principal), **CPLEX** (el del paper), y una opción **abierta** (SCIP/HiGHS) para reproducibilidad sin licencia. Resuelve el maestro (LP en Fase 1; MIP + callback de *lazy constraints* en Fase 2).
- **Prototipo Python+Gurobi:** referencia legible de callbacks + oráculo de correctitud + resultados tempranos.
- **Benchmark vs. paper:** comparar nuestros $LB_1/UB_1/$gap$/T_{tot}$ contra las Tablas 2–9 del paper para el subconjunto elegido.

---

## 12. Checklist de conceptos clave (dominar antes/durante la implementación)

- [ ] **F1, F2, F3, F4** y por qué comparten relajación pero rinden distinto (densidad).
- [ ] **Distancias ordenadas** $D^k_i$, $K_i$, y el **objetivo telescópico**.
- [ ] Variables **$\theta_i$** del maestro y qué representan.
- [ ] **Subproblema** $SP_i$ y **dual** $DSP_i$.
- [ ] **Corte de Benders** (16) y por qué es de **optimalidad** (no factibilidad).
- [ ] **Índice $\tilde k_i$** y las ecuaciones **(17)–(20)**.
- [ ] **Algoritmo de separación** $O(NM)$ y la **matriz $S$**.
- [ ] **Fase 1 vs Fase 2**; rol de la **heurística de redondeo**.
- [ ] **Callbacks** de *lazy constraints* = branch-and-Benders-cut.
- [ ] **Reduced cost fixing** y **constraint reduction**.
- [ ] **Cotas (LB/UB)**, **gap**, y comparación con **Zebra**.
- [ ] **Relajación lagrangiana** (Entrega 2) y su relación con Benders.

---

## 13. Preguntas para el profesor

1. ¿Profundidad esperada de la implementación: núcleo (separación + Fase 1 + Fase 2) basta, o se exigen también PopStar, reduced cost fixing y constraint reduction?
2. ¿La capa de solver con CPLEX/Gurobi/abierto es aceptable, o prefiere un solver específico?
3. ¿Qué subconjunto de instancias se exige reproducir (OR-Library y TSP chicas, o más)?
4. ¿Se requiere replicación numérica exacta de las tablas, o "mismo método + análisis sólido"?
5. ¿Fase 2 con callbacks es obligatoria o un Fase-1-only con buenas cotas ya califica?
6. ¿Entregas 1, 2 y 3 se incorporan en este informe o se evalúan por separado?
7. ¿Las "ideas de optimización de modelamiento/solver" que usted tiene en mente apuntan a alguna familia de instancias o variante en particular (para orientar el diseño desde ya)?
