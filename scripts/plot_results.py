#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera figuras de analisis preliminar (Etapa 8) desde results/benchmark.csv:
  - results/plot_time_vs_N.png   : tiempo total vs tamano N
  - results/plot_gap1_vs_p.png   : brecha de Fase 1 (UB1-LB1)/UB1 vs p
  - results/plot_nodes_vs_p.png  : nodos del B&B vs p

Uso: python scripts/plot_results.py
"""
import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "results", "benchmark.csv")
OUT = os.path.join(ROOT, "results")


def load():
    rows = []
    with open(CSV) as f:
        for r in csv.DictReader(f):
            if r["mode"] != "full":
                continue
            rows.append(r)
    return rows


def main():
    rows = load()
    N = [int(r["N"]) for r in rows]
    p = [int(r["p"]) for r in rows]
    Ttot = [float(r["Ttot"]) for r in rows]
    nodes = [float(r["nodes"]) for r in rows]
    gap1 = []
    for r in rows:
        lb, ub = float(r["LB1"]), float(r["UB1"])
        gap1.append((ub - lb) / ub if ub > 0 else 0.0)

    plt.figure()
    plt.scatter(N, Ttot)
    plt.xlabel("N (clientes = sitios)"); plt.ylabel("Tiempo total [s]")
    plt.title("Tiempo total vs N (OR-Library pmed)")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUT, "plot_time_vs_N.png"), dpi=110, bbox_inches="tight")

    plt.figure()
    plt.scatter(p, [g * 100 for g in gap1])
    plt.xlabel("p (sitios abiertos)"); plt.ylabel("Brecha Fase 1 (UB1-LB1)/UB1 [%]")
    plt.title("Brecha de Fase 1 vs p")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUT, "plot_gap1_vs_p.png"), dpi=110, bbox_inches="tight")

    plt.figure()
    plt.scatter(p, nodes)
    plt.xlabel("p (sitios abiertos)"); plt.ylabel("Nodos B&B (Fase 2)")
    plt.title("Nodos del arbol vs p")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUT, "plot_nodes_vs_p.png"), dpi=110, bbox_inches="tight")

    print("Figuras escritas en results/: plot_time_vs_N.png, plot_gap1_vs_p.png, plot_nodes_vs_p.png")


if __name__ == "__main__":
    main()
