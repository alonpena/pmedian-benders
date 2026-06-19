#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-check del separador C contra el oraculo Python para un MISMO ȳ.

Corre `./pmedian <inst> --p P --dump-cuts <abiertos...>`, parsea cada corte por
cliente (constante + coeficientes), y los compara contra `separate_client` del
prototipo (prototype/pmp_benders.py) con el mismo ȳ. Comparaciones exactas.

Escribe:
  - results/logs/verify_cuts_toy.log          (salida cruda del binario C)
  - results/logs/verify_cuts_oracle_diff.log  (diffs C-vs-Python; vacio/zero = match)

Si CUALQUIER valor discrepa: imprime esperado-vs-real, escribe el diff y SALE != 0.
NO se altera ninguna formula para forzar coincidencia: una discrepancia = bug real.

Uso: python scripts/verify_cuts.py [instancia.pmp] [p] [sitio0 sitio1 ...]
     (default: instances/toy/toy1.pmp 2 0 1)
"""
import os
import re
import sys
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRB_LIB = "/Library/gurobi1200/macos_universal2/lib"
LOGDIR = os.path.join(ROOT, "results", "logs")

sys.path.insert(0, os.path.join(ROOT, "prototype"))
from pmp_benders import parse_instance, separate_client  # noqa: E402

LINE = re.compile(
    r"i=(\d+) ktilde=(\d+) opt=(\S+) cut: theta_\d+ >= (\S+)(.*)")
TERM = re.compile(r"- (\S+)\*y_(\d+)")


def run_c(inst, p, sites):
    env = dict(os.environ, DYLD_LIBRARY_PATH=GRB_LIB)
    cmd = [os.path.join(ROOT, "pmedian"), inst, "--p", str(p),
           "--dump-cuts"] + [str(s) for s in sites]
    out = subprocess.run(cmd, capture_output=True, text=True, env=env).stdout
    os.makedirs(LOGDIR, exist_ok=True)
    with open(os.path.join(LOGDIR, "verify_cuts_toy.log"), "w") as f:
        f.write(out)
    cuts = {}
    for ln in out.splitlines():
        m = LINE.match(ln.strip())
        if not m:
            continue
        i = int(m.group(1))
        kt = int(m.group(2))
        opt = float(m.group(3))
        const = float(m.group(4))
        coef = {int(s): float(c) for c, s in TERM.findall(m.group(5))}
        cuts[i] = {"ktilde": kt, "opt": opt, "const": const, "coef": coef}
    return cuts


def main():
    inst_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        ROOT, "instances", "toy", "toy1.pmp")
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    sites = [int(x) for x in sys.argv[3:]] or [0, 1]

    inst = parse_instance(inst_path, p)
    inst.build_S()
    ybar = [0.0] * inst.M
    for s in sites:
        ybar[s] = 1.0

    cuts_c = run_c(inst_path, p, sites)

    diffs = []
    for i in range(inst.N):
        opt_py, (const_py, coef_py) = separate_client(inst, i, ybar)
        c = cuts_c.get(i)
        if c is None:
            diffs.append(f"cliente {i}: C no emitio linea")
            continue
        # constante (opt y rhs coinciden en este separador)
        if abs(c["const"] - const_py) > 1e-9:
            diffs.append(f"cliente {i}: const C={c['const']} Py={const_py}")
        if abs(c["opt"] - opt_py) > 1e-9:
            diffs.append(f"cliente {i}: opt C={c['opt']} Py={opt_py}")
        # coeficientes (order-independent)
        keys = set(c["coef"]) | set(coef_py)
        for j in sorted(keys):
            cv = c["coef"].get(j, 0.0)
            pv = coef_py.get(j, 0.0)
            if abs(cv - pv) > 1e-9:
                diffs.append(f"cliente {i}: coef y_{j} C={cv} Py={pv}")

    os.makedirs(LOGDIR, exist_ok=True)
    diffpath = os.path.join(LOGDIR, "verify_cuts_oracle_diff.log")
    with open(diffpath, "w") as f:
        f.write(f"instancia={inst_path} p={p} abiertos={sites}\n")
        f.write(f"clientes comparados={inst.N}\n")
        if diffs:
            f.write("DIFERENCIAS (C vs Python):\n")
            for d in diffs:
                f.write("  " + d + "\n")
        else:
            f.write("diffs=0 (C ≡ Python en const y todos los coeficientes)\n")

    if diffs:
        print(f"MISMATCH: {len(diffs)} diferencias C-vs-Python")
        for d in diffs:
            print("  " + d)
        print(f"Ver {diffpath}")
        sys.exit(1)
    print(f"PASS: C ≡ Python para los {inst.N} clientes (0 diffs). "
          f"Logs en {LOGDIR}/verify_cuts_{{toy,oracle_diff}}.log")


if __name__ == "__main__":
    main()
