#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera 4 figuras de analisis (Etapa 8) SOLO desde CSVs reales (sin columnas NA ni
fabricadas):
  (a) results/plot_a_bounds_orlib.png : LB1 / UB1 / OPT por instancia OR-Library
  (b) results/plot_b_time_vs_N.png    : Ttot vs N (log-log)
  (c) results/plot_c_gap_vs_pM.png    : brecha Fase 1 (UB1-LB1)/UB1 vs p/M
  (d) results/plot_d_iter_nodes_vs_p.png : iter y nodes vs p

Fuentes:
  - results/orlib_optima_check.csv  (para (a): LB1,UB1,opt_proven,official)
  - results/benchmark.csv           (para (b),(c),(d): N,p,LB1,UB1,Ttot,iter,nodes)

Uso: python scripts/plot_results.py
"""
import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results")
BENCH = os.path.join(OUT, "benchmark.csv")
ORLIB = os.path.join(OUT, "orlib_optima_check.csv")


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def plot_a():
    rows = load_csv(ORLIB)
    rows = sorted(rows, key=lambda r: int(r["instance"].replace("pmed", "").replace(".pmp", "")))
    names = [r["instance"].replace(".pmp", "") for r in rows]
    lb1 = [float(r["our_LB1"]) for r in rows]
    ub1 = [float(r["our_UB1"]) for r in rows]
    opt = [float(r["our_opt_proven"]) for r in rows]
    x = range(len(names))
    plt.figure(figsize=(10, 4))
    plt.plot(x, lb1, "o-", label="LB1 (Fase 1)")
    plt.plot(x, ub1, "s-", label="UB1 (Fase 1)")
    plt.plot(x, opt, "x--", label="OPT (probado Fase 2)")
    plt.xticks(list(x), names, rotation=60, fontsize=7)
    plt.ylabel("Valor objetivo"); plt.title("Cotas LB1/UB1 y OPT por instancia OR-Library")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUT, "plot_a_bounds_orlib.png"), dpi=110, bbox_inches="tight")


def full_rows():
    return [r for r in load_csv(BENCH) if r["mode"] == "full"]


def plot_b():
    rows = full_rows()
    N = [int(r["N"]) for r in rows]
    Tt = [float(r["Ttot"]) for r in rows]
    plt.figure()
    plt.loglog(N, Tt, "o")
    plt.xlabel("N (clientes = sitios)"); plt.ylabel("Tiempo total [s]")
    plt.title("Tiempo total vs N (log-log)")
    plt.grid(True, which="both", alpha=0.3)
    plt.savefig(os.path.join(OUT, "plot_b_time_vs_N.png"), dpi=110, bbox_inches="tight")


def plot_c():
    rows = full_rows()
    pM = [int(r["p"]) / int(r["M"]) for r in rows]
    gap = []
    for r in rows:
        lb, ub = float(r["LB1"]), float(r["UB1"])
        gap.append(100.0 * (ub - lb) / ub if ub > 0 else 0.0)
    plt.figure()
    plt.scatter(pM, gap)
    plt.xlabel("p / M"); plt.ylabel("Brecha Fase 1 (UB1-LB1)/UB1 [%]")
    plt.title("Brecha de Fase 1 vs p/M")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUT, "plot_c_gap_vs_pM.png"), dpi=110, bbox_inches="tight")


def plot_d():
    rows = full_rows()
    p = [int(r["p"]) for r in rows]
    it = [int(r["iter"]) for r in rows]
    nodes = [float(r["nodes"]) for r in rows]
    fig, ax1 = plt.subplots()
    ax1.scatter(p, it, c="tab:blue", label="iter (Fase 1)")
    ax1.set_xlabel("p"); ax1.set_ylabel("iteraciones Fase 1", color="tab:blue")
    ax2 = ax1.twinx()
    ax2.scatter(p, nodes, c="tab:red", marker="^", label="nodes (Fase 2)")
    ax2.set_ylabel("nodos B&B (Fase 2)", color="tab:red")
    plt.title("Iteraciones y nodos vs p")
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, "plot_d_iter_nodes_vs_p.png"), dpi=110, bbox_inches="tight")


def main():
    plot_a(); plot_b(); plot_c(); plot_d()
    print("Figuras: plot_a_bounds_orlib, plot_b_time_vs_N, plot_c_gap_vs_pM, plot_d_iter_nodes_vs_p (.png en results/)")


if __name__ == "__main__":
    main()
