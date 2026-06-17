#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test unitario del parser OR-Library: regla de aristas duplicadas
(ultima-ocurrencia-gana, ver docs/ADR/0002). Usa una instancia HECHA A MANO con
respuesta CONOCIDA, independiente de pmed1/5819.

Instancia tests/data/dup_edge.orlib (1-based):
  4 nodos, p=1, aristas:  1-2=1, 2-3=1, 3-4=1, 1-2=10 (duplicada)
  Regla ultima-gana => c(1,2)=10. Regla minimo (incorrecta) => c(1,2)=1.

Caminos minimos (ultima-gana, c12=10):
  d(1,2)=10 d(1,3)=11 d(1,4)=12 d(2,3)=1 d(2,4)=2 d(3,4)=1
p-mediana p=1 (abrir 1 centro, sumar distancias):
  centro 2 o 3 => 13.   (con regla minimo seria 4 -> distinto)

Ejecutar:  python tests/test_parse_orlib.py     (exit 0 = PASS, 1 = FAIL)
"""
import os
import sys
import itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from parse_orlib import parse_orlib   # noqa: E402

INST = os.path.join(ROOT, "tests", "data", "dup_edge.orlib")

EXPECTED_D12 = 10           # ultima-gana
EXPECTED_PMEDIAN_P1 = 13    # con la regla correcta
WRONG_IF_MIN = 4            # lo que daria la regla minimo

fails = 0
def check(cond, msg):
    global fails
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fails += 1

def main():
    n, p, D = parse_orlib(INST)
    check(n == 4 and p == 1, f"cabecera n=4 p=1 (got n={n} p={p})")
    # D es 0-based: nodo 1 -> idx 0
    check(D[0][1] == EXPECTED_D12,
          f"c(1,2)=10 por ultima-ocurrencia-gana (got {D[0][1]}; min daria 1)")
    # APSP esperados
    check(D[0][2] == 11 and D[0][3] == 12 and D[1][3] == 2,
          f"caminos minimos consistentes (d13={D[0][2]} d14={D[0][3]} d24={D[1][3]})")
    # p-mediana p=1 por fuerza bruta
    best = min(sum(min(D[i][j] for j in comb) for i in range(n))
               for comb in itertools.combinations(range(n), p))
    check(best == EXPECTED_PMEDIAN_P1,
          f"p-mediana p=1 = 13 con regla correcta (got {best}; regla min daria {WRONG_IF_MIN})")
    check(best != WRONG_IF_MIN, "regla correcta NO coincide con la regla minimo (test discrimina)")

    print("\nRESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
