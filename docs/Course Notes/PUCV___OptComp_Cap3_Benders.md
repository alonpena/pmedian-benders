| Aplicación | de métodos        | de optimización |
| ---------- | ----------------- | --------------- |
| Capítulo   | 3: Descomposición | de Benders      |
Pablo Torrealba
Abril 2026
1/30

Mapa del capítulo
Motivación y estructura
Subproblema y reformulación
Cortes de Benders
Algoritmo
Comentarios y extensiones
2/30

| ¿Cuándo | tiene | sentido | usar | Benders? |     |     |
| ------- | ----- | ------- | ---- | -------- | --- | --- |
Benders es especialmente útil cuando el modelo contiene dos niveles de decisión bien
diferenciados:
un bloque pequeño de decisiones estructurales o complicantes (x);
|     | un bloque     | grande | de decisiones |       | operacionales | (y); |
| --- | ------------- | ------ | ------------- | ----- | ------------- | ---- |
|     | restricciones | que    | acoplan       | ambos | bloques.      |      |
Al fijar las variables x, el problema residual en y se convierte en un LP (?) tratable.
| Benders | explota | esa | separabilidad |     | de forma iterativa. |     |
| ------- | ------- | --- | ------------- | --- | ------------------- | --- |
3/30

| ¿Qué         | tipo           | de estructura | busca           | explotar?    |              |
| ------------ | -------------- | ------------- | --------------- | ------------ | ------------ |
| Típicamente, |                | Benders       | aparece cuando: |              |              |
|              | las decisiones | en x          | son discretas,  | estratégicas | o de diseño; |
las decisiones en y son continuas y más fáciles de optimizar;
al fijar x, el problema residual en y se transforma en un LP tratable.
Benders no reduce la dificultad teórica del problema. La traslada a una interacción
iterativa entre un problema maestro y uno o varios subproblemas.
4/30

| Aplicaciones  | típicas           |                |                     |
| ------------- | ----------------- | -------------- | ------------------- |
| Este esquema  | aparece           | con frecuencia | en:                 |
| localización  | de instalaciones; |                |                     |
| diseño        | y expansión       | de redes;      |                     |
| planificación | energética;       |                |                     |
| problemas     | estocásticos      | de dos         | etapas;             |
| modelos       | con decisiones    | binarias       | y flujos continuos. |
Nota
En todos estos casos la estructura común es la misma: unas pocas decisiones maestras
determinan el contexto en el que se resuelve un problema operacional mucho más
grande.
5/30

| Interacción | entre    | maestro y subproblema |     |     |     |
| ----------- | -------- | --------------------- | --- | --- | --- |
|             | Problema | maestro               |     |     |     |
Subproblema
decide x
|     |          |     | fija | x = x¯ |     |
| --- | -------- | --- | ---- | ------ | --- |
|     | optimiza | η   |      |        |     |
x¯
|     | (aproximación    | de los      | evalúa  | factibilidad | y    |
| --- | ---------------- | ----------- | ------- | ------------ | ---- |
|     | costos globales) |             | costo   |              |      |
|     | considera        | un conjunto | obtiene | información  | dual |
de cortes
Infactible
|     |     |     | rayo extremo | ⇒ corte | de factibilidad |
| --- | --- | --- | ------------ | ------- | --------------- |
Factible
|     |     |     | dual óptimo | ⇒ corte | de optimalidad |
| --- | --- | --- | ----------- | ------- | -------------- |
6/30

| ¿Qué puede | devolver | el subproblema? |
| ---------- | -------- | --------------- |
Para una solución candidata x¯, el subproblema produce uno de dos tipos de información:
Si es factible y acotado: entrega un valor óptimo y una solución dual extrema.
| ⇒   | genera un | corte de optimalidad. |
| --- | --------- | --------------------- |
Si es infactible: entrega un certificado dual de infactibilidad (rayo extremo).
| ⇒   | genera un | corte de factibilidad. |
| --- | --------- | ---------------------- |
En ambos casos, el subproblema aporta información que restringe o mejora el problema
| maestro | en la siguiente | iteración. |
| ------- | --------------- | ---------- |
7/30

