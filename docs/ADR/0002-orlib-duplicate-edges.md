# ADR 0002 — Aristas duplicadas en OR-Library: última-ocurrencia-gana

**Estado:** aceptado (2026-06-17).

## Contexto
Los archivos `pmed*` de OR-Library son grafos; la matriz de asignación se obtiene
con Floyd (todos-a-todos). Algunas instancias contienen **aristas paralelas con
costo distinto** (p. ej. `pmed1`: `{19,20}=[22,30]`, `{30,70}=[5,74]`). Tomar el
**mínimo** (lo natural para caminos mínimos) producía óptimo 5718; el óptimo oficial
de `pmedopt.txt` es **5819**. Había que fijar la regla de desempate.

## Justificación independiente (no circular respecto a 5819)
La regla **NO** se eligió "porque da 5819". Está **documentada por el propio autor de
OR-Library** (J.E. Beasley) en la página de formato `pmedinfo.html`, guardada en
`docs/orlib_pmed_format_spec.txt`. Cita textual:

> Read each edge line in the data file IN TURN:
>    if the three numbers in the line are i,j,k then
>    set c(i,j)=k and c(j,i)=k
> Then subject the matrix c to Floyd's algorithm [...].
> **The effect of this is that in the event of edge (i,j) having different costs
> in the data file only the last such cost is used.**

Es decir: leer aristas **en orden** sobrescribiendo `c(i,j)` ⇒ **gana la última
ocurrencia**. Beasley añade que esta aclaración surgió (2/May/95) por una consulta del
Prof. Avella (Univ. Salerno) justamente sobre la ambigüedad de las aristas múltiples.

Refuerzo secundario (de-facto): construir el grafo con `networkx.add_edge(u,v,weight=c)`
repetido también sobrescribe (última gana), por lo que las implementaciones de
referencia que usan ese patrón coinciden con la regla.

## Decisión
`scripts/parse_orlib.py` lee las aristas en orden y **sobrescribe** `D[u][v]=D[v][u]=c`
(sin `min`). Luego aplica Floyd-Warshall.

## Consecuencias
- (+) Regla derivada del **spec oficial**, no del valor objetivo. Reproduce 5819 como
  consecuencia, no como criterio.
- (+) Test independiente: `tests/test_parse_orlib.py` usa una instancia hecha a mano
  (`tests/data/dup_edge.orlib`) con respuesta conocida (p-mediana = 13 con última-gana,
  4 con mínimo) — verifica la regla **sin** depender de pmed1.
- (−) Si alguna instancia tuviera la intención contraria, fallaría; pero el spec es
  explícito, así que se asume válido para toda la familia pmed.

## Honestidad
La regla es justificable **independientemente** del objetivo 5819: proviene del texto
del mantenedor de OR-Library. No es una racionalización a posteriori.
