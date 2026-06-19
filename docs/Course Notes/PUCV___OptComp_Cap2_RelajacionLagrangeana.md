| Aplicación  | de metodos             | de optimización |
| ----------- | ---------------------- | --------------- |
| Capítulo 2: | relajación lagrangiana |                 |
Pablo Torrealba
Abril 2026
1/31

Mapa del capítulo
| Fundamentos    | de la relajación        | lagrangiana |
| -------------- | ----------------------- | ----------- |
| Descomposición | e interpretación        | económica   |
| Optimización   | del dual y recuperación | primal      |
2/31

Motivación
En muchos problemas de optimización, no todas las restricciones generan la misma di-
ficultad. Frecuentemente, el modelo contiene un conjunto de restricciones que acopla
decisiones que, sin ese acoplamiento, podrían tratarse de forma mucho más simple.
Ejemplos típicos
| restricciones | globales               | de capacidad; |                |
| ------------- | ---------------------- | ------------- | -------------- |
| restricciones | de cobertura           | exacta;       |                |
| balances      | de flujo o asignación; |               |                |
| relaciones    | de consistencia        | entre bloques | de decisiones. |
Idea central
La relajación lagrangiana busca separar la parte estructurada del problema y tratar las
restricciones complicantes mediante penalizaciones en la función objetivo.
3/31

Idea conceptual
Supongamos que el problema original puede verse como la combinación de dos partes:
| una estructura | interna | que sabemos explotar | bien; |     |
| -------------- | ------- | -------------------- | ----- | --- |
un conjunto de restricciones que conecta esa estructura y destruye su tratabilidad.
|     | estructura  | base     | restricciones | complicantes |
| --- | ----------- | -------- | ------------- | ------------ |
|     | subproblema | tratable | acoplamiento  | global       |
La relajación lagrangiana preserva la estructura base y traslada el efecto de las restric-
| ciones complicantes | al  | objetivo. |     |     |
| ------------------- | --- | --------- | --- | --- |
4/31

| Planteamiento | general     |      |                    |               |
| ------------- | ----------- | ---- | ------------------ | ------------- |
| Consideremos  | el problema | de   | minimización       |               |
|               | m´ın        | f(x) |                    |               |
|               | s.a.        | g(x) | ≤ 0 (restricciones | complicantes) |
|               |             | x ∈  | X (estructura      | mantenida).   |
Aquí:
X representa el conjunto que decidimos mantener explícitamente;
g(x) ≤ 0 corresponde a las restricciones que vamos a relajar.
La calidad de la relajación depende de qué restricciones se retiran y de cuánta estructura
| útil queda | en X. |     |     |     |
| ---------- | ----- | --- | --- | --- |
5/31

Función lagrangiana
Asociamos multiplicadores λ ≥ 0 a las restricciones relajadas y definimos
L(x,λ) = f(x)+λ⊤g(x), λ ≥ 0.
Interpretación
si g (x) > 0, la restricción i se viola y esa violación es penalizada;
i
si g (x) ≤ 0, no aparece castigo positivo en esa componente;
i
el vector λ actúa como un sistema de precios o penalizaciones.
La dificultad deja de estar en imponer directamente g(x) ≤ 0 y pasa a reflejarse en el
valor de los multiplicadores.
6/31

Problema lagrangiano
| Para un multiplicador | fijo λ, | definimos | el problema              | relajado  |
| --------------------- | ------- | --------- | ------------------------ | --------- |
|                       |         | (R )      | m´ın (cid:8) f(x)+λ⊤g(x) | (cid:9) . |
λ
x∈X
| Lectura de esta | relajación |     |     |     |
| --------------- | ---------- | --- | --- | --- |
las restricciones complicantes ya no se exigen explícitamente;
| la factibilidad | se controla | solo sobre | X;  |     |
| --------------- | ----------- | ---------- | --- | --- |
las violaciones de g(x) ≤ 0 quedan incorporadas en el objetivo.
7/31