| Recordatorio: |     | puntos | extremos |     | y rayos extremos |     |
| ------------- | --- | ------ | -------- | --- | ---------------- | --- |
Sea
|     |          |               |          | Π                | = {π ≥ 0 :   | B⊤π ≤ d} |
| --- | -------- | ------------- | -------- | ---------------- | ------------ | -------- |
| el  | conjunto | factible      | del dual | del subproblema. |              |          |
|     | Un       | punto extremo | es un    | vértice          | del poliedro | Π.       |
En Benders, los cortes de optimalidad se asocian a puntos extremos.
|     | Un  | rayo extremo | es una | dirección | no acotada | de Π. |
| --- | --- | ------------ | ------ | --------- | ---------- | ----- |
En Benders, los cortes de factibilidad se asocian a rayos extremos.
Nota
El conjunto Π tiene un número finito de puntos extremos y rayos extremos. Esto
garantiza que el algoritmo de Benders termina en un número finito de iteraciones.
8/30

| Recordatorio: | ¿qué es              | un rayo?    |                   |
| ------------- | -------------------- | ----------- | ----------------- |
| Un rayo       | es una semirrecta    | de la forma |                   |
|               |                      | π(t) =      | π¯ +td, t ≥ 0,    |
| donde π¯      | es un punto factible | y d ̸= 0    | es una dirección. |
Si π¯ +td ∈ Π para todo t ≥ 0, entonces Π es no acotado en la dirección d.
Un rayo extremo es una dirección extrema del conjunto: una dirección de borde que
no puede escribirse como combinación de otras direcciones factibles.
Si el dual es no acotado, un rayo extremo entrega el certificado que permite construir
| un corte | de factibilidad. |     |     |
| -------- | ---------------- | --- | --- |
9/30

| Recordatorio: | puntos extremos    | y rayos extremos |              |            |
| ------------- | ------------------ | ---------------- | ------------ | ---------- |
| Caso          | 1: dual con óptimo | finito           | Caso 2: dual | no acotado |
| π             |                    |                  | π 2          |            |
2
mejora
mejora
Π
rayoextremo
|     | Π   | óptimo |     |     |
| --- | --- | ------ | --- | --- |
π 1
π
1
puntoextremoπ⋆
⇒cortedeoptimalidad
|     |     |     | rayoextremoπˆ | ⇒cortedefactibilidad |
| --- | --- | --- | ------------- | -------------------- |
10/30

Forma canónica
| Consideremos | el problema |     |     |
| ------------ | ----------- | --- | --- |
c⊤x+d⊤y
m´ın
|               |                    | s.a.             | Ax+By ≥ b,  |
| ------------- | ------------------ | ---------------- | ----------- |
|               |                    |                  | x ∈ X ⊆ Zp, |
|               |                    |                  | y ≥ 0.      |
| x: decisiones | estratégicas,      | usualmente       | discretas;  |
| y: decisiones | operacionales,     | usualmente       | continuas;  |
| Ax+By         | ≥ b: restricciones | de acoplamiento. |             |
11/30

| Lectura | de la | forma canónica |     |
| ------- | ----- | -------------- | --- |
La dificultad no proviene solo de que x sea entero, sino del acoplamiento entre x e y.
| ¿Como      | podemos | lidiar con    | que x sea entero? |
| ---------- | ------- | ------------- | ----------------- |
| Si fijamos | x =     | x¯, el modelo | se reduce a:      |
m´ın d⊤y
s.a. By ≥ b−Ax¯,
y ≥ 0.
Para un x¯ fijo, el problema en y es un LP paramétrico en el lado derecho, lo que nos
permite escribir los cortes en función del dual de este problema.
12/30

Mapa del capítulo
Motivación y estructura
Subproblema y reformulación
Cortes de Benders
Algoritmo
Comentarios y extensiones
13/30

Subproblema para x¯ fijo
Para una solución candidata x¯, resolvemos el subproblema primal:
(SP ) m´ın d⊤y
x¯
s.a. By ≥ b−Ax¯,
y ≥ 0.
Su dual es:
(DSP ) m´ax π⊤(b−Ax¯)
x¯
s.a. B⊤π ≤ d,
π ≥ 0.
Notar que:
El conjunto factible dual Π = {π ≥ 0 : B⊤π ≤ d} no depende de x¯. Solo el objetivo
dual cambia con cada candidato x¯.
14/30

