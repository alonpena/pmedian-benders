| Aplicaciones | de métodos | de optimización |
| ------------ | ---------- | --------------- |
Optimización computacional
|     | Apunte del | curso |
| --- | ---------- | ----- |
Pablo Torrealba
6/03/2026

ii

Índice general
1. Fundamentos de programación lineal y entera 1
1. Introducción. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
2. Programación lineal: forma estándar, geometría y óptimos . . . . . . . . . . . . . . 3
2.1. Formas estándar . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
2.2. Poliedros y puntos extremos . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
3. Dualidad en programación lineal . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
3.1. Forma primal y dual . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
3.2. Dualidad débil: el principio de cota . . . . . . . . . . . . . . . . . . . . . . . 4
3.3. Dualidad fuerte . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
3.4. Complementariedad . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
3.5. Teorema de Farkas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
3.6. Comportamiento extremo . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
4. Resolución de problemas lineales: Simplex e Interior-Point . . . . . . . . . . . . . . 7
4.1. El método Simplex . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
4.2. Métodos de puntos interiores . . . . . . . . . . . . . . . . . . . . . . . . . . 8
4.3. Comparación conceptual . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
5. Programación entera y mixta: modelos y relajación lineal . . . . . . . . . . . . . . 10
5.1. MILP: definición . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
5.2. Relajación lineal . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
6. Modelamiento con variables binarias: patrones canónicos . . . . . . . . . . . . . . . 11
6.1. Activación condicional y formulaciones Big-M . . . . . . . . . . . . . . . . . 11
6.2. Selección, cobertura y empaquetamiento . . . . . . . . . . . . . . . . . . . . 11
6.3. Linealización de productos binarios . . . . . . . . . . . . . . . . . . . . . . . 12
6.4. Fortalecimiento de formulaciones . . . . . . . . . . . . . . . . . . . . . . . . 12
7. Cotas, certificados y arquitectura de resolución . . . . . . . . . . . . . . . . . . . . 13
7.1. Cotas inferiores y superiores . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
7.2. Certificados de optimalidad . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
7.3. Arquitectura Branch-and-Bound . . . . . . . . . . . . . . . . . . . . . . . . 13
8. Heurísticas básicas: construcción de soluciones factibles . . . . . . . . . . . . . . . 14
8.1. Esquema heurístico general . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
8.2. Búsqueda local y vecindarios . . . . . . . . . . . . . . . . . . . . . . . . . . 14
8.3. Estancamiento y diversificación . . . . . . . . . . . . . . . . . . . . . . . . . 14
8.4. Integración con algoritmos exactos . . . . . . . . . . . . . . . . . . . . . . . 14
iii

iv ÍNDICE GENERAL
2. Relajación Lagrangiana 15
1. Relajaciones: definición formal y consecuencias . . . . . . . . . . . . . . . . . . . . 15
1.1. Problema original (minimización) . . . . . . . . . . . . . . . . . . . . . . . . 15
1.2. Definición de relajación . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
1.3. Relajación por eliminación de restricciones . . . . . . . . . . . . . . . . . . 15
2. Relajación lagrangiana . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
2.1. Motivación . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
2.2. Planteamiento . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
2.3. Función lagrangiana . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
2.4. Problema lagrangiano . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
2.5. Función dual lagrangiana . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
2.6. Dual lagrangiano . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
2.7. Propiedad fundamental: cota inferior . . . . . . . . . . . . . . . . . . . . . . 18
3. Propiedades del dual lagrangiano . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
3.1. Concavidad de la función dual . . . . . . . . . . . . . . . . . . . . . . . . . 19
3.2. No diferenciabilidad y estructura por tramos . . . . . . . . . . . . . . . . . 19
3.3. Subgradientes del dual lagrangiano . . . . . . . . . . . . . . . . . . . . . . . 19
3.4. Interpretación geométrica . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
4. Optimización del dual: método del subgradiente . . . . . . . . . . . . . . . . . . . . 21
4.1. Subgradiente . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
4.2. Idea del método . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
4.3. Esquema algorítmico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
4.4. Elección del tamaño de paso . . . . . . . . . . . . . . . . . . . . . . . . . . 22
4.5. Qué se garantiza (y qué no) con subgradientes . . . . . . . . . . . . . . . . 22
4.6. Criterios de parada prácticos . . . . . . . . . . . . . . . . . . . . . . . . . . 23
4.7. Dibujo: update y proyección . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
5. Heurísticas lagrangianas y recuperación primal . . . . . . . . . . . . . . . . . . . . 24
5.1. Principio general . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
5.2. Clases de heurísticas lagrangianas . . . . . . . . . . . . . . . . . . . . . . . 24
5.3. Relación con el dual . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24

| Capítulo    |     |     | 1   |     |     |     |              |     |        |     |
| ----------- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------ | --- |
| Fundamentos |     |     |     |     |     | de  | programación |     | lineal |     |
y entera
1. Introducción
La programación matemática es una rama de la optimización que estudia como modelar y
resolver problemas de decisión mediante modelos matemáticos. Dichos modelos buscan optimi-
zar (minimizar o maximizar) una medida de desempeño sujeta a un conjunto de restricciones
restricciones. Formalmente, un modelo de programación matemática se compone de:
|     | variables     |          | de decisión  |           | x (lo      | que puede | elegirse),        |           |     |     |
| --- | ------------- | -------- | ------------ | --------- | ---------- | --------- | ----------------- | --------- | --- | --- |
|     | función       | objetivo |              | f(x)      | (lo que    | se        | desea optimizar), |           |     |     |
|     | restricciones |          | (condiciones |           | que        | deben     | satisfacerse),    |           |     |     |
|     | dominio       |          | de las       | variables | (continuo, |           | entero, binario   | o mixto). |     |     |
Enformaabstracta,unproblemadeoptimización,enestecasominimización,puedeescribirse
como:
|     |     |     |     |     |     | m´ın{f(x) | : x ∈ | X }, |     | (1.1) |
| --- | --- | --- | --- | --- | --- | --------- | ----- | ---- | --- | ----- |
donde X representa el conjunto factible determinado por las restricciones y por el dominio de las
variables.
Un buen modelo no sólo debe ser conceptualmente correcto y representar adecuadamente
el fenómeno estudiado; también debe ser resoluble. La utilidad práctica de un modelo depende
de que pueda gestionarse y resolverse en tiempos razonables con los recursos computacionales
disponibles. Un modelo intratable, aunque formalmente correcto, pierde gran parte de su valor
aplicado. Históricamente, muchos problemas de optimización fueron abordados mediante razo-
namiento manual y análisis estructural. Hoy, sin embargo, la optimización moderna descansa
principalmente en la delegación computacional de estas tareas: algoritmos implementados en sol-
vers especializados realizan la exploración sistemática del espacio de soluciones, la construcción
| de  | cotas y | la verificación |     | de  | optimalidad. |     |     |     |     |     |
| --- | ------- | --------------- | --- | --- | ------------ | --- | --- | --- | --- | --- |
La optimización computacional estudia precisamente cómo resolver modelos de tamaño rea-
lista, explotando su estructura, construyendo cotas de calidad y diseñando algoritmos exactos y
| aproximados. |     | Un  | mismo | modelo | puede | ser: |     |     |     |     |
| ------------ | --- | --- | ----- | ------ | ----- | ---- | --- | --- | --- | --- |
computacionalmente sencillo o extremadamente difícil dependiendo de su formulación,
separable o fuertemente acoplado según la naturaleza de sus restricciones,
|     | fuerte | o débil | según | la  | calidad | de sus | relajaciones. |     |     |     |
| --- | ------ | ------- | ----- | --- | ------- | ------ | ------------- | --- | --- | --- |
1

| 2   | CAPÍTULO |     | 1. FUNDAMENTOS |     | DE PROGRAMACIÓN |     | LINEAL | Y ENTERA |
| --- | -------- | --- | -------------- | --- | --------------- | --- | ------ | -------- |
El foco del curso será comprender estas diferencias estructurales y utilizarlas para diseñar
| métodos | de resolución | eficientes. |     |     |     |     |     |     |
| ------- | ------------- | ----------- | --- | --- | --- | --- | --- | --- |
Un ejemplo mínimo (para fijar lenguaje) Supongamos que debemos seleccionar proyectos
i = 1,...,n con costo a y beneficio p , bajo un presupuesto total B. El modelo binario canónico
|     |     |     | i   | i   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
es:
n
X
|     |     |     |     | ma´x p z |     |     |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- | --- |
|     |     |     |     | i i      |     |     |     |     |
i=1
|     |     |     |     | n   |     |     |     | (1.2) |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- |
X
|     |     |     |     | s.a. a z | ≤ B, |     |     |     |
| --- | --- | --- | --- | -------- | ---- | --- | --- | --- |
|     |     |     |     | i i      |      |     |     |     |
i=1
|     |     |     |     | z ∈ {0,1}, | i = 1,...,n. |     |     |     |
| --- | --- | --- | --- | ---------- | ------------ | --- | --- | --- |
i
Elmodelo(1.2)correspondealproblemaclásicodelamochilabinaria(knapsack).Sudificultad
computacional proviene exclusivamente de la restricción de integridad. Si se reemplaza z ∈ {0,1}
i
por z i ∈ [0,1], se obtiene su relajación lineal, que puede resolverse eficientemente y proporciona
| una cota   | superior | para    | el problema | de maximización. |                 |           |     |     |
| ---------- | -------- | ------- | ----------- | ---------------- | --------------- | --------- | --- | --- |
| Este       | ejemplo  | permite | introducir  | inmediatamente:  |                 |           |     |     |
| Relajación |          | LP (z   | ∈ [0,1])    | como mecanismo   | de construcción | de cotas. |     |     |
i
| Estructura:  |     | una única   | restricción | acoplante.        |             |     |     |     |
| ------------ | --- | ----------- | ----------- | ----------------- | ----------- | --- | --- | --- |
| Complejidad: |     | el problema |             | entero es NP-hard | en general. |     |     |     |
En este curso se trabajará con tres ideas que atraviesan transversalmente todo el contenido:
Modelamiento y estructura: identificar qué restricciones generan dificultad y cuáles inducen
| propiedades |     | explotables. |     |     |     |     |     |     |
| ----------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
Cotas y dualidad: construir relajaciones que permitan evaluar la calidad de soluciones y
| guiar | algoritmos. |     |     |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Descomposición: separar problemas grandes en subproblemas manejables explotando su
estructura.
La Parte II profundiza en relajación lagrangiana (dualidad no diferenciable y métodos de
subgradiente), la Parte III en descomposición de Benders (problema maestro y subproblema
mediante cortes), y la Parte IV aborda algunos modelos extendidos y aproximaciones no lineales
que permiten capturar fenómenos más complejos preservando tractabilidad computacional.

