#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador estilo BIRCH (brief 10.1): puntos 2D en clusters gaussianos. Satisfacen
la desigualdad triangular (son euclidianos). N = M. Salida en Variante A (coords).

Uso: python gen_birch.py N p seed n_clusters salida.pmp
"""
import sys
import random
import math


def gen_birch(n, seed, n_clusters):
    rng = random.Random(seed)
    # centros en una grilla aproximada
    side = int(math.ceil(math.sqrt(n_clusters)))
    centers = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(n_clusters)]
    pts = []
    for k in range(n):
        cx, cy = centers[k % n_clusters]
        pts.append((cx + rng.gauss(0, 30), cy + rng.gauss(0, 30)))
    return pts


def write_pmp(pts, p, out, seed, nc):
    n = len(pts)
    with open(out, "w") as f:
        f.write(f"# BIRCH-like N={n} p={p} seed={seed} clusters={nc}\n")
        f.write(f"{n} {n} {p}\n")
        for i, (x, y) in enumerate(pts):
            f.write(f"{i} {x:.4f} {y:.4f}\n")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("uso: gen_birch.py N p seed n_clusters salida.pmp")
        sys.exit(1)
    n = int(sys.argv[1]); p = int(sys.argv[2]); seed = int(sys.argv[3]); nc = int(sys.argv[4])
    pts = gen_birch(n, seed, nc)
    write_pmp(pts, p, sys.argv[5], seed, nc)
    print(f"OK: BIRCH N={n} p={p} clusters={nc} -> {sys.argv[5]}")
