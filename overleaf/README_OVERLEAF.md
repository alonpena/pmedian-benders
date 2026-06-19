# Overleaf — instrucciones de subida y compilación

Paquete autocontenido para compilar el informe y las diapositivas en Overleaf.
Dos proyectos independientes: `report/` y `slides/`.

## Qué subir

**Proyecto 1 — Informe:** subir el contenido de `overleaf/report/`:
```
main.tex
sections/*.tex          (13 secciones + anexo_codigo.tex)
figures/*.png           (4 figuras)
```

**Proyecto 2 — Diapositivas:** subir `overleaf/slides/main.tex` (un solo archivo, sin figuras).

## Cómo subir
1. Overleaf → New Project → Upload Project → arrastrar la carpeta `report/` (o un .zip de su contenido).
2. Repetir para `slides/` como proyecto separado.

## main.tex
- Informe: `report/main.tex` (documento `article`, español).
- Diapositivas: `slides/main.tex` (Beamer 16:9, tema Madrid).

## Compilación
- Compilador: **pdfLaTeX** (Menu → Compiler → pdfLaTeX). NO requiere shell-escape.
- Pasadas: **2** (la segunda resuelve `\ref`/`\eqref`, el índice y la lista de `\todo`).
- En Overleaf, "Recompile" basta; corre las pasadas necesarias.

## Bibliografía
- **No hay `.bib` ni `bibtex/biber`.** Las referencias están como lista manual
  (`\begin{itemize}`) al final de `report/main.tex`. No se requiere paso de bibliografía.
- Si en el futuro se migra a BibTeX: añadir `referencias.bib`, reemplazar la lista por
  `\bibliographystyle{plain}\bibliography{referencias}` y compilar pdfLaTeX → BibTeX → pdfLaTeX ×2.

## Paquetes usados (todos estándar en Overleaf, sin instalación)
`inputenc, fontenc, babel(spanish), amsmath, amssymb, amsthm, mathtools, graphicx,
booktabs, array, longtable, enumitem, geometry, xcolor, listings, etoolbox, hyperref, caption`.
Babel con `es-noshorthands` para que `listings` y el modo matemático no choquen con los
shorthands del español.

## Checklist de figuras
- [ ] `figures/plot_a_bounds_orlib.png` — cotas LB1/UB1/óptimo OR-Library.
- [ ] `figures/plot_b_time_vs_N.png` — tiempo total vs N (log-log).
- [ ] `figures/plot_c_gap_vs_pM.png` — brecha Fase 1 vs p/M.
- [ ] `figures/plot_d_iter_nodes_vs_p.png` — iteraciones y nodos vs p.
- Las 4 se referencian en `sections/09_experimentos.tex` con rutas relativas `figures/...`.
- Tras compilar, confirmar que las 4 aparecen (no como cajas vacías).

## Verificaciones hechas (antes de empacar)
- ✅ Sin rutas absolutas en `\input`/`\includegraphics` (rutas de figura relativas `figures/`).
- ✅ Las menciones a `/Library/gurobi...` en `sections/11_reproducibilidad.tex` son **texto de
  comandos shell** (cómo fijar `GUROBI_HOME`), no rutas de LaTeX: inofensivas para Overleaf.
- ✅ Los 13 `\input{sections/...}` + `anexo_codigo` existen.
- ✅ Balance de entornos `\begin`/`\end` y paridad de `$` correctos en los 14 archivos.
- ✅ Macros `\OPT,\kt,\R,\argmin,\todo` definidas en el preámbulo de `main.tex`.
- ⚠️ No se compiló localmente (sin toolchain TeX en la máquina de origen): la verificación es
  estructural. La compilación final debe hacerse en Overleaf.

## TODOs restantes (se imprimen al final del PDF compilado)
1. **Figura/esquema del sistema** (clientes → sitio abierto más cercano, sobre `toy1`):
   marcado con `\todo{...}` en `sections/01_motivacion.tex`. Es el único hueco abierto.
   Para agregarla: crear `figures/sistema.png` y un `\includegraphics`, luego borrar el `\todo`.

## Opcionales (baja prioridad, ver docs/REPORT_UPGRADE_PLAN.md)
- Ejemplo numérico de una iteración de subgradiente lagrangiano en `toy1`.
- Glosario de notación ($\theta_i$ del pMP vs $\eta$/$\theta(x)$ genérico del curso).