2. PROGRAMACIÓN LINEAL: FORMA ESTÁNDAR, GEOMETRÍA Y ÓPTIMOS 3
| 2. Programación |     |          | lineal: |     | forma | estándar, |     | geometría | y óptimos |     |
| --------------- | --- | -------- | ------- | --- | ----- | --------- | --- | --------- | --------- | --- |
| 2.1. Formas     |     | estándar |         |     |       |           |     |           |           |     |
Un problema de programación lineal (PL) puede escribirse, por ejemplo, como:
c⊤x
|     |     |     |     |     | m´ın |         |      |     |     | (1.3) |
| --- | --- | --- | --- | --- | ---- | ------- | ---- | --- | --- | ----- |
|     |     |     |     |     |      | s.a. Ax | ≤ b  |     |     | (1.4) |
|     |     |     |     |     |      | x       | ≥ 0. |     |     |       |
También son comunes formas con igualdades, cotas, o restricciones ≥. Todas estas formas son
equivalentes bajo transformaciones estándar (variables con signo libre, variables de holgura, etc.).
| 2.2. Poliedros |     | y puntos |       | extremos |             |     |        |              |     |     |
| -------------- | --- | -------- | ----- | -------- | ----------- | --- | ------ | ------------ | --- | --- |
| El conjunto    |     | factible | de un | PL es    | un poliedro |     | (notar | convexidad): |     |     |
Rn
|     |     |     |     | P = | {x ∈ | : Ax | ≤ b, | x ≥ 0}. |     |     |
| --- | --- | --- | --- | --- | ---- | ---- | ---- | ------- | --- | --- |
Un resultado central (teorema fundamental del PL) establece que, si el PL es factible y tiene
óptimo finito, entonces existe una solución óptima en un punto extremo (básico factible) del
poliedro.
Teorema 1.1 (Existencia de óptimo en un punto extremo). Si el PL es factible y la función
objetivo está acotada inferiormente sobre P (es decir, existe un óptimo finito), entonces existe
| una solución | óptima | x⋆  | que es | un punto | extremo |     | de P. |     |     |     |
| ------------ | ------ | --- | ------ | -------- | ------- | --- | ----- | --- | --- | --- |
Lectura computacional Los algoritmos clásicos (simplex) se mueven entre puntos extremos;
los métodos de puntos interiores no necesariamente visitan vértices, pero también se apoyan en
| la estructura | poliédrica. |     |     |     |     |     |     |     |     |     |
| ------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 4   |          |     | CAPÍTULO |              | 1. FUNDAMENTOS |     |     | DE PROGRAMACIÓN |     | LINEAL | Y ENTERA |
| --- | -------- | --- | -------- | ------------ | -------------- | --- | --- | --------------- | --- | ------ | -------- |
| 3.  | Dualidad |     | en       | programación |                |     |     | lineal          |     |        |          |
La dualidad constituye el eje estructural de la programación lineal. Explica por qué las re-
lajaciones entregan cotas, por qué aparecen multiplicadores interpretables como “precios”, y por
qué en descomposición (como en Benders) los problemas duales generan cortes válidos.
| 3.1. |              | Forma | primal      | y        | dual   |          |          |          |                  |     |       |
| ---- | ------------ | ----- | ----------- | -------- | ------ | -------- | -------- | -------- | ---------------- | --- | ----- |
|      | Consideremos |       | el problema |          | primal |          | en forma | canónica | de minimización: |     |       |
|      |              |       |             |          | (P)    |          | m´ın{c⊤x | : Ax ≤   | b, x ≥ 0}.       |     | (1.5) |
|      | donde        | A ∈   | Rm×n,       | b ∈ Rm   | y c    | ∈ Rn.    |          |          |                  |     |       |
|      | Su problema  |       | dual        | asociado | es:    |          |          |          |                  |     |       |
|      |              |       |             |          | (D)    | ma´x{b⊤y |          | : A⊤y    | ≥ c, y ≤ 0}.     |     | (1.6) |
El signo de las restricciones en el primal determina el dominio de las variables duales. Esta
correspondencia será central en relajación lagrangiana y en la interpretación económica de los
multiplicadores.
| 3.2. |     | Dualidad | débil: |     | el principio |     | de  | cota |     |     |     |
| ---- | --- | -------- | ------ | --- | ------------ | --- | --- | ---- | --- | --- | --- |
Teorema 1.2 (Dualidad débil). Para cualquier solución primal factible x y cualquier solución
| dual | factible |     | y, se cumple |     |     |     |     |      |     |     |     |
| ---- | -------- | --- | ------------ | --- | --- | --- | --- | ---- | --- | --- | --- |
|      |          |     |              |     |     |     | b⊤y | c⊤x. |     |     |     |
≤
Demostración. Si x es primal factible, entonces Ax−b ≤ 0. Si y es dual factible, entonces y ≤ 0
| y         | A⊤y−c | ≥    | 0.    |       |       |       |           |      |     |     |     |
| --------- | ----- | ---- | ----- | ----- | ----- | ----- | --------- | ---- | --- | --- | --- |
|           | Como  | Ax−b | ≤ 0   | y y ≤ | 0, se | tiene |           |      |     |     |     |
|           |       |      |       |       |       |       | y⊤(Ax−b)  | ≥ 0. |     |     |     |
| Asimismo, |       | como | A⊤y−c | ≥     | 0 y x | ≥ 0,  | se tiene  |      |     |     |     |
|           |       |      |       |       |       |       | x⊤(A⊤y−c) | ≥    | 0.  |     |     |
Observando que y⊤Ax = x⊤A⊤y, sumando ambas desigualdades se obtiene
|                 |             |          |               |           |          |                  | c⊤x−b⊤y | ≥ 0,               |     |     |     |
| --------------- | ----------- | -------- | ------------- | --------- | -------- | ---------------- | ------- | ------------------ | --- | --- | --- |
| lo              | que implica |          | el resultado. |           |          |                  |         |                    |     |     |     |
| Interpretación. |             |          | En            | problemas |          | de minimización: |         |                    |     |     |     |
|                 | Toda        | solución | dual          | factible  |          | entrega          | una     | cota inferior.     |     |     |     |
|                 | Toda        | solución | primal        |           | factible | entrega          |         | una cota superior. |     |     |     |
En consecuencia,
|     |     |     |     |     |     | b⊤y | ≤   | v(P) ≤ c⊤x. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
Este principio constituye el mecanismo fundamental de construcción de brechas primal–dual.

| 3.   | DUALIDAD | EN  | PROGRAMACIÓN |     |     | LINEAL |     |     | 5   |
| ---- | -------- | --- | ------------ | --- | --- | ------ | --- | --- | --- |
| 3.3. | Dualidad |     | fuerte       |     |     |        |     |     |     |
Teorema 1.3 (Dualidad fuerte). Si uno de los problemas (P) o (D) es factible y tiene óptimo
| finito, | entonces | ambos | lo  | son y | se cumple |        |       |     |     |
| ------- | -------- | ----- | --- | ----- | --------- | ------ | ----- | --- | --- |
|         |          |       |     |       |           | v(P) = | v(D). |     |     |
(x⋆,y⋆)
Consecuencia. Cuando existe óptimo finito, existe un par tal que
|     |     |     |     |     |     | c⊤x⋆ = | b⊤y⋆. |     |     |
| --- | --- | --- | --- | --- | --- | ------ | ----- | --- | --- |
La igualdad primal–dual permite certificar optimalidad computacionalmente mediante la coinci-
| dencia | de  | cotas. |     |     |     |     |     |     |     |
| ------ | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
3.4. Complementariedad
|     | Definimos | las holguras |     | primal | y dual: |     |     |     |     |
| --- | --------- | ------------ | --- | ------ | ------- | --- | --- | --- | --- |
A⊤y−c
|     |     |     |     | u   | = b−Ax | ≥ 0, | v = | ≥ 0. |     |
| --- | --- | --- | --- | --- | ------ | ---- | --- | ---- | --- |
Teorema 1.4 (Condiciones de complementariedad). Si x⋆ y y⋆ son soluciones óptimas, entonces
se cumple
|     |     |     |     |     | y⋆u⋆ | = 0 ∀i, | x⋆v⋆ = 0 | ∀j. |     |
| --- | --- | --- | --- | --- | ---- | ------- | -------- | --- | --- |
|     |     |     |     |     | i i  |         | j j      |     |     |
Obsérvese que, dado que y ≤ 0, estas condiciones son equivalentes a las condiciones estándar
| de   | complementariedad |     | formuladas |     | con | multiplicadores | no negativos. |     |     |
| ---- | ----------------- | --- | ---------- | --- | --- | --------------- | ------------- | --- | --- |
| 3.5. | Teorema           | de  | Farkas     |     |     |                 |               |     |     |
El fundamento geométrico profundo de la dualidad es el siguiente resultado.
Teorema 1.5(Farkas). SeaA ∈ Rm×n yb ∈ Rm.Exactamenteunadelassiguientesafirmaciones
es verdadera:
|     | 1. Existe | x ≥ 0 tal | que | Ax = | b.    |      |     |     |     |
| --- | --------- | --------- | --- | ---- | ----- | ---- | --- | --- | --- |
|     | 2. Existe | y tal que | A⊤y | ≥ 0  | y b⊤y | < 0. |     |     |     |
Interpretación geométrica. Si el sistema Ax = b, x ≥ 0 es infactible, entonces existe un
hiperplano (definido por y) que separa b del cono generado por las columnas de A. El vector y
| constituye |     | un certificado |     | de infactibilidad. |     |     |     |     |     |
| ---------- | --- | -------------- | --- | ------------------ | --- | --- | --- | --- | --- |
Relación con dualidad. El teorema de Farkas es equivalente a dualidad fuerte. Mientras
dualidad débil produce cotas, Farkas expresa la alternativa fundamental: o bien el sistema es
factible, o bien existe un certificado dual que demuestra su imposibilidad.
| 3.6. | Comportamiento |            |             | extremo  |             |                |     |     |     |
| ---- | -------------- | ---------- | ----------- | -------- | ----------- | -------------- | --- | --- | --- |
|      | La dualidad    | también    |             | describe | situaciones | límite:        |     |     |     |
|      | Si el          | primal es  | no acotado, |          | el dual     | es infactible. |     |     |     |
|      | Si el          | dual es no | acotado,    |          | el primal   | es infactible. |     |     |     |
Los solvers modernos utilizan información dual para generar certificados formales de no aco-
| tación | o infactibilidad. |     |     |     |     |     |     |     |     |
| ------ | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |

