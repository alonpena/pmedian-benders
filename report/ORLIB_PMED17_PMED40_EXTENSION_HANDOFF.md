# OR-Library pmed17-pmed40 extension handoff

## Scope

Official OR-Library extension after final evidence consolidation.

## Source

- Official OR-Library source pattern: `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/pmedXX.txt`
- Optima: `instances/orlib/pmedopt.txt`

## Protocol

- pmed17 was run first as smoke.
- Because pmed17 matched official optimum, pmed18-pmed40 were run.
- External timeout: `subprocess.run(..., timeout=300)` for each instance.
- No solver core code changed.

## Outputs

- CSV: `report/evidence/csv/orlib_pmed17_pmed40_300s.csv`
- Logs: `report/evidence/logs/orlib_pmed17_pmed40/`
- Converted/downloaded data: `report/evidence/metadata/orlib_sources/`, `report/evidence/metadata/orlib_pmp/`
- Figure: `report/figures/orlib_pmed1_pmed40_runtime.png`

## Summary

| metric | value |
|---|---:|
| rows | 24 |
| OPT_MATCH | 24 |
| timeout_flag=0 | 24 |
| max Ttot | 10.695018 |
| max runtime instance | pmed36 |

## Interpretation

Together with prior evidence for pmed1-pmed15 and the pmed16 smoke, the project now has local 300-second evidence for OR-Library pmed1-pmed40. The rows were produced across multiple controlled runs, not one monolithic historical campaign.
