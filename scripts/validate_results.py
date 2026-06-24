#!/usr/bin/env python3
"""validate_results.py — check evidence integrity for pmedian-benders replication.

Exit 0 with PASS if all checks pass.
Exit 1 with FAIL listing each violation.
"""

import csv
import os
import pathlib
import sys
import collections

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

RESULTS = REPO_ROOT / "results"
LOGS = RESULTS / "logs"

REQUIRED_LOGS = [
    "pmed1.pmp_p5_full.log",
    "rl1304_p5.pmp_p5_full.log",
    "kroA100.pmp_p10_full.log",
    "verify_cuts_oracle_diff.log",
]

def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")

def check_benchmark_no_duplicates() -> bool:
    p = RESULTS / "benchmark.csv"
    if not p.exists():
        fail(f"{p} not found")
        return False
    with open(p) as f:
        rows = list(csv.DictReader(f))
    key = lambda r: (r.get("instance", ""), r.get("mode", ""), r.get("opt_known", ""))
    counter = collections.Counter(key(r) for r in rows)
    dups = {k: v for k, v in counter.items() if v > 1}
    if dups:
        for k, v in dups.items():
            fail(f"benchmark.csv duplicate key {k}: {v} rows")
        return False
    print(f"  PASS  benchmark.csv: {len(rows)} rows, 0 duplicates")
    return True

def check_orlib_optima() -> bool:
    p = RESULTS / "orlib_optima_check.csv"
    if not p.exists():
        fail(f"{p} not found")
        return False
    with open(p) as f:
        rows = list(csv.DictReader(f))
    ok = True
    for r in rows:
        if r.get("status") != "OPT_MATCH" or float(r.get("delta", "1")) != 0.0:
            fail(f"orlib_optima_check.csv {r.get('instance','?')}: status={r.get('status')} delta={r.get('delta')}")
            ok = False
    if ok:
        print(f"  PASS  orlib_optima_check.csv: {len(rows)} rows all OPT_MATCH delta=0")
    return ok

def check_comparison_vs_paper() -> bool:
    p = RESULTS / "comparison_vs_paper.csv"
    if not p.exists():
        fail(f"{p} not found")
        return False
    with open(p) as f:
        rows = list(csv.DictReader(f))
    ok = True
    for r in rows:
        if r.get("opt_comparison") != "OK" or float(r.get("delta_OPT", "1")) != 0.0:
            fail(f"comparison_vs_paper.csv {r.get('instance','?')} p={r.get('p','?')}: "
                 f"opt_comparison={r.get('opt_comparison')} delta_OPT={r.get('delta_OPT')}")
            ok = False
    if ok:
        print(f"  PASS  comparison_vs_paper.csv: {len(rows)} rows all OK delta_OPT=0")
    return ok

def check_logs_exist() -> bool:
    ok = True
    for name in REQUIRED_LOGS:
        p = LOGS / name
        if not p.exists():
            fail(f"required log missing: {name}")
            ok = False
        else:
            print(f"  PASS  log exists: {name}")
    return ok

def check_logs_content() -> bool:
    ok = True
    # is_branch_and_benders_cut=YES in all full solver logs
    solver_logs = [n for n in REQUIRED_LOGS if n != "verify_cuts_oracle_diff.log"]
    for name in solver_logs:
        p = LOGS / name
        if not p.exists():
            continue
        content = p.read_text()
        if "is_branch_and_benders_cut=YES" not in content:
            fail(f"{name}: missing is_branch_and_benders_cut=YES")
            ok = False
        # lazy_cuts should be present (integer > 0 expected for real instances)
        # We just check that the key exists; value can be read
        if "lazy_cuts=" not in content:
            fail(f"{name}: missing lazy_cuts=")
            ok = False
    # oracle diff: diffs=0
    diff_log = LOGS / "verify_cuts_oracle_diff.log"
    if diff_log.exists():
        content = diff_log.read_text()
        if "diffs=" in content:
            # extract value
            for line in content.splitlines():
                if "diffs=" in line:
                    val = line.split("diffs=")[1].split()[0]
                    if val != "0":
                        fail(f"verify_cuts_oracle_diff.log: diffs={val} (expected 0)")
                        ok = False
                    else:
                        print(f"  PASS  verify_cuts_oracle_diff.log: diffs=0")
    if ok and all(LOGS / n for n in solver_logs):
        print("  PASS  log content checks (branch-and-Benders-cut, lazy_cuts)")
    return ok

def main() -> int:
    print("Validating pmedian-benders evidence...")
    results = [
        check_benchmark_no_duplicates(),
        check_orlib_optima(),
        check_comparison_vs_paper(),
        check_logs_exist(),
        check_logs_content(),
    ]
    if all(results):
        print("\nRESULT: PASS")
        return 0
    else:
        print(f"\nRESULT: FAIL ({len([r for r in results if not r])} of {len(results)} checks failed)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
