#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""User-friendly benchmark pipeline for pmedian-benders.

No YAML required. Built-in case sets:
  smoke   : toy1, pmed1, kroA100
  current : toy1, OR-Library pmed1-15, kroA100, rl1304 paper p-grid
  orlib   : OR-Library pmed1-15
  rl1304  : TSPLIB rl1304 paper p-grid
  kro     : kroA100

Commands:
  list      show cases
  sources   show where official/raw instances come from
  prepare   create .pmp files from raw inputs when possible
  run       run ./pmedian with external timeout, logs, clean CSV (no benchmark.csv append)
  validate  run scripts/validate_results.py for curated/current evidence

This script runs ./pmedian from a temporary working directory so src/main.c writes
its append-only results/benchmark.csv into temp, not into repo results/benchmark.csv.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
PMEDIAN = ROOT / "pmedian"
RESULTS = ROOT / "results"
DEFAULT_LOG_DIR = RESULTS / "logs" / "paperbench"
DEFAULT_OUT = RESULTS / "curated" / "paperbench_current.csv"
NA = "NA"

RL1304_OPT = {
    5: 3099073,
    10: 2134295,
    20: 1412108,
    50: 795012,
    100: 491639,
    200: 268573,
    300: 177326,
    400: 128332,
    500: 97024,
}

@dataclass(frozen=True)
class Case:
    run_id: str
    family: str
    instance: Path
    raw: Optional[Path] = None
    parser: str = "none"          # none|orlib|tsplib|generated
    p: Optional[int] = None
    opt: Optional[float] = None
    provenance: str = "local"
    caveat: str = ""


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def load_orlib_optima() -> dict[str, float]:
    out: dict[str, float] = {}
    path = ROOT / "instances" / "orlib" / "pmedopt.txt"
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        m = re.match(r"\s*(pmed\d+)\s+(\d+)", line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


def all_cases() -> dict[str, Case]:
    opt = load_orlib_optima()
    cases: dict[str, Case] = {}
    cases["toy1"] = Case(
        "toy1", "toy", ROOT / "instances" / "toy" / "toy1.pmp",
        p=2, opt=6, provenance="hand-built toy instance in repo",
    )
    for i in range(1, 16):
        name = f"pmed{i}"
        cases[name] = Case(
            name, "OR-Library", ROOT / "instances" / "orlib" / f"{name}.pmp",
            raw=ROOT / "instances" / "orlib" / f"{name}.txt",
            parser="orlib", opt=opt.get(name),
            provenance="OR-Library Beasley pmed data; official optima in instances/orlib/pmedopt.txt",
        )
    cases["kroA100"] = Case(
        "kroA100", "TSPLIB", ROOT / "instances" / "tsplib" / "kroA100.pmp",
        raw=ROOT / "instances" / "tsplib" / "kroA100.tsp", parser="tsplib", p=10,
        provenance="TSPLIB kroA100 raw .tsp in repo; used as geometry sanity check",
        caveat="not a main paper-table result",
    )
    for p, optv in RL1304_OPT.items():
        run_id = f"rl1304_p{p}"
        cases[run_id] = Case(
            run_id, "TSPLIB", ROOT / "instances" / "tsplib" / f"rl1304_p{p}.pmp",
            raw=ROOT / "instances" / "tsplib" / "rl1304.tsp", parser="tsplib", p=p, opt=float(optv),
            provenance="TSPLIB rl1304 raw .tsp in repo; paper Table 2 values transcribed in scripts/compare_paper.py",
        )
    rw12 = ROOT / "instances" / "orlib" / "rw12.pmp"
    if rw12.exists():
        cases["rw12"] = Case(
            "rw12", "RW", rw12, parser="generated", p=3,
            provenance="small generated RW sanity-check instance committed in repo",
            caveat="not paper RW campaign",
        )
    return cases


def select_cases(set_name: str, only: list[str]) -> list[Case]:
    cases = all_cases()
    if only:
        missing = [x for x in only if x not in cases]
        if missing:
            raise SystemExit(f"Unknown case(s): {', '.join(missing)}")
        return [cases[x] for x in only]
    if set_name == "smoke":
        ids = ["toy1", "pmed1", "kroA100"]
    elif set_name == "orlib":
        ids = [f"pmed{i}" for i in range(1, 16)]
    elif set_name == "rl1304":
        ids = [f"rl1304_p{p}" for p in RL1304_OPT]
    elif set_name == "kro":
        ids = ["kroA100"]
    elif set_name == "current":
        ids = ["toy1"] + [f"pmed{i}" for i in range(1, 16)] + ["kroA100"] + [f"rl1304_p{p}" for p in RL1304_OPT]
    else:
        raise SystemExit(f"Unknown set: {set_name}")
    return [cases[i] for i in ids if i in cases]


def read_header(path: Path) -> tuple[str, str, str]:
    if not path.exists():
        return NA, NA, NA
    for line in path.read_text().splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            parts = s.split()
            if len(parts) >= 3:
                return parts[0], parts[1], parts[2]
            return NA, NA, NA
    return NA, NA, NA


def cmd_str(parts: list[str]) -> str:
    return " ".join(shlex.quote(x) for x in parts)


def prepare_case(case: Case) -> str:
    if case.instance.exists():
        return "exists"
    if case.parser == "orlib" and case.raw and case.raw.exists():
        case.instance.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "parse_orlib.py"), str(case.raw), str(case.instance)], check=True)
        return "created"
    if case.parser == "tsplib" and case.raw and case.raw.exists() and case.p is not None:
        case.instance.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "parse_tsplib.py"), str(case.raw), str(case.p), str(case.instance)], check=True)
        return "created"
    return "missing_raw_or_unsupported"


