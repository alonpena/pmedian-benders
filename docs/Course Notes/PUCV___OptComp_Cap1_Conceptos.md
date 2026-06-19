| Programación | lineal         | y entera      |
| ------------ | -------------- | ------------- |
| Capítulo     | 1: fundamentos | estructurales |
Pablo Torrealba
Marzo 2026
1/39

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
2/39

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
3/39

| ¿Qué | estudia | la  | programación |     | matemática? |     |     |
| ---- | ------- | --- | ------------ | --- | ----------- | --- | --- |
Idea central: modelar decisiones y optimizarlas bajo restricciones.
| Un  | modelo         | contiene  | cuatro       |         | elementos: |                  |              |
| --- | -------------- | --------- | ------------ | ------- | ---------- | ---------------- | ------------ |
|     | Variables      |           | de decisión: |         | lo que     | puede elegirse.  |              |
|     | Función        | objetivo: |              | lo que  | se desea   | minimizar        | o maximizar. |
|     | Restricciones: |           | condiciones  |         | que        | deben cumplirse. |              |
|     | Dominio:       |           | continuo,    | entero, | binario    | o mixto.         |              |
|     |                |           |              |         | m´ın{f(x)  | : x ∈            | X }          |
Mensaje del curso:nobastaconqueelmodeloseacorrecto;tambiéndebeserresoluble
computacionalmente.
4/39

| Tres ideas    | transversales | del capítulo |            |                   |
| ------------- | ------------- | ------------ | ---------- | ----------------- |
| 1. Estructura |               | 2. Cotas     | y dualidad | 3. Descomposición |
¿Qué restricciones generan la ¿Cómo evaluar la calidad de ¿Cómo explotar la estructura
| dificultad? |     | una solución? |     | del problema? |
| ----------- | --- | ------------- | --- | ------------- |
¿Qué parte del modelo acopla ¿Cómo certificar optimalidad ¿Cómo separar un modelo
| las decisiones? |              | o infactibilidad? |              | grande en subproblemas? |
| --------------- | ------------ | ----------------- | ------------ | ----------------------- |
|                 | Modelamiento |                   |              | Resolución              |
|                 | estructura   | del problema      | relajaciones | y algoritmos            |
5/39

| Ejemplo mínimo: | mochila | binaria |     |
| --------------- | ------- | ------- | --- |
Seleccionar proyectos con beneficio p , costo a y presupuesto B.
|     |     | i   | i   |
| --- | --- | --- | --- |
n
(cid:88)
|     |     | m´ax p z |     |
| --- | --- | -------- | --- |
i i
i=1
n
(cid:88)
|     |     | s.a. a z | ≤ B, |
| --- | --- | -------- | ---- |
i i
i=1
|     |     | z ∈ {0,1}, | i = 1,...,n. |
| --- | --- | ---------- | ------------ |
i
Lectura estructural
| Una sola      | restricción acoplante. |                   |                |
| ------------- | ---------------------- | ----------------- | -------------- |
| La dificultad | proviene               | de la integridad. |                |
| Si z ∈ [0,1], | obtenemos              | una relajación    | LP y una cota. |
i
6/39

| De LP | a MILP: | qué cambia | realmente |     |          |
| ----- | ------- | ---------- | --------- | --- | -------- |
|       | x       | LP         |           | x   | MILP     |
|       | 2       |            |           | 2   |          |
|       |         | óptimo     |           |     | conv(P ) |
|       |         | en vértice |           |     | I        |
x x
1 1
LP optimiza sobre un poliedro convexo. MILP introduce estructura discreta: los puntos enteros
|     |     | determinan | la solución | y la calidad de | la relajación. |
| --- | --- | ---------- | ----------- | --------------- | -------------- |
7/39

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
8/39

| Programación | lineal:   | forma estándar | y geometría |     |
| ------------ | --------- | -------------- | ----------- | --- |
| Una forma    | típica de | PL es:         |             |     |
c⊤x
m´ın
s.a. Ax ≤ b,
x ≥ 0.
| El conjunto | factible | es un poliedro: |     |     |
| ----------- | -------- | --------------- | --- | --- |
Rn
|         |             | P = {x ∈ | : Ax ≤ b, | x ≥ 0}. |
| ------- | ----------- | -------- | --------- | ------- |
| Teorema | fundamental | del PL   |           |         |
Si el problema es factible y tiene óptimo finito, existe una solución óptima en un punto
| extremo | del poliedro. |     |     |     |
| ------- | ------------- | --- | --- | --- |
9/39