| 6              | CAPÍTULO   | 1. FUNDAMENTOS | DE PROGRAMACIÓN | LINEAL | Y ENTERA |
| -------------- | ---------- | -------------- | --------------- | ------ | -------- |
| Interpretación | geométrica |                |                 |        |          |
El dual puede interpretarse como la construcción de hiperplanos soporte del poliedro primal.
Cada solución dual factible define una función afín que subestima al valor óptimo primal. El
óptimo dual corresponde al mejor hiperplano soporte posible, es decir, aquel que coincide con el
| valor óptimo | primal. |     |     |     |     |
| ------------ | ------- | --- | --- | --- | --- |
En programación entera, la dualidad lineal deja de ser exacta. Sin embargo, sus principios
sobreviven a través de relajaciones, que darán lugar a funciones duales no diferenciables.

4. RESOLUCIÓN DE PROBLEMAS LINEALES: SIMPLEX E INTERIOR-POINT 7
4. Resolución de problemas lineales: Simplex e Interior-Point
Resolver un problema de programación lineal no es sólo una cuestión teórica: es el núcleo
computacionaldelosmétodosqueveremosmásadelante(relajaciónlagrangiana,Bendersyapro-
| ximaciones |         | no lineales). |     |             |                |      |          |     |
| ---------- | ------- | ------------- | --- | ----------- | -------------- | ---- | -------- | --- |
|            | Existen | dos grandes   |     | familias    | de métodos     | para | resolver | PL: |
|            | Métodos | basados       |     | en vértices | (Simplex).     |      |          |     |
|            | Métodos | de puntos     |     | interiores  | (primal–dual). |      |          |     |
Ambos explotan la estructura convexa del problema, pero desde perspectivas distintas.
| 4.1. | El  | método | Simplex |     |     |     |     |     |
| ---- | --- | ------ | ------- | --- | --- | --- | --- | --- |
En lo que sigue trabajaremos con la forma estándar con igualdades, obtenida introduciendo
| variables | de  | holgura: |     |     |     |     |     |     |
| --------- | --- | -------- | --- | --- | --- | --- | --- | --- |
c⊤x
|     |         |        |       |       | m´ın | s.a. | Ax = | b, x ≥ 0, |
| --- | ------- | ------ | ----- | ----- | ---- | ---- | ---- | --------- |
|     | donde A | ∈ Rm×n | tiene | rango | m.   |      |      |           |
Idea geométrica
Sabemos que, si el problema es factible y tiene óptimo finito, existe una solución óptima en
| un    | punto extremo    |           | del poliedro |           | factible.        |          |          |               |
| ----- | ---------------- | --------- | ------------ | --------- | ---------------- | -------- | -------- | ------------- |
|       | El método        | simplex   | explota      |           | este hecho:      |          |          |               |
|       | Parte            | desde una | solución     |           | básica factible. |          |          |               |
|       | Se mueve         | a una     | base         | adyacente | que              | mejora   | el valor | del objetivo. |
|       | Se detiene       | cuando    |              | no existe | dirección        | de       | mejora.  |               |
|       | Geométricamente, |           | el           | algoritmo | recorre          | vértices | del      | poliedro.     |
| Bases | y soluciones     |           | básicas      |           |                  |          |          |               |
UnabaseesunsubconjuntoB demcolumnaslinealmenteindependientesdeA.Reordenando
| las | variables | como |     |     |     |     |       |     |
| --- | --------- | ---- | --- | --- | --- | --- | ----- | --- |
|     |           |      |     |     |     | x = | (x ,x | ),  |
|     |           |      |     |     |     |     | B N   |     |
la solución básica asociada a la base B se obtiene fijando x = 0 y resolviendo
N
|     |     |     |     |     |     | A   | x = b. |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- |
B B
Es decir,
x = A−1b.
B B
|     | Si x ≥ | 0, la solución |     | es una | solución | básica | factible. |     |
| --- | ------ | -------------- | --- | ------ | -------- | ------ | --------- | --- |
B

| 8      |              |           | CAPÍTULO |             | 1. FUNDAMENTOS |          |            | DE                 | PROGRAMACIÓN |         | LINEAL | Y ENTERA |
| ------ | ------------ | --------- | -------- | ----------- | -------------- | -------- | ---------- | ------------------ | ------------ | ------- | ------ | -------- |
| Costos |              | reducidos | y        | optimalidad |                |          |            |                    |              |         |        |          |
|        | Dada         | una       | base B,  | el valor    | del            | objetivo | puede      | escribirse         |              | como    |        |          |
|        |              |           |          |             |                | c⊤x      | =          | c⊤x +c⊤x           | .            |         |        |          |
|        |              |           |          |             |                |          |            | B B                | N N          |         |        |          |
|        | Sustituyendo |           | x        | = A−1(b−A   |                | x )      | se obtiene |                    |              |         |        |          |
|        |              |           | B        | B           |                | N N      |            |                    |              |         |        |          |
|        |              |           |          |             | c⊤x            | c⊤A−1b+  |            | (cid:0) c⊤ −c⊤A−1A |              | (cid:1) |        |          |
|        |              |           |          |             |                | =        |            |                    |              | N x N . |        |          |
|        |              |           |          |             |                | B        | B          | N                  | B B          |         |        |          |
El vector
|     |     |     |     |     |     | c¯⊤ | c⊤  | −c⊤A−1A |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
=
|     |             |     |        |     |        |            | N   | N B | B N |     |     |     |
| --- | ----------- | --- | ------ | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- |
|     | se denomina |     | vector | de  | costos | reducidos. |     |     |     |     |     |     |
En minimización:
|     | Si  | c¯ ≥ | 0, la solución |     | básica | es óptima. |     |     |     |     |     |     |
| --- | --- | ---- | -------------- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- |
N
Siexistealgúncomponentec¯ < 0,esavariablepuedeentrarenlabaseymejorarelobjetivo.
j
La condición c¯ N ≥ 0 equivale a satisfacer las condiciones duales de optimalidad ¿por que?.
| 4.2. | Métodos |     | de  | puntos | interiores |     |     |     |     |     |     |     |
| ---- | ------- | --- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- |
A diferencia del método simplex, que recorre vértices, los métodos de puntos interiores siguen
| trayectorias |                 | estrictamente |            |             | interiores | del      | conjunto | factible. |           |        |     |       |
| ------------ | --------------- | ------------- | ---------- | ----------- | ---------- | -------- | -------- | --------- | --------- | ------ | --- | ----- |
|              | Consideremos    |               | nuevamente |             | el         | problema | en       | forma     | estándar: |        |     |       |
|              |                 |               |            |             |            | m´ınc⊤x  |          | s.a. Ax   | = b, x    | ≥ 0.   |     |       |
|              | Su dual         | es:           |            |             |            |          |          |           |           |        |     |       |
|              |                 |               |            |             | ma´xb⊤y    |          |          | A⊤y+s     |           |        |     |       |
|              |                 |               |            |             |            |          | s.a.     |           | = c,      | s ≥ 0. |     |       |
|              | Las condiciones |               | de         | optimalidad |            | (KKT)    | son:     |           |           |        |     |       |
|              |                 |               |            |             |            |          |          | Ax =      | b,        |        |     | (1.7) |
A⊤y+s
|     |     |     |     |     |     |     |     | =     | c,    |     |     | (1.8) |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- | --- | ----- |
|     |     |     |     |     |     |     |     | x s = | 0 ∀i, |     |     | (1.9) |
i i
|     |     |     |     |     |     | x   | ≥ 0, | s ≥ 0. |     |     |     | (1.10) |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------ | --- | --- | --- | ------ |
Idea central
|     | La dificultad   |     | principal  |          | radica     | en la     | condición | de        | complementariedad |     |     |     |
| --- | --------------- | --- | ---------- | -------- | ---------- | --------- | --------- | --------- | ----------------- | --- | --- | --- |
|     |                 |     |            |          |            |           |           | x s = 0,  |                   |     |     |     |
|     |                 |     |            |          |            |           |           | i i       |                   |     |     |     |
|     | que caracteriza |     | la         | frontera | del        | poliedro. |           |           |                   |     |     |     |
|     | Los métodos     |     | de barrera |          | reemplazan |           | esta      | condición | por               |     |     |     |
|     |                 |     |            |          |            | x         | s =       | µ,        | µ > 0,            |     |     |     |
i i
|     | lo que | conduce | al  | sistema | primal–dual |     | perturbado |     |     |     |     |     |
| --- | ------ | ------- | --- | ------- | ----------- | --- | ---------- | --- | --- | --- | --- | --- |