| Reformulación | implícita  |             |        |             |
| ------------- | ---------- | ----------- | ------ | ----------- |
| Definimos     | la función | de recurso: |        |             |
|               |            | θ(x) = m´ın | {d⊤y : | By ≥ b−Ax}. |
y≥0
| El problema | original | se reescribe de | forma equivalente | como: |
| ----------- | -------- | --------------- | ----------------- | ----- |
m´ın c⊤x+θ(x).
x∈X
Si bien θ(x) no se conoce explícitamente, es convexa en x (máximo de funciones
lineales). Esto garantiza que los cortes lineales que la aproximan son válidos
globalmente.
En el maestro, η reemplaza a θ(x) como cota inferior del costo operacional:
|     |     | m´ın | c⊤x+η, | η ≥ θ(x). |
| --- | --- | ---- | ------ | --------- |
15/30
x∈X,η

Mapa del capítulo
Motivación y estructura
Subproblema y reformulación
Cortes de Benders
Algoritmo
Comentarios y extensiones
16/30

Corte de optimalidad
Si el subproblema es factible y acotado, por dualidad fuerte existe π⋆ óptimo dual tal
que:
|     |     | θ(x¯) | = π⋆⊤(b−Ax¯). |     |
| --- | --- | ----- | ------------- | --- |
Como π⋆ es factible en Π para cualquier x¯, se cumple para todo x ∈ X:
|     |     | θ(x) | ≥ π⋆⊤(b−Ax). |     |
| --- | --- | ---- | ------------ | --- |
Se agrega al maestro el corte (aproximamos θ con un hiperplano de soporte):
π⋆⊤(b−Ax)
η ≥
| η aproxima    | θ(x) desde | abajo         | con hiperplanos | de soporte;    |
| ------------- | ---------- | ------------- | --------------- | -------------- |
| cada corte    | es válido  | globalmente   | en X,           | no solo en x¯; |
| la envolvente | inferior   | de los cortes | converge        | a θ(x).        |
17/30

Lectura geométrica: corte de optimalidad
θ(x), η
θ(x)
x
Actividad rápida: indicar como se aproima la función con inecuaciones lineales.
18/30

Corte de factibilidad
Si el subproblema es infactible, el dual (DSP ) es no acotado: existe un rayo extremo
x¯
| πˆ ∈ Π tal | que: |     |     |
| ---------- | ---- | --- | --- |
πˆ⊤(b−Ax¯) > 0.
Para que cualquier x ∈ X sea compatible con el subproblema, necesariamente:
πˆ⊤(b−Ax) ≤ 0.
| Se agrega | al maestro | el corte: |     |
| --------- | ---------- | --------- | --- |
πˆ⊤(b−Ax) ≤ 0
| no involucra | a η: | es una restricción pura | sobre x; |
| ------------ | ---- | ----------------------- | -------- |
elimina del maestro todas las decisiones incompatibles con la operación;
como Π tiene finitos rayos extremos, solo pueden generarse finitos cortes de este
19/30
tipo.

Lectura geométrica: corte de factibilidad
θ(x)
X
x¯1 infact. x¯2 infact. x
1πˆ
etroc
2πˆ
etroc
eliminada
factible
De manera esquemática en una dimensión, un corte de factibilidad elimina valores de x
que vuelven infactible el subproblema. En general, este corte es una restricción lineal en
x, no necesariamente una frontera vertical. 20/30

Problema maestro acumulando cortes
Después de generar cortes de optimalidad O y de factibilidad F, el maestro es:
(MPk) m´ın c⊤x+η
s.a. η ≥ π⊤(b−Ax), ∀π ∈ O,
πˆ⊤(b−Ax) ≤ 0, ∀πˆ ∈ F,
x ∈ X.
MPk es una relajación del problema original: toda solución factible del original
satisface todos los cortes, pero no al revés. Con más cortes, el maestro entrega cotas
inferiores cada vez más ajustadas.
21/30

Mapa del capítulo
Motivación y estructura
Subproblema y reformulación
Cortes de Benders
Algoritmo
Comentarios y extensiones
22/30