Poliedro y puntos extremos
x
2
óptimo
v5 v4
v3
v1 v2
x
1
Simplex se mueve entre estos vértices. Los métodos de puntos interiores explotan el
10/39
mismo poliedro, pero sin recorrer necesariamente sus esquinas.

| Dualidad: |          | por qué              | es central |                 |     |     |
| --------- | -------- | -------------------- | ---------- | --------------- | --- | --- |
| La        | dualidad | explica              | tres cosas | a la vez:       |     |     |
|           | por      | qué las relajaciones |            | entregan cotas; |     |     |
por qué aparecen multiplicadores interpretables como precios sombra;
|      | por       | qué en descomposición |     | surgen | cortes y certificados. |     |
| ---- | --------- | --------------------- | --- | ------ | ---------------------- | --- |
| Para | el primal | de minimización       |     |        |                        |     |
m´ın{c⊤x
|     |         |     |     | (P)      | : Ax ≤ | b, x ≥ 0}, |
| --- | ------- | --- | --- | -------- | ------ | ---------- |
| su  | dual es |     |     |          |        |            |
|     |         |     |     | m´ax{b⊤y | A⊤y    |            |
|     |         |     | (D) |          | : ≥    | c, y ≤ 0}. |
El signo de las restricciones en el primal determina el dominio de las variables duales.
11/39

Cómo interpretar el dual
Primal: decide valores de las variables para construir una solución factible.
Dual: asigna valores a las restricciones del primal, interpretables como precios sombra
o valores marginales de los recursos.
Si una restricción del primal es escasa o crítica, su multiplicador dual puede ser alto.
Si una restricción no influye en el óptimo, su multiplicador dual puede ser cero.
El dual entrega una cota y, además, una interpretación económica de la estructura
del problema.
12/39

| Dualidad | débil         | = principio      |             | de cota   |                    |     |
| -------- | ------------- | ---------------- | ----------- | --------- | ------------------ | --- |
| Dualidad |               | débil            |             |           |                    |     |
| Si       | x es primal   | factible         | y y es dual | factible, | entonces           |     |
|          |               |                  |             | b⊤y       | ≤ c⊤x.             |     |
| En       | un problema   | de minimización: |             |           |                    |     |
|          | toda solución | dual             | factible    | entrega   | una cota inferior; |     |
|          | toda solución | primal           | factible    | entrega   | una cota superior. |     |
|          |               |                  |             | b⊤y       | c⊤x.               |     |
|          |               |                  |             | ≤         | v(P) ≤             |     |
|          |               |                  | LB          |           | z⋆                 | UB  |
brecha primal–dual
13/39

Dualidad fuerte y complementariedad
Dualidad fuerte
Si uno de los problemas es factible y tiene óptimo finito, entonces ambos lo son y
v(P) = v(D).
Consecuencia computacional
|     | c⊤x⋆ = | b⊤y⋆ |     |
| --- | ------ | ---- | --- |
certifica optimalidad.
Complementariedad
| u = b−Ax | ≥ 0, | v = A⊤y−c | ≥ 0 |
| -------- | ---- | --------- | --- |
| y⋆u⋆     |      | x⋆v⋆      |     |
|          | = 0, | = 0.      |     |
|          | i i  | j j       |     |
Cada restricción activa en primal o dual deja su huella en el otro problema.
14/39

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
15/39

| Dos familias | para resolver   | PL  |                |                               |
| ------------ | --------------- | --- | -------------- | ----------------------------- |
| Simplex      |                 |     | Interior-Point |                               |
| Se mueve     | entre vértices. |     |                |                               |
|              |                 |     |                | Recorre el interior factible. |
Explota bases y costos reducidos. Resuelve sistemas KKT primal–dual.
Lectura combinatoria del poliedro. Lectura global y suave del poliedro.
|     | Característica |              | Simplex | Interior-Point |
| --- | -------------- | ------------ | ------- | -------------- |
|     | Recorre        | vértices     | Sí      | No             |
|     | Usa bases      | explícitas   | Sí      | No             |
|     | Usa KKT        | directamente | No      | Sí             |
|     | Muy útil       | en MILP      | Sí      | Indirectamente |
16/39