4. RESOLUCIÓN DE PROBLEMAS LINEALES: SIMPLEX E INTERIOR-POINT 9
|     |       |             |     |       |          | Ax    | = b,  |     |     |     | (1.11) |
| --- | ----- | ----------- | --- | ----- | -------- | ----- | ----- | --- | --- | --- | ------ |
|     |       |             |     |       |          | A⊤y+s | = c,  |     |     |     | (1.12) |
|     |       |             |     |       |          | XSe   | = µe, |     |     |     | (1.13) |
|     | donde | X = diag(x) |     | y S = | diag(s). |       |       |     |     |     |        |
Para cada µ > 0 existe, bajo condiciones de regularidad, una solución estrictamente factible
(x(µ),y(µ),s(µ)) con x(µ) > 0 y s(µ) > 0. Estas soluciones definen la trayectoria central.
Cuando µ → 0, la trayectoria converge hacia una solución óptima primal–dual.
| Esquema |     | algorítmico |     |     |     |     |     |     |     |     |     |
| ------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
En la práctica, el sistema perturbado se resuelve mediante un método de Newton.
|     | En cada       | iteración: |                 |            |      |           |             |     |           |     |     |
| --- | ------------- | ---------- | --------------- | ---------- | ---- | --------- | ----------- | --- | --------- | --- | --- |
|     | Se linealizan |            | las             | ecuaciones | KKT. |           |             |     |           |     |     |
|     | Se resuelve   |            | un sistema      | lineal     | para | obtener   | direcciones | de  | búsqueda. |     |     |
|     | Se actualizan |            | simultáneamente |            |      | x, y y s. |             |     |           |     |     |
|     | Se reduce     |            | el parámetro    |            | µ.   |           |             |     |           |     |     |
La cantidad
x⊤s
mide la brecha primal–dual. Sobre la trayectoria central se cumple x⊤s = nµ. Cuando esta
| cantidad | tiende      |                | a cero, | se alcanza | optimalidad. |              |         |       |                |           |     |
| -------- | ----------- | -------------- | ------- | ---------- | ------------ | ------------ | ------- | ----- | -------------- | --------- | --- |
| 4.3.     | Comparación |                |         | conceptual |              |              |         |       |                |           |     |
|          |             | Característica |         |            |              |              | Simplex |       | Interior-Point |           |     |
|          |             | Recorre        |         | vértices   |              |              |         | Sí    |                | No        |     |
|          |             | Explota        |         | estructura | combinatoria |              |         | Sí    |                | No        |     |
|          |             | Explota        |         | sistema    | KKT          | directamente |         | No    |                | Sí        |     |
|          |             | Trayectoria    |         | suave      |              |              |         | No    |                | Sí        |     |
|          |             | Eficiencia     |         | en PL      | grandes      |              | Muy     | buena |                | Excelente |     |
Desde una perspectiva estructural, el método simplex explota la geometría combinatoria del
poliedro, mientras que los métodos de puntos interiores explotan su estructura convexa global.
Ambos convergen al mismo óptimo, pero mediante mecanismos matemáticamente distintos.

| 10              | CAPÍTULO   | 1.     | FUNDAMENTOS |          | DE PROGRAMACIÓN |              | LINEAL | Y      | ENTERA |
| --------------- | ---------- | ------ | ----------- | -------- | --------------- | ------------ | ------ | ------ | ------ |
| 5. Programación |            | entera |             | y mixta: | modelos         | y relajación |        | lineal |        |
| 5.1. MILP:      | definición |        |             |          |                 |              |        |        |        |
Un problema de programación lineal entera mixta (MILP) típicamente se escribe como:
c⊤x+d⊤y
|     |     |     | m´ın |         |         |        |     |     | (1.14) |
| --- | --- | --- | ---- | ------- | ------- | ------ | --- | --- | ------ |
|     |     |     | s.a. | Ax+By   | ≥ b     |        |     |     | (1.15) |
|     |     |     |      | x ∈ Zp, | y ∈ Rq, | y ≥ 0. |     |     |        |
Casos particulares: ILP: todas las variables enteras (q = 0) y BIP: variables binarias (x ∈
{0,1}p).
| 5.2. Relajación |     | lineal |     |     |     |     |     |     |     |
| --------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
La relajación lineal se obtiene reemplazando integridad por continuidad:
|           |         |         |             | Zp              |          | Rp.       |     |     |     |
| --------- | ------- | ------- | ----------- | --------------- | -------- | --------- | --- | --- | --- |
|           |         |         | x           | ∈               | −→ x ∈   |           |     |     |     |
| Denotemos | v(MILP) | y v(LP) | los óptimos | (minimización). |          | Entonces: |     |     |     |
|           |         |         |             | v(LP) ≤         | v(MILP). |           |     |     |     |
Esta es la cota inferior base en algoritmos exactos y será el punto de comparación con cotas de
| relajación | lagrangiana | y Benders. |     |     |     |     |     |     |     |
| ---------- | ----------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Se define la brecha de integridad como una medida de pérdida al relajar integridad:
|     |     |     | gap = | v(MILP)−v(LP) |     | ≥ 0. |     |     |     |
| --- | --- | --- | ----- | ------------- | --- | ---- | --- | --- | --- |
Brechas grandes suelen indicar formulaciones débiles; brechas pequeñas son señales de una for-
| mulación | fuerte. |     |     |     |     |     |     |     |     |
| -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
x 2
|     |     |     |     | conv(P | )   |     |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
I
P
x
1
Figura 1.1: Relajación lineal P (negro), puntos enteros factibles (azul) y envoltura convexa
| conv(P | ) (rojo). |     |     |     |     |     |     |     |     |
| ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
I

6. MODELAMIENTO CON VARIABLES BINARIAS: PATRONES CANÓNICOS 11
| 6.  | Modelamiento |     |     | con | variables |     | binarias: |     | patrones | canónicos |
| --- | ------------ | --- | --- | --- | --------- | --- | --------- | --- | -------- | --------- |
La introducción de variables binarias permite representar decisiones lógicas, selecciones dis-
cretas y relaciones condicionales. Una formulación adecuada resulta crucial para el desempeño
| computacional |             | de  | los algoritmos |     | de     | optimización    | entera. |       |     |     |
| ------------- | ----------- | --- | -------------- | --- | ------ | --------------- | ------- | ----- | --- | --- |
| 6.1.          | Activación  |     | condicional    |     |        | y formulaciones |         | Big-M |     |     |
|               | Considérese |     | la implicación |     | lógica |                 |         |       |     |     |
a⊤x
|     |                 |     |       |          | z = | 1 ⇒ | ≤ b,        | z ∈ | {0,1}. |     |
| --- | --------------- | --- | ----- | -------- | --- | --- | ----------- | --- | ------ | --- |
|     | Una formulación |     | Big-M | estándar |     | es  |             |     |        |     |
|     |                 |     |       |          |     | a⊤x | ≤ b+M(1−z). |     |        |     |
Si z = 1, se recupera la restricción original; si z = 0, esta queda relajada.
Interpretación El parámetro M actúa como una cota superior artificial que desactiva la res-
tricción cuando z = 0. Desde el punto de vista geométrico, un valor excesivo de M debilita la
| relajación |               | lineal.       |              |             |             |                 |                |     |     |     |
| ---------- | ------------- | ------------- | ------------ | ----------- | ----------- | --------------- | -------------- | --- | --- | --- |
| Riesgo     | computacional |               |              | Valores     |             | grandes         | de M producen: |     |     |     |
|            | relajaciones  |               | LP débiles,  |             |             |                 |                |     |     |     |
|            | cotas         | inferiores    | pobres,      |             |             |                 |                |     |     |     |
|            | árboles       | de            | ramificación |             | profundos,  |                 |                |     |     |     |
|            | inestabilidad |               | numérica.    |             |             |                 |                |     |     |     |
|            | Siempre       | que           | sea posible, | se          | recomienda: |                 |                |     |     |     |
|            | derivar       | cotas         | válidas      | y           | ajustadas   | para            | M,             |     |     |     |
|            | utilizar      | restricciones |              | indicadoras |             | del             | solver,        |     |     |     |
|            | emplear       | formulaciones |              | extendidas. |             |                 |                |     |     |     |
| 6.2.       | Selección,    |               | cobertura    |             | y           | empaquetamiento |                |     |     |     |
Muchas decisiones combinatorias se expresan mediante variables binarias.
| Selección |     | con | capacidad |     |     |     |     |     |     |     |
| --------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
n
X
|     |     |     |     |     |     | w z ≤ | W,  | z ∈ {0,1}. |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | ---------- | --- | --- |
|     |     |     |     |     |     | i i   |     | i          |     |     |
i=1
Modela la elección de un subconjunto sujeto a una restricción de recursos.
| Cobertura |     | (Set | Cover) |     |     |     |     |     |     |     |
| --------- | --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
X
|     |     |     |     |     |     |     | z i ≥ 1, | ∀j. |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
i∈S(j)
|     | Garantiza | que | cada | elemento | j   | esté cubierto | al menos |     | una vez. |     |
| --- | --------- | --- | ---- | -------- | --- | ------------- | -------- | --- | -------- | --- |

