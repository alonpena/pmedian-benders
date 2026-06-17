# Formato de instancias

El repositorio usa un formato interno simple para instancias del pMP. Hay dos variantes; los parsers de OR-Library y TSP-Library convierten a una de estas.

## Variante A — Coordenadas (Euclidiana)

Para instancias geométricas (TSP-Library, BIRCH, toy). Los clientes y sitios comparten los mismos puntos (N = M), como en el paper.

```
# comentario opcional (líneas que empiezan con #)
N M p
id x y
...
```

- Primera línea de datos: `N` clientes, `M` sitios, `p` sitios a abrir.
- Luego `N` líneas con `id x y` (coordenadas 2D).
- Distancia: `d(i,j) = floor( sqrt( (xi-xj)^2 + (yi-yj)^2 ) )` (Euclidiana truncada hacia abajo, convención del paper).

## Variante B — Matriz de distancias (RW)

Para instancias no euclidianas / posiblemente asimétricas (RW).

```
# comentario opcional
N M p
MATRIX
d_11 d_12 ... d_1M
...
d_N1 d_N2 ... d_NM
```

- Tras la cabecera `N M p`, la palabra clave `MATRIX`.
- Luego `N` filas de `M` enteros: `d(i,j)`.
- Puede ser asimétrica (RW genera `d(i,j)` uniforme en `[1, N]`).

## Instancia toy (`instances/toy/toy1.pmp`)

4 puntos en un rectángulo, `p = 2`. Óptimo conocido a mano = **6**.

| Cliente | x | y |
|---------|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 3 |
| 2 | 4 | 0 |
| 3 | 4 | 3 |

Distancias (Euclidiana truncada): `d(0,1)=3, d(0,2)=4, d(0,3)=5, d(1,2)=5, d(1,3)=4, d(2,3)=3`.
Abrir {0,3}, {0,2} o {1,2} da costo total 6. Sirve para validar el evaluador (Etapa 2) y la separación (Etapa 4).