| Simplex: idea | geométrica |     |
| ------------- | ---------- | --- |
| En forma      | estándar:  |     |
x 2
camino simplex
m´ın c⊤x
|           | Ax=b,          | x≥0             |
| --------- | -------------- | --------------- |
| Idea del  | método simplex |                 |
| 1. partir | desde una      | solución básica |
factible
x
1
| 2. identificar | una dirección | que mejora el |
| -------------- | ------------- | ------------- |
objetivo
| 3. moverse   | a una base | adyacente     |
| ------------ | ---------- | ------------- |
| 4. detenerse | cuando     | no hay mejora |
17/39
| Geométricamente: | el algoritmo | recorre |
| ---------------- | ------------ | ------- |
| vértices del     | poliedro.    |         |

Métodos de puntos interiores: formulación primal–dual
Consideremos el problema primal
m´ınc⊤x s.a. Ax = b, x ≥ 0,
cuyo dual es
m´axb⊤y s.a. A⊤y+s = c, s ≥ 0.
Las condiciones KKT asociadas son
Ax = b, A⊤y+s = c, x s = 0 ∀i.
i i
Las dos primeras condiciones corresponden a factibilidad primal y dual.
La tercera expresa la complementariedad entre x y s.
18/39

| Métodos | de puntos | interiores: | idea | de barrera |     |
| ------- | --------- | ----------- | ---- | ---------- | --- |
La dificultad central está en la condición de complementariedad
|     |     |     | x   | s = 0 | ∀i, |
| --- | --- | --- | --- | ----- | --- |
i i
| ya que | en el óptimo | algunas            | componentes | deben     | anularse. |
| ------ | ------------ | ------------------ | ----------- | --------- | --------- |
| Los    | métodos de   | barrera reemplazan | esta        | condición | por       |
|        |              |                    | x i s i =   | µ,        | µ > 0,    |
lo que obliga a mantenerse en el interior de la región factible.
Al variar µ, las soluciones obtenidas describen la trayectoria central.
Cuando µ → 0, la trayectoria converge hacia una solución óptima.
En programación entera, estos métodos se usan principalmente para resolver relajaciones lineales o como parte
deesquemashíbridos. 19/39

| Trayectoria | central | y brecha primal–dual |             |           |            |
| ----------- | ------- | -------------------- | ----------- | --------- | ---------- |
|             |         |                      | Los métodos | de puntos | interiores |
x 2
|     |     |     | generan       | una secuencia | de puntos |
| --- | --- | --- | ------------- | ------------- | --------- |
|     |     |     | estrictamente | interiores.   |           |
óptimo
|     |     |     | Esa secuencia | sigue la         | trayectoria  |
| --- | --- | --- | ------------- | ---------------- | ------------ |
|     |     |     | central       | y converge hacia | una solución |
óptima.
|     |             |         | La brecha | primal–dual | se mide mediante |
| --- | ----------- | ------- | --------- | ----------- | ---------------- |
|     | trayectoria | central |           |             |                  |
x⊤s.
x
1
|     |     |     | Sobre la | trayectoria central | se cumple |
| --- | --- | --- | -------- | ------------------- | --------- |
x⊤s=nµ.
|     |     |     | Cuando | µ→0, la brecha | desaparece y |
| --- | --- | --- | ------ | -------------- | ------------ |
20/39
|     |     |     | se alcanza | optimalidad. |     |
| --- | --- | --- | ---------- | ------------ | --- |

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
21/39

