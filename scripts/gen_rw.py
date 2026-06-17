#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de instancias RW (Resende & Werneck, 2004): matriz de distancias
aleatoria, entera, uniforme en [1, n], posiblemente asimetrica. Brief 10.1.
N = M. Diagonal = 0.

Uso: python gen_rw.py N p seed salida.pmp [--symmetric]
"""
import sys
import random


def gen_rw(n, p, seed, symmetric=False):
    rng = random.Random(seed)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                D[i][j] = 0
            elif symmetric and j < i:
                D[i][j] = D[j][i]
            else:
                D[i][j] = rng.randint(1, n)
    return D


def write_pmp(n, p, D, out, symmetric):
    with open(out, "w") as f:
        f.write(f"# RW aleatoria N={n} p={p} {'simetrica' if symmetric else 'asimetrica'}\n")
        f.write(f"{n} {n} {p}\n")
        f.write("MATRIX\n")
        for i in range(n):
            f.write(" ".join(str(D[i][j]) for j in range(n)) + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("uso: gen_rw.py N p seed salida.pmp [--symmetric]")
        sys.exit(1)
    n = int(sys.argv[1]); p = int(sys.argv[2]); seed = int(sys.argv[3]); out = sys.argv[4]
    sym = "--symmetric" in sys.argv[5:]
    D = gen_rw(n, p, seed, sym)
    write_pmp(n, p, D, out, sym)
    print(f"OK: RW N={n} p={p} seed={seed} sym={sym} -> {out}")
