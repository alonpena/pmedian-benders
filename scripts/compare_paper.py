#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparacion contra el paper (Tabla 2 — small TSP). Los valores del paper se
TRANSCRIBEN del PDF docs/Benders_decom_pMedian.pdf (texto extraido, trazable; no
inventados). Se corre nuestro solver sobre las MISMAS instancias TSPLIB y se comparan:
  - OPT (optimo probado): comparacion VALIDA (delta debe ser 0).
  - gap final: VALIDA.
  - tiempos (T1, Ttot): se reportan pero se marcan MACHINE_DEPENDENT
    (paper: Intel XEON W-2145 + CPLEX 20.1; nosotros: Apple M1 + Gurobi 12.0.0).
  - iter / nodes: dependen de init heuristic (PopStar vs uniforme) y solver -> informativos.

Distancia: euclidiana FLOORED (verificado: rl1304 p=5 floor => 3,099,073 = OPT del paper).

Escribe results/comparison_vs_paper.csv. Solo instancias presentes en el PDF.

Uso: python scripts/compare_paper.py
"""
import os
import re
import csv
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSP = os.path.join(ROOT, "instances", "tsplib")
GRB_LIB = "/Library/gurobi1200/macos_universal2/lib"

# --- Tabla 2 del paper (rl1304), transcrita del PDF. ---
# columnas: p, OPT, paper_LB1, paper_UB1, paper_T1, paper_iter, paper_nodes, paper_Ttot
# (filas sin TL; rl1304 se resuelve a optimalidad en todas)
TABLE2_RL1304 = [
    (5,   3099073, 3099073, 3099073, 2.70,  9,   0,   2.8),
    (10,  2134295, 2131788, 2134295, 2.90, 12, 160,  15.4),
    (20,  1412108, 1412108, 1412108, 2.25,  8,   0,   2.3),
    (50,   795012,  795012,  795012, 1.46,  9,   0,   1.5),
    (100,  491639,  491507,  491788, 0.90, 19,  37,   2.4),
    (200,  268573,  268573,  268573, 0.35, 11,   0,   0.5),
    (300,  177326,  177318,  177339, 0.31, 12,   0,   0.5),
    (400,  128332,  128332,  128332, 0.23, 10,   0,   0.2),
    (500,   97024,   97018,   97034, 0.27, 14,   0,   0.4),
]
INSTANCE = "rl1304"


def run_ours(p, opt):
    pmp = os.path.join(TSP, f"{INSTANCE}_p{p}.pmp")
    if not os.path.exists(pmp):
        subprocess.run(["python3", os.path.join(ROOT, "scripts", "parse_tsplib.py"),
                        os.path.join(TSP, f"{INSTANCE}.tsp"), str(p), pmp], check=True)
    env = dict(os.environ, DYLD_LIBRARY_PATH=GRB_LIB)
    out = subprocess.run([os.path.join(ROOT, "pmedian"), pmp, "--mode", "full", "--opt", str(opt)],
                         capture_output=True, text=True, env=env).stdout
    f1 = re.search(r"\[Fase 1\] LB1=([\d.]+) UB1=([\d.]+) iter=(\d+) cuts=\d+ T1=([\d.]+)", out)
    f2 = re.search(r"\[Fase 2\] opt=([\d.]+) cuts=\d+ nodes=([\d.]+) T2=([\d.]+)", out)
    cb = re.search(r"nodos_B&B=(\d+)", out)
    return {
        "LB1": float(f1.group(1)), "UB1": float(f1.group(2)), "iter": int(f1.group(3)),
        "T1": float(f1.group(4)), "opt": float(f2.group(1)),
        "nodes": int(cb.group(1)) if cb else int(float(f2.group(2))),
        "T2": float(f2.group(3)),
    }


def main():
    rows = []
    for (p, OPT, pLB1, pUB1, pT1, pit, pnd, pTt) in TABLE2_RL1304:
        r = run_ours(p, OPT)
        Ttot = r["T1"] + r["T2"]
        delta_opt = r["opt"] - OPT
        opt_valid = "OK" if abs(delta_opt) < 0.5 else "MISMATCH"
        rows.append({
            "instance": INSTANCE, "N": 1304, "p": p,
            "paper_OPT": OPT, "our_opt_proven": int(r["opt"]), "delta_OPT": int(delta_opt),
            "opt_comparison": opt_valid,
            "paper_LB1": pLB1, "our_LB1": int(r["LB1"]),
            "paper_UB1": pUB1, "our_UB1": int(r["UB1"]),
            "paper_iter": pit, "our_iter": r["iter"],
            "paper_nodes": pnd, "our_nodes": r["nodes"],
            "paper_Ttot_s": pTt, "our_Ttot_s": round(Ttot, 2),
            "time_note": "MACHINE_DEPENDENT (paper XEON W-2145/CPLEX20.1; us M1/Gurobi12)",
        })
        print(f"  {INSTANCE} p={p}: our_opt={int(r['opt'])} paper_OPT={OPT} delta={int(delta_opt)} [{opt_valid}]")

    out = os.path.join(ROOT, "results", "comparison_vs_paper.csv")
    cols = ["instance", "N", "p", "paper_OPT", "our_opt_proven", "delta_OPT", "opt_comparison",
            "paper_LB1", "our_LB1", "paper_UB1", "our_UB1",
            "paper_iter", "our_iter", "paper_nodes", "our_nodes",
            "paper_Ttot_s", "our_Ttot_s", "time_note"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    n_ok = sum(1 for r in rows if r["opt_comparison"] == "OK")
    print(f"\n{n_ok}/{len(rows)} OPT coinciden con el paper. Escrito {out}")


if __name__ == "__main__":
    main()