| MILP y relajación | lineal        |              |     |
| ----------------- | ------------- | ------------ | --- |
| Un modelo         | lineal entero | mixto típico | es: |
c⊤x+d⊤y
m´ın
|     |     | s.a. | Ax+By ≥ b, |
| --- | --- | ---- | ---------- |
x ∈ Zp, y ∈ Rq, y ≥ 0.
Casos particulares:
| ILP:          | todas las variables | son | enteras. |
| ------------- | ------------------- | --- | -------- |
| BIP:          | variables binarias. |     |          |
| La relajación | lineal reemplaza    |     |          |
Zp Rp.
x ∈ −→ x ∈
En minimización:
22/39
v(LP) ≤ v(MILP).

| Brecha |           | de integridad | y fortaleza   |     | de formulación       |     |     |
| ------ | --------- | ------------- | ------------- | --- | -------------------- | --- | --- |
|        | Se define | la brecha     | de integridad |     | como                 |     |     |
|        |           |               |               | gap | = v(MILP)−v(LP) ≥ 0. |     |     |
x
2
|     | Brecha | pequeña | ⇒ formulación |     | fuerte. | conv(P ) |     |
| --- | ------ | ------- | ------------- | --- | ------- | -------- | --- |
I
|     | Brecha | grande            | ⇒ relajación   | débil.       |     |     | P   |
| --- | ------ | ----------------- | -------------- | ------------ | --- | --- | --- |
|     | La     | calidad           | del LP impacta | directamente |     |     |     |
|     | el     | Branch-and-Bound. |                |              |     |     |     |
x
1
23/39

| Variables | binarias:        |           | patrones   |            | canónicos     |                |     |
| --------- | ---------------- | --------- | ---------- | ---------- | ------------- | -------------- | --- |
| Las       | variables        | binarias  |            | permiten   | modelar:      |                |     |
|           | selección:       |           | elegir     | proyectos, | arcos,        | instalaciones; |     |
|           | cobertura:       |           | asegurar   | que        | algo quede    | atendido;      |     |
|           | empaquetamiento: |           |            | imponer    | exclusión     | mutua;         |     |
|           | lógica:          | activar,  | desactivar |            | o condicionar | restricciones. |     |
| Ejemplos  |                  | clásicos: |            |            |               |                |     |
(cid:88)
|     |     |     |     | w   | z ≤ W | (capacidad | / selección) |
| --- | --- | --- | --- | --- | ----- | ---------- | ------------ |
i i
i
(cid:88)
|     |     |     |     |     | z   | ≥ 1 (set | cover) |
| --- | --- | --- | --- | --- | --- | -------- | ------ |
i
i∈S(j)
(cid:88)
|     |     |     |     |     | z i ≤ | 1 (set | packing) |
| --- | --- | --- | --- | --- | ----- | ------ | -------- |
i∈S(j)
24/39

| Activación |                 | condicional      |              | y Big-M        |           |             |            |       |     |
| ---------- | --------------- | ---------------- | ------------ | -------------- | --------- | ----------- | ---------- | ----- | --- |
|            | Queremos        | modelar          | la           | implicación    |           |             |            |       |     |
|            |                 |                  |              | z              | = 1 ⇒     | a⊤x ≤ b,    | z ∈ {0,1}. |       |     |
|            | Una formulación |                  | Big-M        | estándar       | es        |             |            |       |     |
|            |                 |                  |              |                | a⊤x       | ≤ b+M(1−z). |            |       |     |
|            | Si z            | = 1, recuperamos |              | la restricción |           | original.   |            | z = 1 | ?   |
|            | Si z            | = 0, la          | restricción  | queda          | relajada. |             |            |       |     |
| Problema:  |                 | si M             | es demasiado |                | grande,   | la          |            | z = 0 |     |
?
| relajación |     | LP se      | vuelve | débil y | aparecen |     |     |     |     |
| ---------- | --- | ---------- | ------ | ------- | -------- | --- | --- | --- | --- |
| problemas  |     | numéricos. |        |         |          |     |     |     |     |
25/39

| Linealización | de productos | binarios          |     |
| ------------- | ------------ | ----------------- | --- |
| Caso 1:       | w = z z ,    | con z ,z ∈ {0,1}. |     |
|               | 1 2          | 1 2               |     |
w ≤ z ,
1
w ≤ z ,
2
w ≥ z +z −1,
1 2
w ∈ {0,1}.
| Caso 2: | w = zx, con | z ∈ {0,1}     | y x ∈ [ℓ,u].  |
| ------- | ----------- | ------------- | ------------- |
|         |             | w ≤ uz,       | w ≥ ℓz,       |
|         |             | w ≤ x−ℓ(1−z), | w ≥ x−u(1−z). |
La idea es siempre la misma: reemplazar no linealidad por una descripción lineal exacta
26/39
| del conjunto | factible. |     |     |
| ------------ | --------- | --- | --- |