| Función dual | lagrangiana |      |             |             |          |
| ------------ | ----------- | ---- | ----------- | ----------- | -------- |
| Definimos    | la función  | dual | lagrangiana | por         |          |
|              |             |      |             | (cid:8)     | (cid:9)  |
|              |             | θ(λ) | = m´ın      | f(x)+λ⊤g(x) | , λ ≥ 0. |
x∈X
Esta función asigna a cada vector de multiplicadores el mejor valor que puede obtenerse
| en el problema | relajado. |     |     |     |     |
| -------------- | --------- | --- | --- | --- | --- |
Interpretación
| fijamos    | precios | λ;          |          |                 |     |
| ---------- | ------- | ----------- | -------- | --------------- | --- |
| resolvemos | el      | subproblema |          | inducido;       |     |
| obtenemos  | un      | valor dual  | asociado | a esos precios. |     |
8/31

Dual lagrangiano
El siguiente paso consiste en elegir los multiplicadores que produzcan la mejor cota
posible:
(D) m´ax θ(λ).
λ≥0
Objetivo
Buscar el mejor vector de multiplicadores para obtener la mejor cota inferior del
problema original.
Lectura conceptual
el problema original elige x;
el dual lagrangiano elige cuánto penalizar cada restricción relajada.
9/31

| ¿Por qué | entrega una      | cota?       |           |             |
| -------- | ---------------- | ----------- | --------- | ----------- |
| Sea      | x factible para  | el problema | original. | Entonces    |
|          |                  |             |           | g(x) ≤ 0.   |
| Como     | λ ≥ 0, se cumple |             |           |             |
|          |                  |             |           | λ⊤g(x) ≤ 0. |
Por tanto,
|              |         |                | f(x)+λ⊤g(x) | ≤ f(x). |
| ------------ | ------- | -------------- | ----------- | ------- |
| Al minimizar | sobre x | ∈ X, obtenemos |             |         |
z⋆,
|     |     |     |     | θ(λ) ≤ |
| --- | --- | --- | --- | ------ |
z⋆
| donde | es el valor | óptimo | del problema | original. |
| ----- | ----------- | ------ | ------------ | --------- |
10/31

Mapa del capítulo
| Fundamentos    | de la relajación        | lagrangiana |
| -------------- | ----------------------- | ----------- |
| Descomposición | e interpretación        | económica   |
| Optimización   | del dual y recuperación | primal      |
11/31

| De la cota    | a la estructura |                  |                   |
| ------------- | --------------- | ---------------- | ----------------- |
| La relajación | lagrangiana     | es especialmente | atractiva cuando: |
al retirar ciertas restricciones, el problema se separa por bloques;
los subproblemas resultantes tienen algoritmos especializados;
el acoplamiento global es pequeño respecto del resto del modelo;
se necesitan buenas cotas inferiores para un esquema exacto o híbrido.
| Ejemplos | típicos |     |     |
| -------- | ------- | --- | --- |
problemas de asignación, localización, ruteo, scheduling, diseño de redes, cobertura y
partición.
La técnica es especialmente poderosa cuando el modelo original contiene una estructura
natural que queda oculta por unas pocas restricciones complicantes.
12/31

| Descomposición |     | inducida    |           |            |              |     |
| -------------- | --- | ----------- | --------- | ---------- | ------------ | --- |
| Supongamos     | que | el problema | tiene una | estructura | por bloques: |     |
K
(cid:88)
|     |     | f(x) | = f (x | ), X | = X ×···×X | ,   |
| --- | --- | ---- | ------ | ---- | ---------- | --- |
|     |     |      | k      | k    | 1          | K   |
k=1
y que el acoplamiento aparece mediante restricciones del tipo
K
(cid:88)
|     |     |     |     | g k (x k ) | ≤ b. |     |
| --- | --- | --- | --- | ---------- | ---- | --- |
k=1
La idea de la relajación lagrangiana es dualizar estas restricciones de acoplamiento para
| desacoplar | el problema | en  | subproblemas | más pequeños. |     |     |
| ---------- | ----------- | --- | ------------ | ------------- | --- | --- |
13/31

