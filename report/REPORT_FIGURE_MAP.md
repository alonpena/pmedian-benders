# Report figure map

| figure filename | source CSV | branch | report section | caption in Spanish | interpretation | caution |
|---|---|---|---|---|---|---|
| `results/figures/benders_300s_runtime_by_instance.png` | `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | 9.1 / 10 | Tiempo total de la campaña Benders 300s por instancia. | Muestra variación de tiempo; máximo en `rl1304_p10`. | Tiempo local, no comparable máquina-independiente. |
| `results/figures/benders_300s_nodes_by_instance.png` | `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | 9.1 / 10 | Nodos branch-and-bound por instancia en Benders. | La mayoría de filas tiene pocos nodos; `rl1304_p10` destaca. | Nodos dependen de Gurobi y configuración. |
| `results/figures/benders_300s_lazy_cuts_by_instance.png` | `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | 5 / 9.1 | Cortes lazy generados por instancia. | Evidencia funcionamiento branch-and-Benders-cut. | No mide por sí sola dificultad total. |
| `results/figures/benders_300s_runtime_vs_N.png` | `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | 9.1 / 11 | Tiempo total Benders versus tamaño N. | Resume escalamiento en campaña curada. | p y familia también influyen; no aislar causalidad. |
| `results/figures/benders_300s_status_summary.png` | `results/benders_300s_campaign.csv` | `exp/requirements-and-300s-benchmark` | 9.1 | Resumen de estados de campaña Benders. | 25 `OPT_MATCH`, 1 `OPTIMAL_NO_KNOWN`, 0 timeouts. | `OPTIMAL_NO_KNOWN` no significa óptimo externo verificado. |
| `results/figures/gap_vs_iteration_pmed1.png` | `results/gap_traces/pmed1_p5_phase1.csv` | `exp/gap-trace-integration` | 9.5 / 10 | Evolución del gap de Fase 1 en pmed1. | Muestra cierre del gap a 0 en 6 iteraciones. | Es gap de Fase 1, no gap MIP de Fase 2. |
| `results/figures/bounds_vs_iteration_pmed1.png` | `results/gap_traces/pmed1_p5_phase1.csv` | `exp/gap-trace-integration` | 5 / 9.5 | Evolución de LB y UB de Fase 1 en pmed1. | Conecta cortes con mejora de cotas. | Solo una instancia representativa. |
| `results/figures/benders_vs_monolithic_runtime.png` | `results/benders_300s_campaign.csv`, `results/monolithic_f1_300s.csv` | `exp/monolithic-baselines` | 9.4 / 11 | Comparación de tiempo Benders versus F1 monolítico. | Benders es más rápido en 4 de 5 filas locales. | No extrapolar a todos los modelos ni a Zebra. |
| `results/figures/benders_vs_monolithic_gap.png` | same | `exp/monolithic-baselines` | 9.4 | Comparación de columnas de gap registradas. | Ilustra métricas registradas. | Definiciones de gap difieren; usar con cuidado. |
| `results/figures/benders_vs_monolithic_nodes.png` | same | `exp/monolithic-baselines` | 9.4 | Comparación de nodos B&B Benders versus F1. | Muestra diferencias de exploración. | Nodos no son tiempo y dependen del solver. |
| `results/figures/synthetic_runtime_vs_N.png` | `results/synthetic_stress_300s.csv` | `exp/synthetic-stress` | 9.6 / 11 | Tiempo en estrés sintético versus N. | Evidencia escalamiento local hasta N=5000. | Instancias sintéticas sin óptimos externos. |
| `results/figures/synthetic_lazy_cuts_vs_N.png` | `results/synthetic_stress_300s.csv` | `exp/synthetic-stress` | 9.6 | Cortes lazy en estrés sintético versus N. | Aumentan con tamaño y p-grid. | No es benchmark del paper. |
| `results/figures/synthetic_nodes_vs_N.png` | `results/synthetic_stress_300s.csv` | `exp/synthetic-stress` | 9.6 | Nodos B&B en estrés sintético versus N. | `N=5000,p=5%` destaca con 292 nodos. | Distribución sintética específica. |
| `results/figures/synthetic_timeout_summary.png` | `results/synthetic_stress_300s.csv` | `exp/synthetic-stress` | 9.6 | Resumen de timeouts sintéticos. | 0 timeouts en 18 filas. | No implica garantía para instancias reales grandes. |

## Toy figure TODO

No hay PNG dedicado de instancia toy en `results/figures/`. Recomendación: crear manualmente en el documento final una figura simple con cuatro puntos, dos medianas seleccionadas y arcos de asignación. Marcar como figura pedagógica, no como resultado experimental.