| Formulaciones | fuertes | vs. débiles |     |
| ------------- | ------- | ----------- | --- |
Dosmodelospuedendescribirelmismoconjuntoenteroytenerdesempeñoscomputacio-
| nales totalmente | distintos. |     |     |
| ---------------- | ---------- | --- | --- |
| Formulación      | fuerte     |     |     |
Su relajación LP aproxima estrechamente al conjunto entero convexo.
| Efectos prácticos |                            |                   |            |
| ----------------- | -------------------------- | ----------------- | ---------- |
| mejores           | cotas inferiores,          |                   |            |
| menos             | nodos en Branch-and-Bound, |                   |            |
| tiempos           | de cómputo                 | menores.          |            |
| Buenas prácticas  |                            |                   |            |
| ajustar           | Big-M al mínimo            | válido,           |            |
| usar variables    | auxiliares                 | cuando fortalecen | el modelo, |
preferir reformulaciones extendidas si la relajación mejora significativamente. 27/39

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
28/39

| Cotas | inferiores, |     | superiores | y   | gap |     |     |
| ----- | ----------- | --- | ---------- | --- | --- | --- | --- |
En minimización:
LB: proviene de una relajación (LP, lagrangiana, descompuesta, etc.).
|         | UB: | proviene  | de  | una solución | factible | entera. |     |
| ------- | --- | --------- | --- | ------------ | -------- | ------- | --- |
| Siempre |     | se cumple |     |              |          |         |     |
z⋆
|     |          |     |           |           | LB      | ≤ ≤ UB. |     |
| --- | -------- | --- | --------- | --------- | ------- | ------- | --- |
| El  | objetivo | del | algoritmo | es cerrar | el gap: |         |     |
UB−LB
.
|UB|
gap global
|     |     |     |     | LB  |     | z⋆  | UB  |
| --- | --- | --- | --- | --- | --- | --- | --- |
29/39

| Certificados de | optimalidad |     |     |     |
| --------------- | ----------- | --- | --- | --- |
En PL
| una solución    | primal factible |              | da una cota | superior;         |
| --------------- | --------------- | ------------ | ----------- | ----------------- |
| una solución    | dual factible   | da           | una cota    | inferior;         |
| si ambas        | coinciden, hay  | optimalidad. |             |                   |
| En programación | entera          |              |             |                   |
| se necesita     | una solución    | entera       | con valor   | UB;               |
| y demostrar     | que toda        | relajación   | relevante   | tiene valor ≥ UB. |
Mensaje operativo
Resolver no es solo encontrar una buena solución: es también certificar que no existe
otra mejor.
30/39

| Arquitectura     | Branch-and-Bound |                      |               |
| ---------------- | ---------------- | -------------------- | ------------- |
| Branch-and-Bound | mantiene         | un árbol de          | subproblemas. |
| En cada nodo:    |                  |                      |               |
| se resuelve      | una relajación   | para obtener         | una LB local; |
| si aparece       | una solución     | entera, se actualiza | la UB global; |
| si LB            | ≥ UB             | , el nodo se poda.   |               |
nodo global
raízLB=12
|     |             | x3≤0LB=14 | x3≥1entero:UB=15 |
| --- | ----------- | --------- | ---------------- |
|     | LB=16podado | LB=14,5   |                  |
31/39

| Cómo leer | un árbol      | B&B           |              |           |
| --------- | ------------- | ------------- | ------------ | --------- |
| 1. La     | raíz resuelve | la relajación | del problema | original. |
2. Si la solución es fraccional, se elige una variable para ramificar.
3. Cada rama agrega restricciones nuevas y genera subproblemas.
4. El árbol termina cuando todos los nodos están podados o resueltos.
| Observación | clave |     |     |     |
| ----------- | ----- | --- | --- | --- |
La eficacia del B&B depende de dos cosas: buenas cotas y buenas soluciones
| factibles | tempranas. |     |     |     |
| --------- | ---------- | --- | --- | --- |
32/39

