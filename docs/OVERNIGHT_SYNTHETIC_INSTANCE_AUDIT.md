# Overnight synthetic instance audit

## Scope

Audited generated synthetic `.pmp` files from branch `exp/synthetic-stress`, commit `d6241d8`/`c5de792`.

## Intended grid

- `N = 100, 250, 500, 1000, 2000, 5000`
- `p_pct = 5, 10, 20`
- seed `20260622`
- p rule: `floor(N * p_pct / 100)`, minimum 1
- M should equal N

## File count

Expected: 18 files.
Found: 18 files.

## Header validation

All synthetic file headers match intended `N`, `M=N`, and p value inferred from filename.

| N | p_pct | expected p |
|---:|---:|---:|
| 100 | 5 | 5 |
| 100 | 10 | 10 |
| 100 | 20 | 20 |
| 250 | 5 | 12 |
| 250 | 10 | 25 |
| 250 | 20 | 50 |
| 500 | 5 | 25 |
| 500 | 10 | 50 |
| 500 | 20 | 100 |
| 1000 | 5 | 50 |
| 1000 | 10 | 100 |
| 1000 | 20 | 200 |
| 2000 | 5 | 100 |
| 2000 | 10 | 200 |
| 2000 | 20 | 400 |
| 5000 | 5 | 250 |
| 5000 | 10 | 500 |
| 5000 | 20 | 1000 |

## Distance rule

The generator writes coordinate-mode `.pmp` files. Existing solver distance function computes Euclidean distances rounded down for coordinate instances. Thus synthetic distances are not explicitly materialized, but use the repository's coordinate distance oracle.

## Campaign validation

`results/synthetic_stress_300s.csv` on branch `exp/synthetic-stress` has 18 rows, matching the 18 generated files. All rows have `timeout_flag=0` and `status=OPTIMAL_NO_KNOWN`.

## Suspicious or caution items

- Synthetic rows have no external known optimum; `OPTIMAL_NO_KNOWN` means solver reported local optimality, not independent benchmark validation.
- Coordinate generation uses integer coordinates in `[0, 1_000_000]`; results should be described as one deterministic synthetic distribution, not general Euclidean behavior.

## Verdict

Synthetic instance audit passes. Grid and headers match specification.