| Descomposición | inducida | por | la relajación |     |     |     |
| -------------- | -------- | --- | ------------- | --- | --- | --- |
Si relajamos las restricciones de acoplamiento con multiplicadores λ ≥ 0, obtenemos
|             |           |     | K         | (cid:32) | K        | (cid:33) |
| ----------- | --------- | --- | --------- | -------- | -------- | -------- |
|             |           |     | (cid:88)  |          | (cid:88) |          |
|             | L(x,λ)    | =   | f (x )+λ⊤ |          | g (x )−b | .        |
|             |           |     | k k       |          | k k      |          |
|             |           |     | k=1       |          | k=1      |          |
| Reordenando | términos: |     |           |          |          |          |
K
|     |        |     | (cid:88)(cid:0) |      |       | (cid:1) |
| --- | ------ | --- | --------------- | ---- | ----- | ------- |
|     | L(x,λ) | =   | −λ⊤b+           | f (x | )+λ⊤g | (x ) .  |
|     |        |     |                 | k    | k k   | k       |
k=1
Así, para un λ fijo, el problema se separa en K subproblemas independientes.
14/31

| Interpretación | económica | de los multiplicadores |
| -------------- | --------- | ---------------------- |
Los multiplicadores lagrangianos pueden interpretarse como precios sombra asociados
| a las restricciones | relajadas. |     |
| ------------------- | ---------- | --- |
Si una restricción es muy difícil de satisfacer, su multiplicador tiende a crecer.
Si una restricción tiene holgura, su multiplicador puede disminuir.
El sistema de multiplicadores refleja la escasez relativa de los recursos o del acopla-
miento.
15/31

| Ejemplo conceptual: | acoplamiento | entre dos     | bloques |
| ------------------- | ------------ | ------------- | ------- |
| Consideremos        | el problema  |               |         |
|                     |              | m´ın f (x )+f | (x )    |
|                     |              | 1 1           | 2 2     |
|                     |              | s.a. x +x ≥   | d,      |
|                     |              | 1 2           |         |
|                     |              | x ∈ X ,       | x ∈ X . |
|                     |              | 1 1           | 2 2     |
La dificultad no proviene necesariamente de X o X , sino de la restricción
1 2
|            |                   | x +x ≥   | d,  |
| ---------- | ----------------- | -------- | --- |
|            |                   | 1 2      |     |
| que obliga | a coordinar ambos | bloques. |     |
Escribiendo
|     |     | d−x −x | ≤ 0, |
| --- | --- | ------ | ---- |
1 2
podemos relajar esa restricción mediante un multiplicador λ ≥ 0.
16/31

| Descomposición |       | del ejemplo |        |            |     |         |     |     |
| -------------- | ----- | ----------- | ------ | ---------- | --- | ------- | --- | --- |
| La lagrangiana | queda | dada        | por    |            |     |         |     |     |
|                |       | L(x         | ,x ,λ) | = f (x )+f | (x  | )+λ(d−x | −x  | ).  |
|                |       | 1           | 2      | 1 1        | 2   | 2       | 1   | 2   |
Reordenando:
|     |     |        |       | (cid:0)  |      | (cid:1) | (cid:0)   | (cid:1) |
| --- | --- | ------ | ----- | -------- | ---- | ------- | --------- | ------- |
|     |     | L(x ,x | ,λ) = | λd+ f (x | )−λx | +       | f (x )−λx | .       |
|     |     | 1      | 2     | 1        | 1    | 1       | 2 2       | 2       |
Por tanto,
|     |      |       |       | (cid:0)   |     | (cid:1) | (cid:0)   | (cid:1) |
| --- | ---- | ----- | ----- | --------- | --- | ------- | --------- | ------- |
|     | θ(λ) | = λd+ | m´ın  | f (x )−λx |     | + m´ın  | f (x )−λx | .       |
|     |      |       |       | 1 1       | 1   |         | 2 2       | 2       |
|     |      |       | x1∈X1 |           |     | x2∈X2   |           |         |
17/31

Mapa del capítulo
| Fundamentos    | de la relajación        | lagrangiana |
| -------------- | ----------------------- | ----------- |
| Descomposición | e interpretación        | económica   |
| Optimización   | del dual y recuperación | primal      |
18/31

| El siguiente     | desafío     |       |               |                     |
| ---------------- | ----------- | ----- | ------------- | ------------------- |
| En las secciones | anteriores  | vimos | que:          |                     |
| la relajación    | lagrangiana |       | entrega cotas | inferiores válidas; |
y que, además, puede revelar estructura y permitir descomposición.
| Pero todavía | queda | una pregunta | central: |     |
| ------------ | ----- | ------------ | -------- | --- |
Pregunta
¿Cómo elegimos los multiplicadores λ para obtener la mejor cota posible?
| Eso nos lleva | al problema | dual | lagrangiano: |       |
| ------------- | ----------- | ---- | ------------ | ----- |
|               |             |      | m´ax         | θ(λ). |
λ≥0
19/31