Heurísticas: por qué importan tanto
Las heurísticas no son un accesorio: son parte central de la arquitectura de resolución.
Objetivo principal
Encontrar rápido una buena solución factible ⇒ mejorar la UB.
Esquema genérico
1. construir una solución inicial;
2. mejorarla con búsqueda local;
3. actualizar la mejor UB conocida;
4. reiniciar o diversificar si conviene.
Una mejor UB implica más poda y menos árbol.
33/39

| Búsqueda local | y vecindarios |     |     |
| -------------- | ------------- | --- | --- |
Un vecindario N(x) define los movimientos elementales que pueden realizarse desde una
solución x.
| En minimización, | se busca | un vecino x′ | ∈ N(x) tal que |
| ---------------- | -------- | ------------ | -------------- |
|                  |          | f(x′)        | < f(x).        |
Si existe, la búsqueda avanza. Si no existe, x es un óptimo local para ese vecindario.
| Movimientos | típicos |     |     |
| ----------- | ------- | --- | --- |
intercambio,
inserción,
| activación | o desactivación | binaria, |     |
| ---------- | --------------- | -------- | --- |
| inversión  | o permutación.  |          |     |
34/39

| Estancamiento | en búsqueda | local |             |             |                 |     |
| ------------- | ----------- | ----- | ----------- | ----------- | --------------- | --- |
|               |             |       | La búsqueda | local puede | quedar atrapada | en  |
f(x)
|     |     |     | una solución | que es buena        | dentro de su |     |
| --- | --- | --- | ------------ | ------------------- | ------------ | --- |
|     |     |     | vecindario,  | pero no globalmente | óptima.      |     |
|     |     |     | Para escapar | del estancamiento   | se utilizan  |     |
|     |     |     | estrategias  | como:               |              |     |
óptimo local
reinicios,
|     | mejor solución |     | perturbaciones, |     |     |     |
| --- | -------------- | --- | --------------- | --- | --- | --- |
x
|     |     |     | vecindarios | variables,      |              |     |
| --- | --- | --- | ----------- | --------------- | ------------ | --- |
|     |     |     | memoria     | tabú.           |              |     |
|     |     |     | La idea es  | explorar nuevas | regiones del |     |
|     |     |     | espacio de  | soluciones.     |              |     |
35/39

Mapa del capítulo
| Introducción            | y estructura           |             |
| ----------------------- | ---------------------- | ----------- |
| Programación            | lineal: geometría      | y dualidad  |
| Cómo se resuelve        | un LP                  |             |
| Programación            | entera y formulaciones | binarias    |
| Cotas, Branch-and-Bound | y                      | heurísticas |
| Cierre del              | capítulo               |             |
36/39

Resumen conceptual
1. LP aporta geometría convexa, dualidad y certificados.
2. MILP introduce discreción, brecha de integridad y dificultad combinatoria.
3. La calidad de una formulación se mide por la fuerza de su relajación.
4. Los algoritmos exactos viven de cotas + buenas soluciones factibles.
5. Simplex, Interior-Point, B&B y heurísticas son piezas de una misma arquitectura.
37/39

| Qué queda     | preparado       | para los siguientes | capítulos |
| ------------- | --------------- | ------------------- | --------- |
| Este capítulo | deja instaladas | las bases para:     |           |
Relajación lagrangiana: relajar restricciones difíciles y optimizar la función dual.
Descomposición de Benders:separarvariablesmaestrasysubproblemasmediante
cortes.
Modelos extendidos y aproximaciones: capturar más realismo sin perder tracta-
bilidad.
| Idea final |     |     |     |
| ---------- | --- | --- | --- |
Entender la estructura del modelo es lo que permite elegir la estrategia
| computacional | correcta. |     |     |
| ------------- | --------- | --- | --- |
38/39

| Programación | lineal         | y entera      |
| ------------ | -------------- | ------------- |
| Capítulo     | 1: fundamentos | estructurales |
Pablo Torrealba
Marzo 2026
39/39