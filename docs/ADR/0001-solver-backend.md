# ADR 0001 — Backend de solver por defecto: Gurobi

**Estado:** aceptado (2026-06-17).

## Contexto
Fase 2 necesita un árbol de branch-and-cut con callbacks de lazy constraints.
Escribir B&B desde cero queda fuera de alcance. Opciones de solver disponibles:
Gurobi (instalado, con licencia), CPLEX (el del paper, **no** instalado aquí),
SCIP/HiGHS (abiertos, sin licencia).

## Decisión
Backend por defecto = **Gurobi 12.0.0**. Se mantiene una capa de abstracción
delgada en C (`src/solver.h`) con backends seleccionables en compilación
(`make SOLVER=gurobi|cplex|scip`) para no acoplar el núcleo al solver.

## Consecuencias
- (+) Licencia académica activa, callbacks lazy bien documentados (ver `SOLVER_NOTES.md`).
- (+) La abstracción permite agregar CPLEX (comparación fiel al paper) o SCIP (repro sin licencia) después.
- (−) CPLEX no verificable ahora (header ausente). Comparación contra el paper tendrá diferencia de máquina/solver — se reportará como nota en `comparison_vs_paper.csv`.