| 12              | CAPÍTULO |      | 1.       | FUNDAMENTOS |     |     | DE PROGRAMACIÓN |     | LINEAL | Y ENTERA |
| --------------- | -------- | ---- | -------- | ----------- | --- | --- | --------------- | --- | ------ | -------- |
| Empaquetamiento |          | (Set | Packing) |             |     |     |                 |     |        |          |
X
|     |     |     |     |     |     | z i ≤ | 1,  | ∀j. |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
i∈S(j)
| Impone | exclusión | mutua |     | entre | selecciones. |     |     |     |     |     |
| ------ | --------- | ----- | --- | ----- | ------------ | --- | --- | --- | --- | --- |
Estos patrones aparecen en problemas de localización, asignación, diseño de redes y planifi-
cación.
| 6.3. Linealización |     |     | de productos |     |     | binarios |     |     |     |     |
| ------------------ | --- | --- | ------------ | --- | --- | -------- | --- | --- | --- | --- |
Los términos no lineales deben ser reformulados para obtener modelos MILP.
| Producto | binario–binario |        |     | Sea    |     |       |        |        |     |     |
| -------- | --------------- | ------ | --- | ------ | --- | ----- | ------ | ------ | --- | --- |
|          |                 |        |     | w      | = z | z ,   | z ,z ∈ | {0,1}. |     |     |
|          |                 |        |     |        | 1   | 2     | 1 2    |        |     |     |
| Una      | reformulación   | lineal |     | exacta | es: |       |        |        |     |     |
|          |                 |        |     |        | w   | ≤ z , |        |        |     |     |
1
|     |     |     |     |     | w   | ≤ z , |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
2
|          |                  |     |     |     | w   | ≥ z         | +z −1,    |              |     |     |
| -------- | ---------------- | --- | --- | --- | --- | ----------- | --------- | ------------ | --- | --- |
|          |                  |     |     |     |     | 1           | 2         |              |     |     |
|          |                  |     |     |     | w   | ∈ {0,1}.    |           |              |     |     |
| Producto | binario–continuo |     |     | Si  | w = | zx, con     | z ∈ {0,1} | y x ∈ [ℓ,u]: |     |     |
|          |                  |     |     |     | w   | ≤ uz,       |           |              |     |     |
|          |                  |     |     |     | w   | ≥ ℓz,       |           |              |     |     |
|          |                  |     |     |     | w   | ≤ x−ℓ(1−z), |           |              |     |     |
|          |                  |     |     |     | w   | ≥ x−u(1−z). |           |              |     |     |
Esta formulación evita el uso explícito de constantes Big-M arbitrarias.
| 6.4. Fortalecimiento |     |     | de  | formulaciones |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- |
Distintas formulaciones pueden describirel mismo conjunto enteropero presentar relajaciones
| lineales | muy diferentes. |     |     |     |     |     |     |     |     |     |
| -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Una formulación se denomina fuerte si su relajación LP aproxima estrechamente al conjunto
| convexo       | entero.    |                      |           |     |     |     |     |     |     |     |
| ------------- | ---------- | -------------------- | --------- | --- | --- | --- | --- | --- | --- | --- |
| Formulaciones |            | fuertes              | permiten: |     |     |     |     |     |     |     |
| menos         | nodos      | en Branch-and-Bound, |           |     |     |     |     |     |     |     |
| mejores       | cotas,     |                      |           |     |     |     |     |     |     |     |
| tiempos       | de cómputo |                      | menores.  |     |     |     |     |     |     |     |
El fortalecimiento mediante reformulación, eliminación de Big-M innecesarios y uso de varia-
| bles auxiliares | es  | una etapa | central |     | en el | diseño | de modelos | eficientes. |     |     |
| --------------- | --- | --------- | ------- | --- | ----- | ------ | ---------- | ----------- | --- | --- |

| 7.  | COTAS, | CERTIFICADOS |              |     | Y ARQUITECTURA |              |     | DE RESOLUCIÓN | 13  |
| --- | ------ | ------------ | ------------ | --- | -------------- | ------------ | --- | ------------- | --- |
| 7.  | Cotas, |              | certificados |     | y              | arquitectura |     | de resolución |     |
Los algoritmos exactos para programación entera se basan en la interacción sistemática entre
| cotas, | descomposición |            | y   | exploración   | del        | espacio | de  | soluciones. |     |
| ------ | -------------- | ---------- | --- | ------------- | ---------- | ------- | --- | ----------- | --- |
| 7.1.   | Cotas          | inferiores |     | y             | superiores |         |     |             |     |
|        | En un          | problema   | de  | minimización: |            |         |     |             |     |
Cota inferior (LB):provienedeunarelajacióndelproblema(lineal,lagrangiana,descom-
|     | puesta, | etc.). |     |     |     |     |     |     |     |
| --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
Cota superior (UB): proviene de una solución factible obtenida mediante heurísticas o
|     | algoritmos |       | exactos.   |          |     |      |     |       |     |
| --- | ---------- | ----- | ---------- | -------- | --- | ---- | --- | ----- | --- |
|     | Estas      | cotas | satisfacen | siempre: |     |      |     |       |     |
|     |            |       |            |          |     | LB ≤ | z⋆  | ≤ UB, |     |
z⋆
|     | donde       | es            | el valor | óptimo. |           |                 |     |         |     |
| --- | ----------- | ------------- | -------- | ------- | --------- | --------------- | --- | ------- | --- |
|     | El objetivo | computacional |          |         | es cerrar | progresivamente |     | el gap: |     |
UB−LB
.
|UB|
|      | Cuando       | este | se anula, | se certifica |     | optimalidad. |     |     |     |
| ---- | ------------ | ---- | --------- | ------------ | --- | ------------ | --- | --- | --- |
| 7.2. | Certificados |      | de        | optimalidad  |     |              |     |     |     |
Una solución óptima no solo debe encontrarse, sino también demostrarse.
Programación lineal Una solución dual factible certifica una cota inferior por dualidad débil.
| Programación |              |                  | entera         | La optimalidad   |           | se     | prueba | cuando:            |     |
| ------------ | ------------ | ---------------- | -------------- | ---------------- | --------- | ------ | ------ | ------------------ | --- |
|              | existe       | una              | solución       | entera           | con valor | UB,    |        |                    |     |
|              | todas        | las relajaciones |                | exploradas       |           | tienen | valor  | ≥ UB.              |     |
|              | Esto         | constituye       | un certificado |                  | implícito | basado |        | en cotas globales. |     |
| 7.3.         | Arquitectura |                  |                | Branch-and-Bound |           |        |        |                    |     |
La mayoría de los solvers comerciales utilizan variantes avanzadas de Branch-and-Bound.
|     | El algoritmo |      | mantiene    | un         | árbol de        | subproblemas: |      |        |     |
| --- | ------------ | ---- | ----------- | ---------- | --------------- | ------------- | ---- | ------ | --- |
|     | cada         | nodo | corresponde | a          | una relajación, |               |      |        |     |
|     | cada         | nodo | genera      | una cota   | inferior        | local,        |      |        |     |
|     | soluciones   |      | factibles   | actualizan | el              | UB global.    |      |        |     |
|     | Un nodo      | se   | poda si:    |            |                 |               |      |        |     |
|     |              |      |             |            |                 | LB            | ≥ UB | .      |     |
|     |              |      |             |            |                 | nodo          |      | global |     |
El proceso continúa hasta que todos los nodos están podados o explorados.

| 14  |             | CAPÍTULO |     | 1.       | FUNDAMENTOS  |     | DE  | PROGRAMACIÓN  | LINEAL    | Y ENTERA |
| --- | ----------- | -------- | --- | -------- | ------------ | --- | --- | ------------- | --------- | -------- |
| 8.  | Heurísticas |          |     | básicas: | construcción |     |     | de soluciones | factibles |          |
Las heurísticas no son componentes accesorios, sino elementos centrales en la arquitectura de
resolución.
Su función principal es generar rápidamente buenas cotas superiores, acelerando la poda del
| árbol | de búsqueda. |     |            |     |         |     |     |     |     |     |
| ----- | ------------ | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- |
| 8.1.  | Esquema      |     | heurístico |     | general |     |     |     |     |     |
Para un problema de minimización m´ın{f(x) : x ∈ V}, un esquema genérico es:
|      | 1. Construcción  |          | inicial         | de            | una solución     | factible | x(0). |     |     |     |
| ---- | ---------------- | -------- | --------------- | ------------- | ---------------- | -------- | ----- | --- | --- | --- |
|      | 2. Mejora        | mediante |                 | búsqueda      | local.           |          |       |     |     |     |
|      | 3. Actualización |          | del             | mejor         | UB conocido.     |          |       |     |     |     |
|      | 4. Reinicio      | o        | diversificación |               | si es necesario. |          |       |     |     |     |
| 8.2. | Búsqueda         |          | local           | y vecindarios |                  |          |       |     |     |     |
Un vecindario N(x) define el conjunto de soluciones accesibles desde x mediante movimientos
elementales (intercambio, inserción, inversión, activación binaria, etc.).
|      | Una solución   |             | x es óptimo  |                   | local si:   |          |            |          |     |     |
| ---- | -------------- | ----------- | ------------ | ----------------- | ----------- | -------- | ---------- | -------- | --- | --- |
|      |                |             |              |                   | f(x)        | ≤ f(x′), | ∀x′        | ∈ N(x).  |     |     |
|      | Los algoritmos |             | iteran       | mientras          | exista      | mejora:  |            |          |     |     |
|      |                |             |              |                   | ∃x′         |          | f(x′)      |          |     |     |
|      |                |             |              |                   |             | ∈ N(x)   | :          | < f(x).  |     |     |
| 8.3. | Estancamiento  |             |              | y diversificación |             |          |            |          |     |     |
|      | La búsqueda    |             | local puede  | quedar            | atrapada    |          | en óptimos | locales. |     |     |
|      | Para evitarlo, |             | se emplean   |                   | estrategias | como:    |            |          |     |     |
|      | reinicios      | aleatorios, |              |                   |             |          |            |          |     |     |
|      | perturbaciones |             | controladas, |                   |             |          |            |          |     |     |
|      | vecindarios    |             | variables,   |                   |             |          |            |          |     |     |
|      | memoria        |             | adaptativa   | (tabú).           |             |          |            |          |     |     |
Estas técnicas permiten explorar regiones alternativas del espacio de soluciones.
| 8.4. | Integración |     | con | algoritmos |     | exactos |     |     |     |     |
| ---- | ----------- | --- | --- | ---------- | --- | ------- | --- | --- | --- | --- |
En solvers modernos, las heurísticas operan de forma integrada con los métodos exactos.
|     | Se ejecutan |     | en nodos     | del | árbol          | B&B. |     |     |     |     |
| --- | ----------- | --- | ------------ | --- | -------------- | ---- | --- | --- | --- | --- |
|     | Aprovechan  |     | información  |     | dual.          |      |     |     |     |     |
|     | Se activan  |     | tras cambios |     | estructurales. |      |     |     |     |     |
Esta interacción explica gran parte del rendimiento de los solucionadores actuales.

