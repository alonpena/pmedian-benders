# Web source and replication feasibility audit

## Scope

Internet was available. Checked official/trustworthy sources first. Did not download huge datasets. Did not build external Zebra/PopStar.

## Source table

| component | source_url_or_reference | available | license_or_provenance | local_status | implementation_risk | next_action |
|---|---|---|---|---|---|---|
| OR-Library pmed1–pmed40 | `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/pmedinfo.html` and `.../orlib/files/pmed*.txt` | yes | OR-Library / J.E. Beasley benchmark data; page states 40 files and pmedopt | pmed1–15 local `.pmp`; pmed16–40 not local | low/moderate: parser exists but conversion from OR-Library edge format must be applied consistently with duplicate-edge/Floyd rule | Download/convert one pmed16 smoke first, then expand if clean |
| OR-Library pmed16 | `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/pmed16.txt` | yes, HEAD 200, ~39KB | OR-Library | not local | low | Safe candidate for Option A |
| OR-Library pmed40 | `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/pmed40.txt` | yes, HEAD 200, ~205KB | OR-Library | not local | low/moderate due largest OR-Lib size | Later, after pmed16 smoke |
| TSPLIB rl1304 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/rl1304.tsp.gz` | yes, HEAD 200 | TSPLIB95 / University Heidelberg mirror | raw and `.pmp` p-grid local | low | already run available p-grid |
| TSPLIB fl1400 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/fl1400.tsp.gz` | yes, HEAD 200 | TSPLIB95 | raw `.tsp` local, no `.pmp` p-grid | low/moderate: converter exists but p-grid/optima must be defined | candidate Option B |
| TSPLIB u1432 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/u1432.tsp.gz` | yes, HEAD 200 | TSPLIB95 | raw `.tsp` local, no `.pmp` p-grid | low/moderate | candidate Option B |
| TSPLIB vm1748 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/vm1748.tsp.gz` | yes, HEAD 200 | TSPLIB95 | raw `.tsp` local, no `.pmp` p-grid | low/moderate | candidate Option B |
| TSPLIB d2103 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/d2103.tsp.gz` | yes, HEAD 200 | TSPLIB95 | not local | moderate | download only if needed; convert p-grid |
| TSPLIB pcb3038 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/pcb3038.tsp.gz` | yes, HEAD 200 | TSPLIB95 | not local | moderate | later candidate |
| TSPLIB fl3795 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/fl3795.tsp.gz` | yes, HEAD 200 | TSPLIB95 | not local | moderate/high | later candidate, confirm memory |
| TSPLIB rl5934 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/rl5934.tsp.gz` | yes, HEAD 200 | TSPLIB95 | not local | high for local sort/campaign | do not run tonight without memory check |
| TSPLIB usa13509 | `https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/usa13509.tsp.gz` | yes, HEAD 200, ~118KB compressed | TSPLIB95 | not local | too risky tonight: N=13509 coordinate sort/cuts likely heavy | document only |
| TSPLIB sw24978 | checked `.../sw24978.tsp`, `.tsp.gz`, `.zip` | not found at checked TSPLIB mirror | unknown | not local | unknown | mark NEEDS_DOWNLOAD / source unresolved |
| PopStar | Resende & Werneck (2004) heuristic referenced in project docs; no official public source found in light web/GitHub search | not confirmed | literature reference only; no local code | not implemented | high integration risk; would affect heuristic/UB path | write feasibility only; do not claim implemented |
| Zebra | García, Labbé & Marín (2011) method referenced by paper; no official author/paper source found in light search | not confirmed | paper comparator only | not implemented/run | very high; branch-cut-and-price external method | mark NEEDS_AUTHOR_CODE / NOT_AVAILABLE_PUBLICLY unless official source appears |
| GitHub `paulafernalia/p-median-zebra` | `https://github.com/paulafernalia/p-median-zebra` | yes | MIT; 2025 student-style repo; README says column generation with HiGHS, not paper Zebra | not local | not suitable as paper Zebra evidence | do not use for Zebra claims |
| BIRCH | Paper/project docs describe BIRCH-style clustered 2D points; local `scripts/gen_birch.py` exists | official paper dataset not found in this light audit | local generator only, no campaign | not run | moderate if synthetic generator accepted; high if exact paper data required | keep as NOT_RUN / needs source decision |
| RW | Project docs cite Resende & Werneck (2004); local `scripts/gen_rw.py` and `rw12.pmp` exist | generator available locally; exact paper campaign data not downloaded | tiny local rw12 only | partial local | moderate: generator easy, full campaign can be run but not same as external data unless seed/spec matches paper | feasible synthetic-style RW campaign later, label honestly |
| ODM | Paper/project docs cite Briant & Naddef (2004), N=3773 with forbidden assignments | no local data/source found in light audit | no parser support for forbidden assignments | not implemented | high: model/parser need forbidden-assignment support | not tonight |

## Notes

- OR-Library is the cleanest path toward fuller replication. Official pmed16–pmed40 are small/moderate and format is known.
- TSPLIB small/medium is feasible because direct official `.tsp.gz` files exist and local raw `fl1400/u1432/vm1748` already exist, but p-grid selection must match paper before claims.
- Zebra remains paper-only. A GitHub repo with “zebra” in the name exists but is not proven to be the García–Labbé–Marín Zebra code and must not be used for claims.
- PopStar source availability remains unconfirmed; integration should not be attempted without trustworthy source/provenance.

## Verdict

Best low-risk next replication move: OR-Library pmed16 smoke conversion/run from official OR-Library source. Second-best: TSPLIB `fl1400`/`u1432`/`vm1748` preprocessing if p-grid is defined.
