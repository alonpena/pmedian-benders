#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prototipo Python+Gurobi de la descomposicion de Benders para el p-mediana (pMP).

Sirve como ORACULO de correctitud y referencia legible de los callbacks para la
implementacion en C. Replica el nucleo del paper de Duran-Mateluna, Ales &
Elloumi (2023). Numeros de ecuacion remiten a docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md.

Componentes:
  - parser de instancias (Variante A coords / Variante B matriz), ver docs/INSTANCE_FORMAT.md
  - distancia d(i,j) euclidiana truncada (floor) para coords
  - matriz S (sitios ordenados por cercania)         -> seccion 7.8
  - separacion O(NM): k̃_i (Alg.2), OPT(SP_i) ec.18, corte ec.20
  - modelo de referencia F3 (oraculo exacto)          -> seccion 4.3
  - fuerza bruta (oraculo para instancias chicas)     -> Etapa 2
  - Fase 1: maestro LP + loop de cortes + redondeo    -> seccion 9.1
  - Fase 2: branch-and-Benders-cut (lazy callback)    -> seccion 9.2

Uso:
    python pmp_benders.py <instancia.pmp> [--p P] [--mode phase1|full|f3|brute|all]
"""
import sys
import math
import argparse
import gurobipy as gp
from gurobipy import GRB

EPS = 1e-6


# --------------------------------------------------------------------------- #
# Instancia
# --------------------------------------------------------------------------- #
class Instance:
    """Almacena la instancia y entrega d(i,j) y la matriz S a demanda."""

    def __init__(self, N, M, p, coords=None, matrix=None):
        self.N = N            # numero de clientes
        self.M = M            # numero de sitios
        self.p = p            # sitios a abrir
        self.coords = coords  # lista de (x,y) si Variante A
        self.matrix = matrix  # matriz NxM si Variante B
        self._S = None        # matriz S (lazy)
        self._D = None        # distancias ordenadas por cliente (lazy)

    def dist(self, i, j):
        """d(i,j): euclidiana truncada (floor) para coords; entrada directa para matriz."""
        if self.matrix is not None:
            return self.matrix[i][j]
        xi, yi = self.coords[i]
        xj, yj = self.coords[j]
        return int(math.floor(math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)))

    def build_S(self):
        """Matriz S: para cada cliente, sitios ordenados por distancia creciente.
        Tambien guarda las distancias ordenadas. Costo O(NM log M). Seccion 7.8."""
        if self._S is not None:
            return
        self._S = []
        self._D = []
        for i in range(self.N):
            order = sorted(range(self.M), key=lambda j: self.dist(i, j))
            self._S.append(order)
            self._D.append([self.dist(i, j) for j in order])

    @property
    def S(self):
        self.build_S()
        return self._S

    @property
    def Dord(self):
        self.build_S()
        return self._D


def parse_instance(path, p_override=None):
    with open(path) as f:
        lines = [ln.rstrip("\n") for ln in f]
    data = [ln for ln in lines if ln.strip() and not ln.lstrip().startswith("#")]
    header = data[0].split()
    N, M, p = int(header[0]), int(header[1]), int(header[2])
    if p_override is not None:
        p = p_override
    rest = data[1:]
    if rest and rest[0].strip().upper() == "MATRIX":
        rows = rest[1:1 + N]
        matrix = [[int(v) for v in r.split()] for r in rows]
        return Instance(N, M, p, matrix=matrix)
    coords = [None] * N
    for idx, ln in enumerate(rest[:N]):
        parts = ln.split()
        cid = int(parts[0])
        x, y = float(parts[1]), float(parts[2])
        coords[cid] = (x, y)
    return Instance(N, M, p, coords=coords)


# --------------------------------------------------------------------------- #
# Separacion O(NM) — Algoritmos 1 y 2, ecuaciones 17-20
# --------------------------------------------------------------------------- #
def separate_client(inst, i, ybar):
    """Separacion para el cliente i dado ȳ (vector de tamano M, posibl. fraccionario).

    Devuelve (opt_i, cut) donde:
      opt_i = OPT(SP_i(ȳ))  (ec.18)
      cut   = (rhs, coef_dict)  representando  theta_i + sum_j coef_j y_j >= rhs  (ec.20)
              coef_dict vacio si k̃_i = 0.
    Implementa el Algoritmo 2 para k̃_i en O(M)."""
    S = inst.S[i]
    Dd = inst.Dord[i]
    M = inst.M

    # --- Algoritmo 2: calcular k̃_i ---
    k_tilde = 0
    r = 0                       # indice 0-based en S (r=1 en el pseudocodigo)
    val = 1.0 - ybar[S[0]]
    while val > EPS and r < M - 1:
        if Dd[r + 1] > Dd[r]:   # salto de radio (incremento estricto de distancia)
            k_tilde += 1
        r += 1
        val -= ybar[S[r]]

    # --- ec.18 y corte ec.20 ---
    if k_tilde == 0:
        # ya hay (fraccion de) sitio abierto en el radio minimo
        opt = float(Dd[0])
        return opt, (float(Dd[0]), {})

    # D^{k̃+1}_i = distancia del primer radio cubierto = Dd[r] (sitio S[r] donde val<=0)
    D_next = float(Dd[r])
    # sitios con d_ij <= D^{k̃}_i  <=>  d_ij < D_next (radios estrictamente menores)
    coef = {}
    acc = 0.0
    for t in range(r):          # S[0..r-1] tienen distancia < D_next
        j = S[t]
        c = D_next - Dd[t]      # (D^{k̃+1}_i - d_ij) >= 0
        coef[j] = c
        acc += c * ybar[j]
    opt = D_next - acc          # ec.18
    return opt, (D_next, coef)


def separate_all(inst, ybar, thetabar=None):
    """Algoritmo 1: separa todos los clientes. Devuelve (UB, cuts) donde UB = sum OPT(SP_i)
    y cuts = lista de (i, rhs, coef) de cortes violados (si thetabar dado)."""
    UB = 0.0
    cuts = []
    for i in range(inst.N):
        opt, (rhs, coef) = separate_client(inst, i, ybar)
        UB += opt
        if thetabar is not None and thetabar[i] < opt - 1e-6:
            cuts.append((i, rhs, coef))
    return UB, cuts


# --------------------------------------------------------------------------- #
# Oraculos: fuerza bruta y F3
# --------------------------------------------------------------------------- #
def eval_open_set(inst, open_sites):
    """Objetivo exacto dado un conjunto de sitios abiertos (suma de distancias minimas)."""
    total = 0
    for i in range(inst.N):
        total += min(inst.dist(i, j) for j in open_sites)
    return total


def brute_force(inst):
    """Enumera C(M,p) conjuntos. Solo para instancias chicas. Etapa 2 (oraculo)."""
    from itertools import combinations
    best, best_set = None, None
    for comb in combinations(range(inst.M), inst.p):
        v = eval_open_set(inst, comb)
        if best is None or v < best:
            best, best_set = v, comb
    return best, best_set


def solve_F3(inst, verbose=False):
    """Modelo de referencia F3 (ec.10-15). Oraculo exacto via Gurobi. Seccion 4.3."""
    inst.build_S()
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 1 if verbose else 0)
    env.start()
    m = gp.Model("F3", env=env)
    y = m.addVars(inst.M, vtype=GRB.BINARY, name="y")

    # radios distintos por cliente
    obj = gp.LinExpr()
    z = {}
    for i in range(inst.N):
        Dd = inst.Dord[i]
        S = inst.S[i]
        # construir radios distintos D^1<...<D^K y los sitios en cada radio
        radii = []
        sites_at = []
        kprev = None
        for t in range(inst.M):
            d = Dd[t]
            if d != kprev:
                radii.append(d)
                sites_at.append([S[t]])
                kprev = d
            else:
                sites_at[-1].append(S[t])
        K = len(radii)
        obj += radii[0]
        for k in range(K - 1):
            z[(i, k)] = m.addVar(lb=0.0, name=f"z_{i}_{k}")
            obj += (radii[k + 1] - radii[k]) * z[(i, k)]
        # ec.12: z^1 + sum_{d=D^1} y >= 1
        m.addConstr(z[(i, 0)] + gp.quicksum(y[j] for j in sites_at[0]) >= 1)
        # ec.13: z^k + sum_{d=D^k} y >= z^{k-1}
        for k in range(1, K - 1):
            m.addConstr(z[(i, k)] + gp.quicksum(y[j] for j in sites_at[k]) >= z[(i, k - 1)])
    m.addConstr(y.sum() == inst.p)
    m.setObjective(obj, GRB.MINIMIZE)
    m.optimize()
    open_sites = [j for j in range(inst.M) if y[j].X > 0.5]
    return m.ObjVal, sorted(open_sites)


# --------------------------------------------------------------------------- #
# Heuristica de redondeo (seccion 9.1)
# --------------------------------------------------------------------------- #
def rounding_heuristic(inst, ybar):
    """Abre los p sitios con mayor ȳ_j y evalua exacto. Devuelve (UB, open_sites)."""
    order = sorted(range(inst.M), key=lambda j: -ybar[j])
    open_sites = order[:inst.p]
    return eval_open_set(inst, open_sites), sorted(open_sites)


# --------------------------------------------------------------------------- #
# Fase 1 — maestro LP + loop de cortes + redondeo (Algoritmo 3, seccion 9.1)
# --------------------------------------------------------------------------- #
def phase1(inst, verbose=False, max_iter=10000):
    inst.build_S()
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    m = gp.Model("MP_LP", env=env)
    y = [m.addVar(lb=0.0, ub=1.0, name=f"y_{j}") for j in range(inst.M)]
    theta = [m.addVar(lb=0.0, name=f"theta_{i}") for i in range(inst.N)]
    m.addConstr(gp.quicksum(y) == inst.p)
    m.setObjective(gp.quicksum(theta), GRB.MINIMIZE)

    # arranque heuristico: y uniforme (greedy/aleatorio reemplaza a PopStar)
    ybar = [inst.p / inst.M] * inst.M
    UB1 = math.inf
    best_set = None
    LB1 = 0.0
    it = 0
    # cortes iniciales desde el arranque
    while it < max_iter:
        it += 1
        thetabar = [theta[i].X if m.SolCount > 0 else 0.0 for i in range(inst.N)] \
            if it > 1 else [0.0] * inst.N
        _, cuts = separate_all(inst, ybar, thetabar)
        # redondeo cada iteracion para bajar UB1
        ubr, setr = rounding_heuristic(inst, ybar)
        if ubr < UB1:
            UB1, best_set = ubr, setr
        if not cuts:
            break
        for (i, rhs, coef) in cuts:
            expr = theta[i] + gp.quicksum(c * y[j] for j, c in coef.items())
            m.addConstr(expr >= rhs)
        m.optimize()
        LB1 = m.ObjVal
        ybar = [y[j].X for j in range(inst.M)]
        if verbose:
            print(f"[F1] iter={it} LB1={LB1:.4f} UB1={UB1:.4f} cuts={len(cuts)}")
    return LB1, UB1, best_set, it


# --------------------------------------------------------------------------- #
# Fase 2 — branch-and-Benders-cut (lazy callback, seccion 9.2)
# --------------------------------------------------------------------------- #
def phase2(inst, verbose=False):
    inst.build_S()
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 1 if verbose else 0)
    env.start()
    m = gp.Model("MP_MIP", env=env)
    m.Params.LazyConstraints = 1
    m.Params.MIPGap = 1e-10
    y = [m.addVar(vtype=GRB.BINARY, name=f"y_{j}") for j in range(inst.M)]
    theta = [m.addVar(lb=0.0, name=f"theta_{i}") for i in range(inst.N)]
    m.addConstr(gp.quicksum(y) == inst.p)
    m.setObjective(gp.quicksum(theta), GRB.MINIMIZE)
    m._y = y
    m._theta = theta
    m._inst = inst
    m._ncuts = 0

    def cb(model, where):
        if where != GRB.Callback.MIPSOL:
            return
        yv = model.cbGetSolution(model._y)
        tv = model.cbGetSolution(model._theta)
        _, cuts = separate_all(model._inst, yv, tv)
        for (i, rhs, coef) in cuts:
            expr = model._theta[i] + gp.quicksum(c * model._y[j] for j, c in coef.items())
            model.cbLazy(expr >= rhs)
            model._ncuts += 1

    m.optimize(cb)
    open_sites = sorted(j for j in range(inst.M) if y[j].X > 0.5)
    return m.ObjVal, open_sites, m._ncuts, int(m.NodeCount)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Prototipo Benders pMP (oraculo).")
    ap.add_argument("instance")
    ap.add_argument("--p", type=int, default=None)
    ap.add_argument("--mode", default="all",
                    choices=["phase1", "full", "f3", "brute", "all"])
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    inst = parse_instance(args.instance, args.p)
    print(f"Instancia: N={inst.N} M={inst.M} p={inst.p}")

    if args.mode in ("brute", "all") and inst.M <= 20:
        bv, bs = brute_force(inst)
        print(f"[brute] opt={bv} set={bs}")
    if args.mode in ("f3", "all"):
        fv, fs = solve_F3(inst, args.verbose)
        print(f"[F3]    opt={fv:.1f} set={fs}")
    if args.mode in ("phase1", "all"):
        LB1, UB1, s1, it = phase1(inst, args.verbose)
        print(f"[F1]    LB1={LB1:.4f} UB1={UB1:.1f} set={s1} iter={it}")
    if args.mode in ("full", "all"):
        v2, s2, nc, nodes = phase2(inst, args.verbose)
        print(f"[F2]    opt={v2:.1f} set={s2} cuts={nc} nodes={nodes}")


if __name__ == "__main__":
    main()
