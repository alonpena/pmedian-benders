# Final submission audit

Fecha: 2026-06-19. Rama: `main`. Repo: `github.com/alonpena/pmedian-benders`.

## Final commit

- Commit final de la entrega: ver salida final de `git rev-parse HEAD` después del commit `docs: align final submission with honest paper replication scope`.
- Nota técnica: no se incrusta el hash exacto dentro de este archivo porque modificar el archivo cambiaría el hash del commit. El hash exacto se imprime en el handoff final.

## Clean git status

Esperado al cierre:

```bash
git status --short
# sin archivos modificados/no trackeados relevantes
```

Los PDFs locales en `informe/` son artefactos generados y no forman parte del paquete fuente; se ignoran para mantener estado limpio.

## Readiness status

**READY_WITH_RISKS**

Criterios:

| Criterio | Estado |
|---|---|
| Report source exists | READY: `report/main.tex` |
| Slides source exists | READY: `slides/main.tex` |
| Overleaf package exists | READY: `overleaf/report/`, `overleaf/slides/` |
| Algorithm verified | READY: separator tests + OR-Library + `rl1304` evidence |
| Repo clean after commit | READY target; verify with `git status --short` |
| Zebra rerun | RISK: NOT_RUN |
| Full paper campaign | RISK: NOT_RUN |

## Exact artifacts to submit

### Primary upload to Overleaf

- `overleaf/report/` — upload as one Overleaf project; main file `main.tex`.
- `overleaf/slides/` — upload as second Overleaf project; main file `main.tex`.

### Course/repo artifacts

- Report source: `report/main.tex`
- Slides source: `slides/main.tex`
- Results: `results/*.csv`, `results/logs/*.log`, `results/plot_*.png`
- Final defense notes: `docs/DEFENSA_ORAL.md`
- Replication audit: `docs/CONSISTENCY_AND_REPLICATION_AUDIT.md`
- Paper matrix: `docs/PAPER_REPLICATION_MATRIX.md`
- Numerical trace: `docs/NUMERICAL_CLAIMS_TRACE.md`

## Local verification commands run

```bash
make test                                  # PASS
.venv/bin/python scripts/verify_cuts.py    # PASS, 0 diffs
python3 structural_overleaf_check          # inputs=13 graphics=4 missing=0
rg -n "TODO|FALTA" overleaf/report overleaf/slides -S   # no matches
rg -n "/Users|/Library|/opt|/tmp|/var|/home" overleaf/report overleaf/slides -S  # no matches
```

Recorded status: PASS before final commit.

## Commands unavailable

```bash
python scripts/verify_cuts.py      # `python` command not found; `.venv/bin/python` works
pdflatex report/main.tex
pdflatex slides/main.tex
```

Reason: local TeX toolchain unavailable (`pdflatex` not found). Structural checks were used instead; final compilation must be done in Overleaf.

## Overleaf structural readiness

| Check | Status |
|---|---|
| Standard packages only | READY |
| Relative figure paths | READY |
| All figures copied locally | READY |
| All `\input` files present | READY |
| No bibliography file required | READY |
| No shell-escape | READY |
| No absolute paths in LaTeX package | READY |
| No visible pending markers in LaTeX package | READY |

## Replication-scope risks

1. Zebra not implemented or run locally. Any Zebra comparison is a literature claim from the paper.
2. Large/huge TSP, BIRCH, RW large, ODM not run locally.
3. PopStar, reduced-cost fixing, constraint reduction not implemented.
4. Local solver is Gurobi, not paper CPLEX.
5. Local LaTeX compilation unavailable; Overleaf compile remains final check.

## Final defense wording

Replicamos completamente el mecanismo algorítmico central propuesto por Duran-Mateluna et al. —F3, maestro, subproblema, dual, cortes, separación O(NM), dos fases y warm-start—. En lo computacional, reproducimos y verificamos un subconjunto de instancias disponible en el repositorio. No reejecutamos Zebra ni toda la campaña de gran escala, por lo que esas comparaciones se citan como resultados del paper, no como resultados locales.
