# OR-Library pmed16 smoke handoff

## Phase

PHASE 4 Option A — official OR-Library pmed16 smoke.

## Branch

- `exp/orlib-pmed16-smoke`
- Base commit: `15a150a`

## Source

Official OR-Library source:

- `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/pmed16.txt`
- Source page: `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/pmedinfo.html`

Official optimum from local `instances/orlib/pmedopt.txt`:

- `pmed16 = 8162`

## Conversion

Command:

```bash
python3 scripts/parse_orlib.py instances/orlib/pmed16.txt instances/orlib/pmed16.pmp
```

Converted header:

```text
400 400 5
```

## Smoke run

External timeout policy:

- Python `subprocess.run(..., timeout=300)`.
- Log records `TIMEOUT_SECONDS: 300` and `TIMEOUT_FLAG: 0`.

Run command equivalent:

```bash
./pmedian instances/orlib/pmed16.pmp --mode full --opt 8162
```

Output files:

- `results/orlib_pmed16_smoke_300s.csv`
- `results/logs/orlib_pmed16_smoke/pmed16_300s.log`

## Result

| instance | N | p | status | obj | known opt | timeout_flag | Ttot | nodes | lazy cuts |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| pmed16 | 400 | 5 | OPT_MATCH | 8162 | 8162 | 0 | 0.793458 | 68 | 265 |

Phase output from log:

```text
[Fase 1] LB1=8092.0000 UB1=8188.0 iter=7 cuts=1573 T1=0.134 s
[Fase 2] opt=8162.0 cuts=265 nodes=68 T2=0.620 s start=warm set={19,228,266,373,378}
[CALLBACK] warm_cuts=1573  separaciones(MIPSOL)=15  cortes_lazy=265  nodos_B&B=68
```

## Tests

Ran:

```bash
make test
```

Both tests printed `RESULT: PASS`.

## Interpretation

- Official OR-Library pmed16 can be downloaded, converted, and solved locally under 300-second wrapper.
- This supports expanding OR-Library replication beyond pmed1–pmed15.
- This is only one smoke row; do not claim pmed16–pmed40 campaign complete.

## Next safe step

Create a dedicated wrapper for pmed16–pmed40, run first pmed16–pmed20 with 300s external timeout, then expand if no failures/timeouts.