def parse_solver_output(text: str) -> dict[str, str]:
    d = {k: NA for k in ["LB1", "UB1", "T1", "iter", "cuts_phase1", "obj", "T2", "nodes", "lazy_cuts", "separation_calls", "warm_cuts"]}
    m = re.search(r"\[Fase 1\]\s+LB1=([\d.+\-eE]+)\s+UB1=([\d.+\-eE]+)\s+iter=(\d+)\s+cuts=(\d+)\s+T1=([\d.+\-eE]+)", text)
    if m:
        d.update({"LB1": m.group(1), "UB1": m.group(2), "iter": m.group(3), "cuts_phase1": m.group(4), "T1": m.group(5)})
    m = re.search(r"\[Fase 2\]\s+opt=([\d.+\-eE]+)\s+cuts=(\d+)\s+nodes=([\d.+\-eE]+)\s+T2=([\d.+\-eE]+)", text)
    if m:
        d.update({"obj": m.group(1), "lazy_cuts": m.group(2), "nodes": m.group(3), "T2": m.group(4)})
    m = re.search(r"warm_cuts=(\d+)\s+separaciones\(MIPSOL\)=(\d+)\s+cortes_lazy=(\d+)\s+nodos_B&B=([\d.+\-eE]+)", text)
    if m:
        d.update({"warm_cuts": m.group(1), "separation_calls": m.group(2), "lazy_cuts": m.group(3), "nodes": m.group(4)})
    return d


def run_case(case: Case, timeout: int, log_dir: Path) -> dict[str, str]:
    n, m, p = read_header(case.instance)
    row = {
        "run_id": case.run_id, "family": case.family, "instance": rel(case.instance),
        "N": n, "M": m, "p": p, "status": "NOT_RUN", "timeout_s": str(timeout),
        "opt_known": NA if case.opt is None else str(int(case.opt)), "delta_opt": NA,
        "matches_known_opt": NA, "log_path": NA, "provenance": case.provenance, "caveat": case.caveat,
    }
    row.update({k: NA for k in ["LB1", "UB1", "T1", "iter", "cuts_phase1", "obj", "T2", "nodes", "lazy_cuts", "separation_calls", "warm_cuts", "elapsed_s"]})
    if not case.instance.exists():
        row["status"] = "MISSING_INSTANCE"
        return row
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{case.run_id}.log"
    cmd = [str(PMEDIAN), str(case.instance), "--mode", "full"]
    if case.opt is not None:
        cmd += ["--opt", str(int(case.opt))]
    env = os.environ.copy()
    if not env.get("DYLD_LIBRARY_PATH"):
        lib = sorted(Path("/Library").glob("gurobi*/macos_universal2/lib"))
        if lib:
            env["DYLD_LIBRARY_PATH"] = str(lib[-1])
    start = time.time()
    try:
        with tempfile.TemporaryDirectory(prefix="paperbench_") as tmp:
            proc = subprocess.run(cmd, cwd=tmp, env=env, text=True, capture_output=True, timeout=timeout)
        elapsed = time.time() - start
        text = "COMMAND: " + cmd_str(["./pmedian", rel(case.instance), "--mode", "full"] + (["--opt", str(int(case.opt))] if case.opt is not None else [])) + "\n"
        text += f"RETURN_CODE: {proc.returncode}\nELAPSED_S: {elapsed:.3f}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n"
        log_path.write_text(text)
        row["elapsed_s"] = f"{elapsed:.3f}"
        row["log_path"] = rel(log_path)
        row.update(parse_solver_output(proc.stdout))
        row["status"] = "OK" if proc.returncode == 0 else "ERROR"
        if case.opt is not None and row.get("obj", NA) != NA:
            delta = float(row["obj"]) - float(case.opt)
            row["delta_opt"] = f"{delta:.6f}"
            row["matches_known_opt"] = "YES" if abs(delta) < 0.5 else "NO"
    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start
        log_path.write_text(f"COMMAND: {cmd_str(cmd)}\nTIMEOUT_AFTER_S: {timeout}\nELAPSED_S: {elapsed:.3f}\nSTDOUT:\n{e.stdout or ''}\nSTDERR:\n{e.stderr or ''}\n")
        row["status"] = "TIMEOUT"
        row["elapsed_s"] = f"{elapsed:.3f}"
        row["log_path"] = rel(log_path)
    return row