| Capítulo   |               |     | 2        |             |                 |           |     |                     |       |
| ---------- | ------------- | --- | -------- | ----------- | --------------- | --------- | --- | ------------------- | ----- |
| Relajación |               |     |          | Lagrangiana |                 |           |     |                     |       |
| 1.         | Relajaciones: |     |          | definición  |                 | formal    |     | y consecuencias     |       |
| 1.1.       | Problema      |     | original |             | (minimización)  |           |     |                     |       |
|            | Consideremos  | un  | problema |             | de minimización |           |     | en forma abstracta: |       |
|            |               |     |          |             | (P)             | m´ın{f(x) |     | : x ∈ V },          | (2.1) |
donde:
|      | x denota       | el vector  |                 | de decisión, |               |                |           |                  |       |
| ---- | -------------- | ---------- | --------------- | ------------ | ------------- | -------------- | --------- | ---------------- | ----- |
|      | V es el        | conjunto   | factible        |              | del problema  |                | original, |                  |       |
|      | f(·) es        | la función | objetivo.       |              |               |                |           |                  |       |
| 1.2. | Definición     |            | de              | relajación   |               |                |           |                  |       |
|      | Una relajación |            | de (P)          | es           | otro problema |                | de        | minimización:    |       |
|      |                |            |                 |              | (RP)          | m´ın{g(x)      |           | : x ∈ W },       | (2.2) |
| tal  | que se cumplen |            | simultáneamente |              |               | las siguientes |           | condiciones:     |       |
|      | 1. Relajación  | del        | conjunto        |              | factible:     |                | W ⊇       | V,               |       |
|      | 2. Objetivo    | no         | mayor           | sobre        | V:            | g(x)           | ≤ f(x)    | para todo x ∈ V. |       |
La interpretación indica que el problema relajado (2.2) admite al menos todas las soluciones
factibles del problema original y, eventualmente, otras adicionales. Además, sobre el conjunto
original V, su función objetivo no excede a la del problema original. Como consecuencia, el valor
óptimo del relajado proporciona una cota inferior del valor óptimo original.
Denotemos por v(P) y v(RP) los valores óptimos de (2.1) y (2.2), respectivamente. Entonces:
|      |            |     |     |             |     | v(RP) | ≤             | v(P). | (2.3) |
| ---- | ---------- | --- | --- | ----------- | --- | ----- | ------------- | ----- | ----- |
| 1.3. | Relajación |     | por | eliminación |     | de    | restricciones |       |       |
Un caso habitual ocurre cuando el problema original puede escribirse como
|     |     |     |     |     | V   | = {x | ∈ X | : h(x) ≤ 0}. |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | ------------ | --- |
15

| 16  |     | CAPÍTULO | 2. RELAJACIÓN | LAGRANGIANA |
| --- | --- | -------- | ------------- | ----------- |
Si se eliminan algunas de esas restricciones, se obtiene un conjunto más grande
h˜(x)
|     | W = {x | ∈ X : | ≤ 0}, |     |
| --- | ------ | ----- | ----- | --- |
h˜
donde contiene sólo una parte de las restricciones de h. En este caso, usualmente se mantiene
la misma función objetivo, es decir, g(x) = f(x), y la desigualdad (2.3) sigue siendo válida.
Enproblemasenteros,unarelajaciónclásicaconsisteenreemplazarrestriccionesdeintegridad
|     |     | {0,1}n, | [0,1]n. |     |
| --- | --- | ------- | ------- | --- |
por un dominio continuo. Por ejemplo, si x ∈ se relaja a x ∈ Nuevamente, el
conjunto factible se amplía y se obtiene una cota inferior para el problema original.

| 2.  | RELAJACIÓN |     | LAGRANGIANA |             |     |     |     |     |     |     | 17  |
| --- | ---------- | --- | ----------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| 2.  | Relajación |     |             | lagrangiana |     |     |     |     |     |     |     |
2.1. Motivación
En muchos problemas de optimización, especialmente enteros o mixtos, ciertas restricciones
acoplan variables de una forma que destruye la estructura explotable del problema.
|     | Ejemplos      | típicos |     | incluyen:    |         |             |            |     |              |     |     |
| --- | ------------- | ------- | --- | ------------ | ------- | ----------- | ---------- | --- | ------------ | --- | --- |
|     | restricciones |         | de  | balance      | global, |             |            |     |              |     |     |
|     | restricciones |         | de  | cobertura    |         | exacta,     |            |     |              |     |     |
|     | restricciones |         | de  | capacidad    |         | compartida, |            |     |              |     |     |
|     | restricciones |         | de  | consistencia |         | entre       | decisiones |     | jerárquicas. |     |     |
Larelajación lagrangiana consisteenretirarexplícitamenteestasrestriccionesdelconjunto
factible e incorporarlas a la función objetivo mediante penalizaciones lineales.
|     | Su propósito |     | es:              |     |           |     |                    |           |           |              |     |
| --- | ------------ | --- | ---------------- | --- | --------- | --- | ------------------ | --------- | --------- | ------------ | --- |
|     | preservar    |     | la estructura    |     | favorable |     | del conjunto       |           | restante, |              |     |
|     | obtener      |     | una relajación   |     | válida    | del | problema           | original, |           |              |     |
|     | generar      |     | cotas inferiores |     | fuertes   | y   | computacionalmente |           |           | explotables. |     |
2.2. Planteamiento
|     | Consideremos |     | el  | problema | de   | minimización |     |                |     |               |       |
| --- | ------------ | --- | --- | -------- | ---- | ------------ | --- | -------------- | --- | ------------- | ----- |
|     |              |     |     | (P)      | m´ın | f(x)         |     |                |     |               | (2.4) |
|     |              |     |     |          | s.a. | g(x)         | ≤ 0 | (restricciones |     | complicantes) | (2.5) |
|     |              |     |     |          |      | x ∈          | X   | (estructura    |     | mantenida).   | (2.6) |
Aquí:
|      | X       | es un | conjunto    | relativamente |                   |     | simple, | posiblemente |     | entero,  |     |
| ---- | ------- | ----- | ----------- | ------------- | ----------------- | --- | ------- | ------------ | --- | -------- | --- |
|      | g(x)    | ≤ 0   | representa  |               | las restricciones |     | que     | se decide    |     | relajar. |     |
| 2.3. | Función |       | lagrangiana |               |                   |     |         |              |     |          |     |
Asociando multiplicadores λ ≥ 0 a las restricciones relajadas, se define la función lagrangiana
|     |     |     |     |     | L(x,λ) |     | = f(x)+λ⊤g(x), |     |     | λ ≥ 0. |     |
| --- | --- | --- | --- | --- | ------ | --- | -------------- | --- | --- | ------ | --- |
Interpretación
|     | Si  | g i (x) | > 0, la | restricción |          | i se viola | y esa         | violación |     | es penalizada. |     |
| --- | --- | ------- | ------- | ----------- | -------- | ---------- | ------------- | --------- | --- | -------------- | --- |
|     | Si  | g (x)   | ≤ 0, el | término     | asociado |            | no incrementa |           | el  | objetivo.      |     |
i
|      | El       | vector           | λ controla |             | la severidad |           | de la penalización. |             |             |     |     |
| ---- | -------- | ---------------- | ---------- | ----------- | ------------ | --------- | ------------------- | ----------- | ----------- | --- | --- |
| 2.4. | Problema |                  |            | lagrangiano |              |           |                     |             |             |     |     |
|      | Para     | un multiplicador |            |             | fijo λ,      | se define | el problema         |             | lagrangiano |     |     |
|      |          |                  |            |             |              | (R        | )                   | m´ınL(x,λ). |             |     |     |
λ
x∈X
Lasrestriccionescomplicantesdesaparecenexplícitamentedelconjuntofactible,yladificultad
| se  | traslada | al  | ajuste | adecuado | de  | los multiplicadores. |     |     |     |     |     |
| --- | -------- | --- | ------ | -------- | --- | -------------------- | --- | --- | --- | --- | --- |