| No diferenciabilidad | del              | dual |     |
| -------------------- | ---------------- | ---- | --- |
| La función           | dual lagrangiana |      |     |
(cid:8) (cid:9)
|     |     | θ(λ) = m´ın | f(x)+λ⊤g(x) |
| --- | --- | ----------- | ----------- |
x∈X
| es cóncava, | pero en general | no diferenciable. |     |
| ----------- | --------------- | ----------------- | --- |
La razón es que, al cambiar λ, puede cambiar de forma abrupta la solución óptima del
| problema      | lagrangiano. |             |                |
| ------------- | ------------ | ----------- | -------------- |
| Cada solución | x ∈ X induce | una función | afín           |
|               |              | ϕ (λ)       | = f(x)+λ⊤g(x). |
x
La función dual corresponde al mínimo puntual de todas ellas:
|     |     | θ(λ) | = m´ınϕ (λ). |
| --- | --- | ---- | ------------ |
x
x∈X
20/31

| Geometría | de la función | dual |     |     |
| --------- | ------------- | ---- | --- | --- |
θ(λ)
quiebre
λ
La función dual lagrangiana suele ser cóncava, por tramos afines y no suave. Por eso, en lugar
|     |     | de gradientes | clásicos, se usan | subgradientes. |
| --- | --- | ------------- | ----------------- | -------------- |
21/31

| Subgradiente | del dual |     |     |     |
| ------------ | -------- | --- | --- | --- |
Sea λ ≥ 0, y sea x(λ) una solución óptima del problema lagrangiano
|     |     |      | (cid:8)     | (cid:9) |
| --- | --- | ---- | ----------- | ------- |
|     |     | m´ın | f(x)+λ⊤g(x) | .       |
x∈X
Entonces
|                    |     |         | s(λ) = g(x(λ)) |     |
| ------------------ | --- | ------- | -------------- | --- |
| es un subgradiente | de  | θ en λ. |                |     |
Interpretación
| Si g (x(λ)) | > 0, la | restricción | i está violada. |     |
| ----------- | ------- | ----------- | --------------- | --- |
i
| Si g (x(λ)) | < 0, existe | holgura | en esa componente. |     |
| ----------- | ----------- | ------- | ------------------ | --- |
i
| Si g (x(λ)) | = 0, la | componente | está balanceada | localmente. |
| ----------- | ------- | ---------- | --------------- | ----------- |
i
El subgradiente mide, en cierto sentido, la dirección en que conviene ajustar los multipli-
22/31
cadores.

| Método del | subgradiente |     |     |
| ---------- | ------------ | --- | --- |
λk, xk.
Dado un vector resolvemos el problema lagrangiano y obtenemos una solución
Luego calculamos
|                  |            | sk = g(xk).     |           |
| ---------------- | ---------- | --------------- | --------- |
| La actualización | clásica es |                 |           |
|                  |            | λk+1 (cid:0) λk | sk(cid:1) |
|                  |            | = ΠRm           | +α ,      |
k
+
| donde ΠRm | denota la proyección | sobre el ortante | no negativo. |
| --------- | -------------------- | ---------------- | ------------ |
+
23/31

Visualización del update
λ
2
Si alguna componente de λ˜
queda negativa, se proyecta
sobre Rm.
+
λk
+α sk
k
λk+1
λ
1
λ˜
24/31

| Elección | del tamaño | de paso |     |     |
| -------- | ---------- | ------- | --- | --- |
El comportamiento del método depende fuertemente del tamaño de paso α .
k
| Opciones | habituales          |         |     |     |
| -------- | ------------------- | ------- | --- | --- |
|          | pasos decrecientes; |         |     |     |
|          | reglas adaptativas; |         |     |     |
|          | pasos tipo          | Polyak: |     |     |
UB−θ(λk)
|     |     | α = β | , 0 < | β < 2. |
| --- | --- | ----- | ----- | ------ |
k
∥sk∥2
| Aquí | UB representa | una cota superior | primal conocida. |     |
| ---- | ------------- | ----------------- | ---------------- | --- |
Tarea
| Definir | y comparar | formas de actualizar | los valores |     |
| ------- | ---------- | -------------------- | ----------- | --- |
25/31