def write_csv(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["run_id", "family", "instance", "N", "M", "p", "status", "timeout_s", "obj", "opt_known", "delta_opt", "matches_known_opt", "LB1", "UB1", "T1", "T2", "elapsed_s", "iter", "cuts_phase1", "warm_cuts", "lazy_cuts", "separation_calls", "nodes", "log_path", "provenance", "caveat"]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, NA) for c in cols})


def main() -> int:
    ap = argparse.ArgumentParser(description="User-friendly pmedian-benders benchmark pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ["list", "prepare", "run"]:
        sp = sub.add_parser(name)
        sp.add_argument("--set", default="current", choices=["smoke", "current", "orlib", "rl1304", "kro"])
        sp.add_argument("--only", nargs="*", default=[])
    sub.add_parser("sources")
    sub.add_parser("validate")
    runp = sub.choices["run"]
    runp.add_argument("--timeout", type=int, default=300)
    runp.add_argument("--out", default=str(DEFAULT_OUT))
    runp.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR))
    args = ap.parse_args()

    if args.cmd == "sources":
        print("Official/provenance sources:")
        print("- OR-Library pmed: raw pmed*.txt files; parser scripts/parse_orlib.py; official optima instances/orlib/pmedopt.txt; duplicate-edge rule docs/ADR/0002-orlib-duplicate-edges.md")
        print("- TSPLIB: raw .tsp files in instances/tsplib or downloaded from TSPLIB; parser scripts/parse_tsplib.py; distances floored to match paper convention")
        print("- RW: scripts/gen_rw.py can generate RW-like matrices; exact paper RW requires matching seeds/spec")
        print("- BIRCH: scripts/gen_birch.py is BIRCH-like synthetic only; exact paper BIRCH needs data/provenance")
        print("- ODM: not supported; needs forbidden-assignment model/parser")
        print("- Zebra/PopStar/comparators: not in repo; paper-reported only unless user supplies code/binary")
        return 0

    if args.cmd == "validate":
        return subprocess.call([sys.executable, str(ROOT / "scripts" / "validate_results.py")])

    cases = select_cases(args.set, args.only)
    if args.cmd == "list":
        for c in cases:
            n, m, p = read_header(c.instance)
            print(f"{c.run_id:14} family={c.family:10} p={p:>4} exists={c.instance.exists()} opt={c.opt if c.opt is not None else NA} path={rel(c.instance)}")
        return 0

    if args.cmd == "prepare":
        for c in cases:
            print(f"{c.run_id:14} {prepare_case(c)} -> {rel(c.instance)}")
        return 0

    if args.cmd == "run":
        if not PMEDIAN.exists():
            raise SystemExit("./pmedian not found. Run: make")
        rows = [run_case(c, args.timeout, Path(args.log_dir)) for c in cases]
        write_csv(rows, Path(args.out))
        print(f"Wrote {args.out} ({len(rows)} rows)")
        bad = [r for r in rows if r["status"] != "OK" or (r.get("matches_known_opt") == "NO")]
        if bad:
            print("Non-OK rows:")
            for r in bad:
                print(f"  {r['run_id']} status={r['status']} match={r.get('matches_known_opt')} log={r.get('log_path')}")
            return 1
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