| 18           |     |                          |                     | CAPÍTULO | 2.      | RELAJACIÓN | LAGRANGIANA |
| ------------ | --- | ------------------------ | ------------------- | -------- | ------- | ---------- | ----------- |
| 2.5. Función |     | dual lagrangiana         |                     |          |         |            |             |
| Definimos    | la  | función dual lagrangiana |                     | por      |         |            |             |
|              |     |                          | (cid:8) f(x)+λ⊤g(x) |          | (cid:9) |            |             |
|              |     | θ(λ)                     | = m´ın              |          | , λ     | ≥ 0.       |             |
x∈X
Estafunciónasigna,acadavectordemultiplicadores,elvaloróptimodelproblemalagrangiano
asociado.
| 2.6. Dual | lagrangiano |           |      |           |     |     |     |
| --------- | ----------- | --------- | ---- | --------- | --- | --- | --- |
| El dual   | lagrangiano | se define | como |           |     |     |     |
|           |             |           | (D)  | ma´xθ(λ). |     |     |     |
λ≥0
Su objetivo es encontrar el mejor vector de multiplicadores posible, de modo de obtener la
| cota inferior  | más | fuerte inducida | por la relajación. |          |     |     |     |
| -------------- | --- | --------------- | ------------------ | -------- | --- | --- | --- |
| 2.7. Propiedad |     | fundamental:    | cota               | inferior |     |     |     |
Sea z⋆ el valor óptimo del problema original. Entonces, para todo λ ≥ 0,
|     |     |     |     | θ(λ) ≤ z⋆. |     |     |     |
| --- | --- | --- | --- | ---------- | --- | --- | --- |
Demostración. Sea x⋆ una solución óptima factible del problema original. Como g(x⋆) ≤ 0 y
| λ ≥ 0, se | tiene |     |     |     |     |     |     |
| --------- | ----- | --- | --- | --- | --- | --- | --- |
λ⊤g(x⋆)
≤ 0.
Por lo tanto,
|           |       | L(x⋆,λ)          | = f(x⋆)+λ⊤g(x⋆) |              | ≤ f(x⋆) | = z⋆. |     |
| --------- | ----- | ---------------- | --------------- | ------------ | ------- | ----- | --- |
| Como θ(λ) | es el | mínimo de L(x,λ) | sobre x         | ∈ X, resulta |         |       |     |
|           |       |                  | θ(λ)            | ≤ L(x⋆,λ)    | ≤ z⋆.   |       |     |

| 3.   | PROPIEDADES |     | DEL              | DUAL  | LAGRANGIANO |             |                     |          | 19  |
| ---- | ----------- | --- | ---------------- | ----- | ----------- | ----------- | ------------------- | -------- | --- |
| 3.   | Propiedades |     |                  | del   | dual        | lagrangiano |                     |          |     |
| 3.1. | Concavidad  |     |                  | de la | función     | dual        |                     |          |     |
|      | La función  |     | dual lagrangiana |       |             |             |                     |          |     |
|      |             |     |                  |       |             |             | (cid:8) f(x)+λ⊤g(x) | (cid:9)  |     |
|      |             |     |                  |       | θ(λ) =      | m´ın        |                     | , λ ≥ 0, |     |
x∈X
es una función cóncava, incluso cuando el problema primal es entero o no convexo.
| Demostración. |     |     | Para | cada x | ∈ X, la | función |     |     |     |
| ------------- | --- | --- | ---- | ------ | ------- | ------- | --- | --- | --- |
f(x)+λ⊤g(x)
|     |     |     |     |     |     | λ   | 7→  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
es afín en λ. La función θ(λ) es el mínimo puntual de esta familia de funciones afines. Por tanto,
θ es cóncava.
| 3.2. | No  | diferenciabilidad |     |     | y   | estructura | por | tramos |     |
| ---- | --- | ----------------- | --- | --- | --- | ---------- | --- | ------ | --- |
La función θ(λ) es típicamente no diferenciable. La razón es que el minimizador de
|     |     |     |     |     |     | m´ın | {f(x)+λ⊤g(x)} |     |     |
| --- | --- | --- | --- | --- | --- | ---- | ------------- | --- | --- |
x∈X
| puede | cambiar |          | bruscamente |          | cuando | λ varía. |                |     |     |
| ----- | ------- | -------- | ----------- | -------- | ------ | -------- | -------------- | --- | --- |
|       | Cada    | solución | x ∈         | X define | una    | función  | afín           |     |     |
|       |         |          |             |          |        | ϕ (λ)    | = f(x)+λ⊤g(x), |     |     |
x
y la función dual lagrangiana corresponde a la envolvente inferior de todas ellas. Cuando cambia
la solución lagrangiana óptima, cambia la pendiente de θ, generando quiebres.
| 3.3. | Subgradientes |         |          | del | dual     | lagrangiano |              |             |     |
| ---- | ------------- | ------- | -------- | --- | -------- | ----------- | ------------ | ----------- | --- |
|      | Sea           | λ ≥ 0 y | sea x(λ) | una | solución | óptima      | del problema | lagrangiano |     |
m´ın{f(x)+λ⊤g(x)}.
|     |     |     |     |     | (R  | )   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
λ
x∈X
Entonces,
|     |                 |     |     |         |     |     | s(λ) = g (cid:0) x(λ) | (cid:1) | (2.7) |
| --- | --------------- | --- | --- | ------- | --- | --- | --------------------- | ------- | ----- |
| es  | un subgradiente |     | de  | θ en λ. |     |     |                       |         |       |
Interpretación
|     | Si  | s (λ) > | 0, la | restricción | relajada |     | i está violada. |     |     |
| --- | --- | ------- | ----- | ----------- | -------- | --- | --------------- | --- | --- |
i
|     | Si  | s (λ) < | 0, la | restricción | presenta |     | holgura. |     |     |
| --- | --- | ------- | ----- | ----------- | -------- | --- | -------- | --- | --- |
i
|     | Si  | s (λ) = | 0, la | restricción | está | activa | en ese | sentido local. |     |
| --- | --- | ------- | ----- | ----------- | ---- | ------ | ------ | -------------- | --- |
i

| 20  | CAPÍTULO | 2. RELAJACIÓN | LAGRANGIANA |
| --- | -------- | ------------- | ----------- |
3.4. Interpretación geométrica
θ(λ)
|     | función | cóncava |     |
| --- | ------- | ------- | --- |
quiebre
λ
Figura 2.1: Estructura típica de la función dual lagrangiana: cóncava, no diferenciable y definida
por tramos afines.

| 4. OPTIMIZACIÓN |            |     | DEL   | DUAL:  | MÉTODO |             | DEL | SUBGRADIENTE |              | 21  |
| --------------- | ---------- | --- | ----- | ------ | ------ | ----------- | --- | ------------ | ------------ | --- |
| 4. Optimización |            |     |       | del    | dual:  | método      |     | del          | subgradiente |     |
| En              | la Sección | 3   | vimos | que el | dual   | lagrangiano |     |              |              |     |
m´ın{f(x)+λ⊤g(x)},
|     |     |     | (D) | ma´x | θ(λ), |     | θ(λ) | =   |     |     |
| --- | --- | --- | --- | ---- | ----- | --- | ---- | --- | --- | --- |
|     |     |     |     | λ≥0  |       |     |      | x∈X |     |     |
es un problema cóncavo pero, en general, no diferenciable. El método clásico para abordarlo es
| el método | del | subgradiente. |     |     |     |     |     |     |     |     |
| --------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
4.1. Subgradiente
Sea θ :m→ una función cóncava. Un vector s ∈m es un subgradiente de θ en λ si
|     |         |              |     | θ(λ′)   | θ(λ)+s⊤(λ′−λ), |        |      |                | ∀λ′ ∈m |       |
| --- | ------- | ------------ | --- | ------- | -------------- | ------ | ---- | -------------- | ------ | ----- |
|     |         |              |     |         | ≤              |        |      |                | .      | (2.8) |
| En  | el caso | lagrangiano, |     | si x(λ) | es             | óptimo | para | (R ), entonces |        |       |
λ
|                    |                  |        |         |      |       | s(λ)     | = g(x(λ))         |             |             |     |
| ------------------ | ---------------- | ------ | ------- | ---- | ----- | -------- | ----------------- | ----------- | ----------- | --- |
| es un subgradiente |                  |        | de θ en | λ.   |       |          |                   |             |             |     |
| 4.2.               | Idea del         | método |         |      |       |          |                   |             |             |     |
| Dado               | un multiplicador |        |         | λk ≥ | 0, se | resuelve | el                | subproblema | lagrangiano |     |
|                    |                  |        |         |      | xk ∈  |          | {f(x)+(λk)⊤g(x)}, |             |             |     |
x∈X
| y luego   | se construye  |              | el vector |      |          |      |             |        |     |       |
| --------- | ------------- | ------------ | --------- | ---- | -------- | ---- | ----------- | ------ | --- | ----- |
|           |               |              |           |      |          |      | sk = g(xk), |        |     |       |
| que actúa | como          | subgradiente |           | de   | θ en     | λk.  |             |        |     |       |
| La        | actualización |              | básica    | toma | la forma |      |             |        |     |       |
|           |               |              |           |      |          | λk+1 | = λk        | +α sk. |     | (2.9) |
k
Comoeldominiodualimponeλ ≥ 0,enrelajaciónlagrangianaseutilizalaversiónproyectada:
|     |     |     |     |     | λk+1 |     | (cid:0) | λk sk(cid:1) |     |        |
| --- | --- | --- | --- | --- | ---- | --- | ------- | ------------ | --- | ------ |
|     |     |     |     |     |      | =   | ΠRm     | +α           | ,   | (2.10) |
|     |     |     |     |     |      |     | +       | k            |     |        |
donde
|     |     |     |     | (cid:2) | (cid:3) |            |     |          |          |     |
| --- | --- | --- | --- | ------- | ------- | ---------- | --- | -------- | -------- | --- |
|     |     |     |     | ΠRm     | (u)     | = ma´x{0,u |     | i }, i = | 1,...,m. |     |
|     |     |     |     | +       | i       |            |     |          |          |     |
Interpretación Si g (xk) > 0, la restricción relajada i está violada y el método incrementa
i
(xk)
la penalización correspondiente. Si g i < 0, la restricción presenta holgura y la penalización
| asociada | puede | reducirse. |     |     |     |     |     |     |     |     |
| -------- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |

