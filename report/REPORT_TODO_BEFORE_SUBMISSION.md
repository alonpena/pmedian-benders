# Report TODO before submission

## Critical checks

1. Completar hardware/software: CPU, RAM, macOS versión, Gurobi versión exacta, compilador.
2. Confirmar si el formato final será LaTeX/Overleaf, DOCX o PDF generado desde Markdown.
3. Verificar referencias en formato APA/BibTeX: Duran-Mateluna et al. (2023), ReVelle & Swain, Beasley OR-Library, TSPLIB/Reinelt, Gurobi.
4. Confirmar instrucciones formales del curso: extensión, portada, secciones obligatorias, rúbrica.
5. Revisar que cada número en el informe tenga ruta de evidencia en `REPORT_TABLES.md` o `REPORT_CLAIMS_AUDIT.md`.

## Figures

6. Elegir 5–8 figuras finales; no saturar el informe.
7. Copiar o regenerar figuras de ramas experimentales si se necesita un único directorio final.
8. Figura pedagógica toy creada en `report/figures/toy_pmedian_explanation.png`; revisar estética final.
9. Mejorar estética de figuras si se instala matplotlib; mantener CSV como fuente.
10. Confirmar captions finales en español.

## Content polish

11. Ajustar longitud del resumen a requerimiento exacto si el profesor lo especifica.
12. Revisar consistencia de notación: `i`, `j`, `I`, `J`, `d_ij`, `x_ij`, `y_j`, `theta_i`.
13. Revisar que `theta_i` se explique como cota/costo de cliente y no como variable de asignación.
14. Diferenciar claramente LB de relajación LP, LB del maestro Benders, UB incumbente, MIP gap y status experimental.
15. Añadir una explicación corta de complejidad/tamaño F1 versus maestro Benders.
16. Incluir explícitamente la respuesta “¿hasta qué tamaño se resolvió?” con N=1304 real/preprocesado y N=5000 sintético.
17. Añadir una tabla corta de “lo replicado vs lo no replicado”.
18. Actualizar narrativa: OR-Library pmed1–pmed40 ahora tiene evidencia consolidada; pmed16 sigue siendo smoke individual dentro de esa consolidación.
19. Verificar que `kroA100` se presente como `OPTIMAL_NO_KNOWN`, no como match externo.
20. Evitar todo lenguaje de marketing: usar “evidencia local”, “replicación parcial”, “auditado”.

## Reproducibility

21. Mapa de evidencia creado en `report/FINAL_EVIDENCE_INDEX.md`; decidir si incluirlo como apéndice.
22. Explicar que no todos los artefactos están en una sola rama.
23. Verificar comandos de reproducción por rama.
24. Confirmar que las rutas de logs citadas existen en sus ramas.
25. Confirmar que el informe no invita a correr campañas largas sin advertencia.

## Claims discipline

26. Buscar en el borrador frases prohibidas: “supera a Zebra”, “replicación completa”, “PopStar implementado”.
27. Asegurar que Zebra se mencione solo como comparación reportada por el paper.
28. Asegurar que BIRCH/RW/ODM figuren como limitaciones/futuro trabajo.
29. Asegurar que synthetic stress no se presente como benchmark del paper.
30. Asegurar que monolithic F1 se presente como baseline local, no como paper C benchmark.
