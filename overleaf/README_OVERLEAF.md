# Overleaf — paquete limpio

Paquete autocontenido para compilar informe y diapositivas en Overleaf. Dos proyectos independientes: `report/` y `slides/`.

## Qué subir

**Proyecto informe:** subir todo `overleaf/report/`:

```text
main.tex
sections/*.tex
figures/*.png
```

**Proyecto diapositivas:** subir todo `overleaf/slides/`:

```text
main.tex
```

## Archivo principal

- Informe: `main.tex` dentro del proyecto `report/`.
- Diapositivas: `main.tex` dentro del proyecto `slides/`.

## Compilación

- Compilador: **pdfLaTeX**.
- Shell escape: **no requerido**.
- Bibliografía: no hay `.bib`; referencias manuales en `report/main.tex`.
- Figuras: rutas relativas `figures/...`.

## Paquetes usados

Paquetes estándar Overleaf: `inputenc`, `fontenc`, `babel`, `amsmath`, `amssymb`, `amsthm`, `mathtools`, `graphicx`, `booktabs`, `array`, `longtable`, `enumitem`, `geometry`, `xcolor`, `listings`, `hyperref`, `caption`.

## Figuras incluidas

- `overleaf/report/figures/plot_a_bounds_orlib.png`
- `overleaf/report/figures/plot_b_time_vs_N.png`
- `overleaf/report/figures/plot_c_gap_vs_pM.png`
- `overleaf/report/figures/plot_d_iter_nodes_vs_p.png`

No hay figuras en slides.

## Verificación estructural local

La máquina local no tiene `pdflatex`; se hicieron chequeos estructurales:

- Todos los `\input{...}` existen.
- Todos los `\includegraphics{...}` existen.
- No hay rutas absolutas en archivos LaTeX del paquete.
- No hay marcadores visibles de pendientes en archivos LaTeX del paquete.
- No hay dependencia de shell-escape.
- No hay archivo de bibliografía requerido.

## Riesgos conocidos

- Compilación real debe confirmarse en Overleaf.
- Si Overleaf cambia versión de `babel`/Beamer, podría requerir recompilar dos veces, pero no hay dependencia no estándar.
- Comparación Zebra y campaña grande no son resultados locales; el informe lo declara como alcance experimental parcial.
