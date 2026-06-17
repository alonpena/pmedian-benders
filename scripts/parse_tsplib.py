#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser TSP-Library (Reinelt, 1991) EUC_2D -> formato interno Variante A (coords).
Clientes = sitios = nodos (N = M = DIMENSION). El p se pasa por argumento.

La distancia la calcula el nucleo como euclidiana TRUNCADA (floor), convencion del
paper (brief 10.1). Nota: TSPLIB canonico usa redondeo al entero mas cercano; aqui
mantenemos floor para ser consistentes con el resto del proyecto.

Uso: python parse_tsplib.py entrada.tsp p salida.pmp
"""
import sys


def parse_tsplib(path):
    coords = []
    in_section = False
    dim = None
    with open(path) as f:
        for ln in f:
            s = ln.strip()
            if s.upper().startswith("DIMENSION"):
                dim = int(s.split(":")[-1].strip())
            elif s.upper().startswith("NODE_COORD_SECTION"):
                in_section = True
            elif s in ("EOF", "") and in_section:
                if s == "EOF":
                    break
            elif in_section:
                parts = s.split()
                if len(parts) >= 3:
                    coords.append((float(parts[1]), float(parts[2])))
    return coords


def write_pmp(coords, p, out):
    n = len(coords)
    with open(out, "w") as f:
        f.write(f"# TSP-Library convertida a Variante A (coords). N=M={n} p={p}\n")
        f.write(f"{n} {n} {p}\n")
        for i, (x, y) in enumerate(coords):
            f.write(f"{i} {x:g} {y:g}\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("uso: parse_tsplib.py <entrada.tsp> <p> <salida.pmp>")
        sys.exit(1)
    coords = parse_tsplib(sys.argv[1])
    p = int(sys.argv[2])
    write_pmp(coords, p, sys.argv[3])
    print(f"OK: N=M={len(coords)} p={p} -> {sys.argv[3]}")
