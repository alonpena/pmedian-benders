#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runner de benchmark: ejecuta ./pmedian sobre instancias OR-Library, agrega filas a
results/benchmark.csv (lo hace el binario) y produce results/orlib_optima_check.csv
comparando nuestro optimo probado contra el optimo OFICIAL de OR-Library
(pmedopt.txt).

NOTA de honestidad: OR-Library no corresponde a una tabla transcrita del paper en este
repo; la referencia local es el optimo oficial de Beasley. La comparacion contra la
Tabla 2 del paper (rl1304) vive en scripts/compare_paper.py y
results/comparison_vs_paper.csv. Zebra no se ejecuta aqui.

Uso:
  python scripts/run_benchmark.py            # corre el set por defecto
  python scripts/run_benchmark.py pmed1 pmed2 ...
"""
import os
import re
import sys
import csv
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORLIB = os.path.join(ROOT, "instances", "orlib")
RESULTS = os.path.join(ROOT, "results")
GRB_LIB = "/Library/gurobi1200/macos_universal2/lib"

# p por defecto de cada pmed (OR-Library): pmed1..5 p=5,10,10,20,33 ... usamos los
# que vienen en el header del archivo (no hardcodear): el binario toma el p del .pmp.

DEFAULT_SET = [f"pmed{i}" for i in range(1, 16)]


def load_official_opt():
    opt = {}
    path = os.path.join(ORLIB, "pmedopt.txt")
    if not os.path.exists(path):
        return opt
    with open(path) as f:
        for ln in f:
            m = re.match(r"\s*(pmed\d+)\s+(\d+)", ln)
            if m:
                opt[m.group(1)] = int(m.group(2))
    return opt


def ensure_pmp(name, official):
    """Convierte pmedN.txt -> pmedN.pmp si hace falta. Devuelve ruta .pmp."""
    txt = os.path.join(ORLIB, name + ".txt")
    pmp = os.path.join(ORLIB, name + ".pmp")
    if not os.path.exists(pmp) and os.path.exists(txt):
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "parse_orlib.py"), txt, pmp],
                       check=True)
    return pmp


def run_one(name, official):
    pmp = ensure_pmp(name, official)
    if not os.path.exists(pmp):
        print(f"  [skip] {name}: no .pmp ni .txt")
        return None
    opt = official.get(name)
    cmd = [os.path.join(ROOT, "pmedian"), pmp, "--mode", "full"]
    if opt is not None:
        cmd += ["--opt", str(opt)]
    env = dict(os.environ, DYLD_LIBRARY_PATH=GRB_LIB)
    out = subprocess.run(cmd, capture_output=True, text=True, env=env).stdout
    f1 = re.search(r"\[Fase 1\] LB1=([\d.]+) UB1=([\d.]+) iter=(\d+) cuts=(\d+) T1=([\d.]+)", out)
    f2 = re.search(r"\[Fase 2\] opt=([\d.]+) cuts=(\d+) nodes=([\d.]+) T2=([\d.]+)", out)
    if not f2:
        print(f"  [warn] {name}: sin salida Fase 2\n{out}")
        return None
    row = {
        "instance": name,
        "LB1": float(f1.group(1)), "UB1": float(f1.group(2)),
        "iter": int(f1.group(3)), "T1": float(f1.group(5)),
        "our_opt": float(f2.group(1)), "nodes": float(f2.group(3)), "T2": float(f2.group(4)),
        "official_opt": opt,
    }
    row["delta"] = (row["our_opt"] - opt) if opt is not None else None
    status = "OPT_MATCH" if opt is not None and abs(row["our_opt"] - opt) < 0.5 else "CHECK"
    row["status"] = status
    print(f"  {name}: our_opt={row['our_opt']:.0f} official={opt} delta={row['delta']} [{status}]")
    return row


def main():
    names = sys.argv[1:] or DEFAULT_SET
    official = load_official_opt()
    os.makedirs(RESULTS, exist_ok=True)
    rows = []
    for n in names:
        r = run_one(n, official)
        if r:
            rows.append(r)
    comp = os.path.join(RESULTS, "orlib_optima_check.csv")
    with open(comp, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instance", "our_LB1", "our_UB1", "our_opt_proven", "our_iter",
                    "our_nodes", "our_T1_s", "our_T2_s", "orlib_official_opt", "delta",
                    "status", "note"])
        for r in rows:
            w.writerow([r["instance"], r["LB1"], r["UB1"], r["our_opt"], r["iter"],
                        f"{r['nodes']:.0f}", r["T1"], r["T2"], r["official_opt"], r["delta"],
                        r["status"],
                        "ref = optimo oficial OR-Library (pmedopt.txt); NO es tabla del paper"])
    print(f"\nEscrito {comp} ({len(rows)} filas)")


if __name__ == "__main__":
    main()
