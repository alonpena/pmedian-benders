#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
External 300-second Benders benchmark wrapper.

Important: this wrapper runs ./pmedian from a temporary working directory so the
solver binary cannot append to the repository-level results/benchmark.csv. Raw
stdout/stderr are captured into results/logs/benders_300s/.
"""
from __future__ import annotations

import argparse
import csv
import glob
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
DEFAULT_OUT = RESULTS / "benders_300s_campaign.csv"
DEFAULT_LOG_DIR = RESULTS / "logs" / "benders_300s"
DEFAULT_TIMEOUT = 300
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

CSV_COLUMNS = [
    "family",
    "instance",
    "N",
    "p",
    "command",
    "status",
    "timeout_flag",
    "obj",
    "LB1",
    "UB1",
    "gap",
    "T1",
    "T2",
    "Ttot",
    "iterations",
    "nodes",
    "lazy_cuts",
    "separation_calls",
    "matches_known_opt",
    "delta_opt",
    "log_path",
]


@dataclass
class Case:
    family: str
    instance: str
    path: Path
    known_opt: Optional[float] = None


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def first_data_line(path: Path) -> Optional[str]:
    with path.open() as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                return s
    return None


def read_pmp_header(path: Path) -> tuple[str, str]:
    line = first_data_line(path)
    if not line:
        return NA, NA
    parts = line.split()
    if len(parts) < 3:
        return NA, NA
    return parts[0], parts[2]


def load_orlib_optima() -> dict[str, float]:
    opt = {}
    path = ROOT / "instances" / "orlib" / "pmedopt.txt"
    if not path.exists():
        return opt
    for line in path.read_text().splitlines():
        m = re.match(r"\s*(pmed\d+)\s+(\d+)", line)
        if m:
            opt[m.group(1)] = float(m.group(2))
    return opt


def build_cases(campaign: str) -> list[Case]:
    opt = load_orlib_optima()
    toy = Case("toy", "toy1", ROOT / "instances" / "toy" / "toy1.pmp", 6.0)
    pmed1 = Case("OR-Library", "pmed1", ROOT / "instances" / "orlib" / "pmed1.pmp", opt.get("pmed1"))
    kro = Case("TSPLIB", "kroA100", ROOT / "instances" / "tsplib" / "kroA100.pmp", None)
    if campaign == "smoke":
        return [toy, pmed1, kro]

    cases = [toy]
    for i in range(1, 16):
        name = f"pmed{i}"
        cases.append(Case("OR-Library", name, ROOT / "instances" / "orlib" / f"{name}.pmp", opt.get(name)))
    cases.append(kro)
    for p in [5, 10, 20, 50, 100, 200, 300, 400, 500]:
        path = ROOT / "instances" / "tsplib" / f"rl1304_p{p}.pmp"
        cases.append(Case("TSPLIB", f"rl1304_p{p}", path, float(RL1304_OPT[p])))
    return cases


def ensure_gurobi_env() -> dict[str, str]:
    env = os.environ.copy()
    if not env.get("DYLD_LIBRARY_PATH"):
        candidates = sorted(glob.glob("/Library/gurobi*/macos_universal2/lib"))
        if candidates:
            env["DYLD_LIBRARY_PATH"] = candidates[-1]
    return env


def safe_num(value: Optional[float], digits: int = 6) -> str:
    if value is None:
        return NA
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def decode_timeout_field(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return str(value)


def parse_output(text: str) -> dict[str, Optional[float]]:
    out: dict[str, Optional[float]] = {
        "N": None,
        "p": None,
        "LB1": None,
        "UB1": None,
        "T1": None,
        "iterations": None,
        "obj": None,
        "T2": None,
        "nodes": None,
        "lazy_cuts": None,
        "separation_calls": None,
    }
    m = re.search(r"Instancia\s+.*?:\s+N=(\d+)\s+M=(\d+)\s+p=(\d+)", text)
    if m:
        out["N"] = float(m.group(1))
        out["p"] = float(m.group(3))
    m = re.search(r"\[Fase 1\]\s+LB1=([\d.+\-eE]+)\s+UB1=([\d.+\-eE]+)\s+iter=(\d+)\s+cuts=(\d+)\s+T1=([\d.+\-eE]+)", text)
    if m:
        out["LB1"] = float(m.group(1))
        out["UB1"] = float(m.group(2))
        out["iterations"] = float(m.group(3))
        out["T1"] = float(m.group(5))
    m = re.search(r"\[Fase 2\]\s+opt=([\d.+\-eE]+)\s+cuts=(\d+)\s+nodes=([\d.+\-eE]+)\s+T2=([\d.+\-eE]+)", text)
    if m:
        out["obj"] = float(m.group(1))
        out["lazy_cuts"] = float(m.group(2))
        out["nodes"] = float(m.group(3))
        out["T2"] = float(m.group(4))
    m = re.search(r"separaciones\(MIPSOL\)=(\d+)\s+cortes_lazy=(\d+)\s+nodos_B&B=([\d.+\-eE]+)", text)
    if m:
        out["separation_calls"] = float(m.group(1))
        out["lazy_cuts"] = float(m.group(2))
        out["nodes"] = float(m.group(3))
    return out


def command_for(case: Case) -> tuple[list[str], list[str]]:
    abs_cmd = [str(PMEDIAN), str(case.path), "--mode", "full"]
    rel_cmd = ["./pmedian", rel(case.path), "--mode", "full"]
    if case.known_opt is not None:
        opt_s = str(int(case.known_opt)) if float(case.known_opt).is_integer() else str(case.known_opt)
        abs_cmd += ["--opt", opt_s]
        rel_cmd += ["--opt", opt_s]
    return abs_cmd, rel_cmd


def log_name(run_id: str, case: Case, p: str) -> str:
    raw = f"{run_id}_{case.family}_{case.instance}_p{p}.log"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)


def run_case(case: Case, timeout: int, log_dir: Path, run_id: str) -> dict[str, str]:
    header_N, header_p = read_pmp_header(case.path) if case.path.exists() else (NA, NA)
    abs_cmd, rel_cmd = command_for(case)
    command_str = " ".join(shlex.quote(x) for x in rel_cmd)

    row = {c: NA for c in CSV_COLUMNS}
    row.update({
        "family": case.family,
        "instance": case.instance,
        "N": header_N,
        "p": header_p,
        "command": command_str,
        "timeout_flag": "0",
        "matches_known_opt": NA,
        "delta_opt": NA,
    })

    if not case.path.exists():
        log_path = log_dir / log_name(run_id, case, header_p)
        log_path.write_text(f"COMMAND: {command_str}\nERROR: missing instance file {case.path}\n")
        row["status"] = "ERROR"
        row["log_path"] = rel(log_path)
        return row

    env = ensure_gurobi_env()
    log_dir.mkdir(parents=True, exist_ok=True)
    elapsed = 0.0
    returncode: Optional[int] = None
    timed_out = False
    stdout = ""
    stderr = ""

    with tempfile.TemporaryDirectory(prefix="pmedian_300s_") as tmp:
        start = time.monotonic()
        try:
            proc = subprocess.run(
                abs_cmd,
                cwd=tmp,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            elapsed = time.monotonic() - start
            stdout = proc.stdout or ""
            stderr = proc.stderr or ""
            returncode = proc.returncode
        except subprocess.TimeoutExpired as exc:
            elapsed = time.monotonic() - start
            timed_out = True
            stdout = decode_timeout_field(exc.stdout)
            stderr = decode_timeout_field(exc.stderr)
            returncode = None

    parsed = parse_output(stdout + "\n" + stderr)
    p_for_log = str(int(parsed["p"])) if parsed.get("p") is not None else header_p
    log_path = log_dir / log_name(run_id, case, p_for_log)
    log_path.write_text(
        "COMMAND: " + command_str + "\n"
        + f"TIMEOUT_SECONDS: {timeout}\n"
        + f"TIMEOUT_FLAG: {1 if timed_out else 0}\n"
        + f"RETURNCODE: {returncode if returncode is not None else 'NA'}\n"
        + f"WRAPPER_TTOT_SECONDS: {elapsed:.6f}\n"
        + "\n--- STDOUT ---\n"
        + stdout
        + "\n--- STDERR ---\n"
        + stderr
    )

    for key in ["N", "p", "LB1", "UB1", "T1", "T2", "nodes", "lazy_cuts", "separation_calls"]:
        if parsed.get(key) is not None:
            if key in {"N", "p", "nodes", "lazy_cuts", "separation_calls"}:
                row[key] = str(int(round(parsed[key])))
            else:
                row[key] = safe_num(parsed[key])
    if parsed.get("iterations") is not None:
        row["iterations"] = str(int(round(parsed["iterations"])))
    if parsed.get("obj") is not None:
        row["obj"] = safe_num(parsed["obj"])
    row["Ttot"] = safe_num(elapsed)
    row["timeout_flag"] = "1" if timed_out else "0"
    row["log_path"] = rel(log_path)

    obj = parsed.get("obj")
    lb1 = parsed.get("LB1")
    if obj is not None and lb1 is not None and obj > 0:
        row["gap"] = safe_num((obj - lb1) / obj)

    if timed_out:
        row["status"] = "TIMEOUT"
    elif returncode not in (0, None):
        row["status"] = "ERROR"
    elif obj is None:
        row["status"] = "PARSE_WARNING"
    elif case.known_opt is None:
        row["status"] = "OPTIMAL_NO_KNOWN"
    else:
        delta = obj - case.known_opt
        row["delta_opt"] = safe_num(delta)
        if abs(delta) < 0.5:
            row["status"] = "OPT_MATCH"
            row["matches_known_opt"] = "YES"
        else:
            row["status"] = "MISMATCH"
            row["matches_known_opt"] = "NO"

    return row


def write_rows(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing {path}. Use --overwrite.")
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run pmedian Benders benchmark with external 300s timeout.")
    ap.add_argument("--campaign", choices=["smoke", "full"], default="full")
    ap.add_argument("--time-limit", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()

    if not PMEDIAN.exists():
        raise SystemExit("Missing ./pmedian. Run `make` first.")

    run_id = args.run_id or f"{args.campaign}_{time.strftime('%Y%m%d_%H%M%S')}"
    cases = build_cases(args.campaign)
    rows = []
    for i, case in enumerate(cases, start=1):
        print(f"[{i}/{len(cases)}] {case.family} {case.instance}")
        row = run_case(case, args.time_limit, args.log_dir, run_id)
        print(f"  status={row['status']} timeout={row['timeout_flag']} obj={row['obj']} log={row['log_path']}")
        rows.append(row)

    write_rows(args.output, rows, args.overwrite)
    print(f"Wrote {args.output} ({len(rows)} rows)")

    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print("Status counts:")
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
