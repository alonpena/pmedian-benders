#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser OR-Library (Beasley, 1990) pmed -> formato interno Variante B (matriz).

Formato OR-Library pmed:
  linea 1:  n  m  p     (n nodos, m aristas, p medianas)
  m lineas: u v cost    (arista no dirigida con costo)
Las distancias d(i,j) son los caminos minimos de todos-a-todos (Floyd-Warshall).
Clientes = sitios = nodos (N = M = n).

Uso:  python parse_orlib.py instances/orlib/pmed1.txt instances/orlib/pmed1.pmp
"""
import sys

INF = float("inf")


def parse_orlib(path):
    with open(path) as f:
        toks = f.read().split()
    it = iter(toks)
    n = int(next(it)); m = int(next(it)); p = int(next(it))
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    for _ in range(m):
        u = int(next(it)) - 1   # OR-Library es 1-based
        v = int(next(it)) - 1
        c = int(next(it))
        # Convencion OR-Library: si una arista aparece repetida, la ULTIMA
        # ocurrencia es la valida (overwrite). En pmed1 esto reproduce el
        # optimo oficial 5819 (usar el minimo daria 5718, incorrecto).
        D[u][v] = c
        D[v][u] = c
    # Floyd-Warshall: O(n^3)
    for k in range(n):
        Dk = D[k]
        for i in range(n):
            dik = D[i][k]
            if dik == INF:
                continue
            Di = D[i]
            for j in range(n):
                nd = dik + Dk[j]
                if nd < Di[j]:
                    Di[j] = nd
    return n, p, D


def write_pmp(n, p, D, out_path):
    with open(out_path, "w") as f:
        f.write(f"# OR-Library pmed convertida a Variante B (matriz de caminos minimos)\n")
        f.write(f"{n} {n} {p}\n")
        f.write("MATRIX\n")
        for i in range(n):
            f.write(" ".join(str(int(D[i][j])) for j in range(n)) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("uso: parse_orlib.py <entrada_orlib> <salida.pmp>")
        sys.exit(1)
    n, p, D = parse_orlib(sys.argv[1])
    write_pmp(n, p, D, sys.argv[2])
    print(f"OK: n={n} p={p} -> {sys.argv[2]}")