| 22   |                  |         |     |             |     |       |           | CAPÍTULO |     | 2. RELAJACIÓN | LAGRANGIANA |     |
| ---- | ---------------- | ------- | --- | ----------- | --- | ----- | --------- | -------- | --- | ------------- | ----------- | --- |
| 4.3. |                  | Esquema |     | algorítmico |     |       |           |          |     |               |             |     |
|      | El procedimiento |         |     | conceptual  |     | puede | resumirse | así:     |     |               |             |     |
λ0
|     | 1. Inicializar |     |                | ≥ 0 y | fijar un    | criterio | de parada. |                   |     |     |     |     |
| --- | -------------- | --- | -------------- | ----- | ----------- | -------- | ---------- | ----------------- | --- | --- | --- | --- |
|     | 2. Resolver    |     | el subproblema |       | lagrangiano |          |            |                   |     |     |     |     |
|     |                |     |                |       |             | xk       |            | {f(x)+(λk)⊤g(x)}. |     |     |     |     |
∈ x∈X
|     | 3. Evaluar |     | la función |     | dual |       |                   |     |     |     |     |     |
| --- | ---------- | --- | ---------- | --- | ---- | ----- | ----------------- | --- | --- | --- | --- | --- |
|     |            |     |            |     |      | θ(λk) | f(xk)+(λk)⊤g(xk). |     |     |     |     |     |
=
|      | 4. Construir  |          | un    | subgradiente    |     |          |            |          |     |     |     |     |
| ---- | ------------- | -------- | ----- | --------------- | --- | -------- | ---------- | -------- | --- | --- | --- | --- |
|      |               |          |       |                 |     |          | sk         | = g(xk). |     |     |     |     |
|      | 5. Actualizar |          | los   | multiplicadores |     | mediante |            | (2.10).  |     |     |     |     |
|      | 6. Repetir    |          | hasta | satisfacer      | el  | criterio | de parada. |          |     |     |     |     |
| 4.4. |               | Elección | del   | tamaño          |     | de paso  |            |          |     |     |     |     |
La calidad del método depende fuertemente de la elección de α k . Una regla clásica y muy
| utilizada |     | en relajación |     | lagrangiana |     | es  | el paso | tipo Polyak: |     |     |     |     |
| --------- | --- | ------------- | --- | ----------- | --- | --- | ------- | ------------ | --- | --- | --- | --- |
UB−θ(λk)
|       |     |     |          |          | α   | = β          |       | ,       | 0 < | β < 2, |     | (2.11) |
| ----- | --- | --- | -------- | -------- | --- | ------------ | ----- | ------- | --- | ------ | --- | ------ |
|       |     |     |          |          |     | k            | ∥sk∥2 |         |     |        |     |        |
| donde | UB  | es  | una cota | superior |     | del problema |       | primal. |     |        |     |        |
Interpretación
|     | Si  | la cota   | dual | θ(λk)      | está       | lejos de    | UB, el  | paso              | es grande.       |     |     |     |
| --- | --- | --------- | ---- | ---------- | ---------- | ----------- | ------- | ----------------- | ---------------- | --- | --- | --- |
|     | A   | medida    | que  | el gap     | disminuye, |             | el paso | se reduce         | automáticamente. |     |     |     |
|     | El  | parámetro |      | β controla | la         | agresividad | de      | la actualización. |                  |     |     |     |
Otras reglas posibles También existen otras estrategias de tamaño de paso, por ejemplo:
|     | pasos | decrecientes, |     |     | como | α = c/(k+1), |     |     |     |     |     |     |
| --- | ----- | ------------- | --- | --- | ---- | ------------ | --- | --- | --- | --- | --- | --- |
k
|      | pasos  | constantes  |              | por     | bloques, |                  |         |               |       |       |     |     |
| ---- | ------ | ----------- | ------------ | ------- | -------- | ---------------- | ------- | ------------- | ----- | ----- | --- | --- |
|      | reglas | adaptativas |              | basadas |          | en estancamiento |         | del           | valor | dual. |     |     |
| 4.5. |        | Qué         | se garantiza |         | (y       | qué              | no) con | subgradientes |       |       |     |     |
Garantía típica Bajo hipótesis apropiadas sobre la elección del tamaño de paso, el método
permite aproximar el óptimo dual y mejorar progresivamente la mejor cota dual encontrada.
Limitaciones
|     | Las | iteraciones |     | λk pueden |     | no converger. |     |     |     |     |     |     |
| --- | --- | ----------- | --- | --------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
θ(λk)
Los valores pueden oscilar; por ello, usualmente se registra el mejor valor dual obte-
nido.
En problemas enteros puede existir duality gap: aun alcanzando el óptimo dual, no necesa-
|     | riamente |     | se obtiene |     | el óptimo | primal. |     |     |     |     |     |     |
| --- | -------- | --- | ---------- | --- | --------- | ------- | --- | --- | --- | --- | --- | --- |

| 4. OPTIMIZACIÓN | DEL       | DUAL: MÉTODO | DEL SUBGRADIENTE |     | 23  |
| --------------- | --------- | ------------ | ---------------- | --- | --- |
| 4.6. Criterios  | de parada | prácticos    |                  |     |     |
En aplicaciones, el método suele detenerse usando una combinación de criterios como:
| número        | máximo de | iteraciones,  |             |     |     |
| ------------- | --------- | ------------- | ----------- | --- | --- |
| estancamiento | del mejor | valor dual    | encontrado, |     |     |
| norma pequeña | del       | subgradiente, |             |     |     |
UB−θk
| gap estimado |     | inferior a | un umbral prefijado. |     |     |
| ------------ | --- | ---------- | -------------------- | --- | --- |
ma´x
| 4.7. Dibujo: | update | y proyección |     |     |     |
| ------------ | ------ | ------------ | --- | --- | --- |
λ
2
λ≥0
|     |     | Si algún | componente queda | negativo, |     |
| --- | --- | -------- | ---------------- | --------- | --- |
=ma´x{0,λ˜
|     |     | se proyecta: | λk+1 | }.  |     |
| --- | --- | ------------ | ---- | --- | --- |
|     |     |              | i    | i   |     |
λk
+α sk
k
λk+1
λ
λ˜ 1
Figura 2.2: Paso de subgradiente con proyección al ortante no negativo.

| 24  |             |     |              |     |     |     | CAPÍTULO       | 2.  | RELAJACIÓN | LAGRANGIANA |
| --- | ----------- | --- | ------------ | --- | --- | --- | -------------- | --- | ---------- | ----------- |
| 5.  | Heurísticas |     | lagrangianas |     |     |     | y recuperación |     | primal     |             |
La relajación lagrangiana produce buenas cotas inferiores, pero las soluciones x(λ) suelen
ser inviables para el problema original. Para obtener cotas superiores se utilizan heurísticas
lagrangianas.
| 5.1. | Principio | general |     |     |     |     |     |     |     |     |
| ---- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
El principio es transformar una solución lagrangiana x(λ) en una solución factible xfeas del
| problema | original:       |         |      |          |      |      |     |        |     |     |
| -------- | --------------- | ------- | ---- | -------- | ---- | ---- | --- | ------ | --- | --- |
|          |                 |         |      |          |      | x(λ) | −→  | xfeas. |     |     |
| Rol      | en el algoritmo |         |      |          |      |      |     |        |     |     |
|          | Entregan        | una     | cota | superior | UB.  |      |     |        |     |     |
|          | Permiten        | evaluar | el   | duality  | gap. |      |     |        |     |     |
Mejoran el desempeño del método de subgradiente (por ejemplo, mediante pasos tipo Pol-
yak).
| 5.2. | Clases | de  | heurísticas |     | lagrangianas |     |     |     |     |     |
| ---- | ------ | --- | ----------- | --- | ------------ | --- | --- | --- | --- | --- |
1. Heurísticas de reparación (repair) Corrigen directamente las violaciones de las restric-
ciones relajadas:
|      | eliminar         | excesos,    |                     |            |          |                    |               |                   |     |     |
| ---- | ---------------- | ----------- | ------------------- | ---------- | -------- | ------------------ | ------------- | ----------------- | --- | --- |
|      | reasignar        | flujos,     |                     |            |          |                    |               |                   |     |     |
|      | forzar           | coberturas  | faltantes.          |            |          |                    |               |                   |     |     |
| 2.   | Heurísticas      | greedy      |                     | guiadas    | por      | multiplicadores    |               |                   |     |     |
|      | Se interpretan   |             | los multiplicadores |            |          | como               | precios.      |                   |     |     |
|      | Se construye     | una         | solución            |            | factible | minimizando        |               | costos reducidos. |     |     |
| 3.   | Heurísticas      | híbridas    |                     |            |          |                    |               |                   |     |     |
|      | La solución      | lagrangiana |                     | inicializa |          | un                 | método        | local.            |     |     |
|      | Se combina       | con         | búsqueda            |            | local    | o metaheurísticas. |               |                   |     |     |
| 5.3. | Relación         | con         | el                  | dual       |          |                    |               |                   |     |     |
|      | Cuanto mejor     | sea         | la heurística       |            | primal:  |                    |               |                   |     |     |
|      | menor            | será el     | duality             | gap,       |          |                    |               |                   |     |     |
|      | más informativos |             | serán               | los        | pasos    | del                | subgradiente, |                   |     |     |
|      | más rápido       | convergerá  |                     | el         | esquema  | global.            |               |                   |     |     |