| Esquema | general | del | método |     |
| ------- | ------- | --- | ------ | --- |
λ0
| 1.  | Inicializar | multiplicadores |     | ≥ 0. |
| --- | ----------- | --------------- | --- | ---- |
λk.
| 2.  | Resolver | el problema | lagrangiano | para |
| --- | -------- | ----------- | ----------- | ---- |
| 3.  | Obtener  | una cota    | inferior:   |      |
LBk = θ(λk).
| 4.  | Calcular | el subgradiente: |     |     |
| --- | -------- | ---------------- | --- | --- |
sk g(xk).
=
| 5.  | Actualizar | λk+1.    |             |             |
| --- | ---------- | -------- | ----------- | ----------- |
| 6.  | Guardar    | la mejor | cota dual   | encontrada. |
| 7.  | Repetir    | hasta    | criterio de | parada.     |
26/31

| La necesidad |     | de  | recuperación |     | primal |     |
| ------------ | --- | --- | ------------ | --- | ------ | --- |
La solución xk obtenida del problema lagrangiano suele ser óptima para la relajación,
| pero | no necesariamente |     | factible | para | el problema | original. |
| ---- | ----------------- | --- | -------- | ---- | ----------- | --------- |
Por eso, en la práctica se incorpora una etapa de recuperación primal:
|     |     |     |     |     | xk  | xfeas. |
| --- | --- | --- | --- | --- | --- | ------ |
−→
| Objetivos |           | de     | esta etapa    |                     |              |           |
| --------- | --------- | ------ | ------------- | ------------------- | ------------ | --------- |
|           | construir |        | una solución  | factible            | del problema | original; |
|           | obtener   | una    | cota superior | UB;                 |              |           |
|           | medir     | el gap | primal–dual;  |                     |              |           |
|           | apoyar    | la     | actualización | de multiplicadores. |              |           |
27/31

| Heurísticas | de  | recuperación | primal |
| ----------- | --- | ------------ | ------ |
Las heurísticas de recuperación primal pueden tomar varias formas.
| 1.  | Reparación            | directa    |                     |
| --- | --------------------- | ---------- | ------------------- |
|     | eliminar violaciones; |            |                     |
|     | reasignar             | recursos;  |                     |
|     | restaurar             | coberturas | o balances.         |
| 2.  | Construcción          | guiada     | por multiplicadores |
|     | usar λ como           | sistema    | de precios;         |
construir una solución factible a partir de costos ajustados.
28/31

| Heurísticas | de           | recuperación | primal       |     |
| ----------- | ------------ | ------------ | ------------ | --- |
| 3.          | Mejora local |              |              |     |
|             | partir desde | la solución  | lagrangiana; |     |
aplicar búsqueda local o metaheurísticas para restaurar factibilidad;
|     | mejorar | la calidad de | la solución | factible obtenida. |
| --- | ------- | ------------- | ----------- | ------------------ |
En general, estas estrategias buscan transformar una solución dualmente informada, pero
eventualmente infactible, en una solución primal factible de buena calidad.
29/31

| Cotas y gap | durante       | el algoritmo                |
| ----------- | ------------- | --------------------------- |
| Durante     | la ejecución, | mantenemos simultáneamente: |
una cota inferior dual, obtenida desde la relajación lagrangiana;
una cota superior primal, obtenida por recuperación o heurísticas.
| Así, en | minimización: |     |
| ------- | ------------- | --- |
z⋆
LB ≤ ≤ UB.
| Y el gap | puede medirse | como: |
| -------- | ------------- | ----- |
UB−LB
.
|UB|
30/31

Ventajas y limitaciones
| Ventajas         | Limitaciones   |                 |                          |
| ---------------- | -------------- | --------------- | ------------------------ |
| cotas inferiores | fuertes;       | dual no         | suave;                   |
| explotación      | de estructura; | ajuste delicado | de pasos;                |
| descomposición   | natural;       | soluciones      | duales no necesariamente |
factibles;
apoyo a heurísticas;
integración con métodos exactos. calidad dependiente de qué restriccio-
nes se relajan.
31/31