| Algoritmo | clásico | de Benders |
| --------- | ------- | ---------- |
DescomposiciónclásicadeBenders
|     | 1: O←∅, F | ←∅, LB←−∞, UB←+∞ |
| --- | --------- | ---------------- |
2: repeat
|     | ResolverMPk | yobtener(x¯k,η¯k) |
| --- | ----------- | ----------------- |
3:
4: LB←c⊤x¯k+η¯k
5: ResolverSP
x¯k
|     | if SP | esinfactiblethen |
| --- | ----- | ---------------- |
6: x¯k
7: Obtenerunrayoextremoπˆ
8: AgregarcortedefactibilidadaF
else
9:
Obtenerunasolucióndualóptimaπ⋆
10:
11: AgregarcortedeoptimalidadaO
|     | 12: UB←m´ın{UB, | c⊤x¯k+θ(x¯k)} |
| --- | --------------- | ------------- |
13: endif
14: untilUB−LB≤ε
15: returnmejorsoluciónencontrada
23/30

| Cómo leer las | cotas |     |     |
| ------------- | ----- | --- | --- |
El problema maestro entrega una cota inferior (LB): usa una aproximación de θ(x),
| por lo que | subestima el costo | verdadero. |     |
| ---------- | ------------------ | ---------- | --- |
El subproblema factible entrega una cota superior (UB): evalúa el costo real para
| una solución | x¯k concreta. |     |     |
| ------------ | ------------- | --- | --- |
gap
|     | LB  | z⋆  | UB  |
| --- | --- | --- | --- |
Los cortes de optimalidad suben el LB. Las soluciones factibles del subproblema bajan el
| UB. El algoritmo | termina cuando | el gap cierra. |     |
| ---------------- | -------------- | -------------- | --- |
Tarea: que pasa si no cierra? que pasa cuando el problema ya no es continuo.
24/30

Mapa del capítulo
Motivación y estructura
Subproblema y reformulación
Cortes de Benders
Algoritmo
Comentarios y extensiones
25/30

| ¿Por | qué Benders | puede | funcionar | bien? |
| ---- | ----------- | ----- | --------- | ----- |
Benders suele ser atractivo cuando se cumplen una o más de estas condiciones:
el número de variables binarias maestras es relativamente pequeño;
el subproblema continuo tiene estructura especial que lo hace rápido de resolver
|     | (red, flujo, | LP con | pocas restricciones); |     |
| --- | ------------ | ------ | --------------------- | --- |
el modelo monolítico tiene una relajación LP débil o genera árboles de B&B muy
grandes;
existen estructuras repetitivas o escenarios separables que permiten resolver muchos
|      | subproblemas | en paralelo. |     |     |
| ---- | ------------ | ------------ | --- | --- |
|      | No tengo     | otra opción  | (?) |     |
| Pero | no siempre   | se gana      |     |     |
Si el maestro queda muy débil o los cortes son poco informativos, el método puede
| requerir | muchas | iteraciones | antes de | cerrar el gap. |
| -------- | ------ | ----------- | -------- | -------------- |
26/30

| Aceleraciones | habituales    |               |
| ------------- | ------------- | ------------- |
| Mejoras       | en la calidad | de los cortes |
Multicuts: agregar varios cortes por iteración en lugar de uno agregado.
Cortes fortalecidos: explotar la estructura o la integralidad de x.
27/30

| Aceleraciones | habituales    |             |
| ------------- | ------------- | ----------- |
| Mejoras       | en la gestión | del maestro |
Warm starts: iniciar con una solución o conjunto de cortes de buena calidad.
Stabilization: evitar oscilaciones fuertes entre iteraciones.
Branch-and-Benders-cut: integrar cortes dentro del árbol de branch-and-bound.
28/30

Extensiones importantes
Benders lógico: el subproblema no necesita ser un LP; basta con que entregue
| explicaciones | o inferencias | válidas**. |
| ------------- | ------------- | ---------- |
Benders estocástico (L-shaped): cada escenario genera un subproblema indepen-
| diente y | los cortes se agregan | al maestro. |
| -------- | --------------------- | ----------- |
29/30

| Aplicación | de métodos        | de optimización |
| ---------- | ----------------- | --------------- |
| Capítulo   | 3: Descomposición | de Benders      |
Pablo Torrealba
Abril 2026
30/30