# Report claims audit

## SAFE CLAIMS

1. El proyecto implementa un núcleo Benders estilo F4 derivado de F3 con variables `y_j` y `theta_i`. Evidence: `src/phase1.c`, `src/phase2.c`, `report/evidence/docs/PAPER_REPLICATION_MATRIX.md`.
2. La campaña Benders 300s contiene 26 filas, 25 `OPT_MATCH`, 1 `OPTIMAL_NO_KNOWN` y 0 timeouts. Evidence: `report/evidence/csv/benders_300s_campaign.csv`, `report/evidence/docs/OVERNIGHT_TIMEOUT_AUDIT.md`.
3. OR-Library `pmed1`–`pmed40` fue verificada localmente contra óptimos oficiales en evidencia consolidada. Evidence: `report/evidence/csv/benders_300s_campaign.csv`, `report/evidence/csv/orlib_pmed16_smoke_300s.csv`, `report/evidence/csv/orlib_pmed17_pmed40_300s.csv`, `report/evidence/docs/BENDERS_300S_CAMPAIGN.md`, `report/ORLIB_PMED17_PMED40_EXTENSION_HANDOFF.md`.
4. TSPLIB `rl1304` fue ejecutada localmente en 9 valores de p y coincidió con óptimos de referencia usados por el wrapper. Evidence: `report/evidence/csv/benders_300s_campaign.csv`, `report/evidence/docs/BENDERS_300S_CAMPAIGN.md`.
5. `kroA100` fue resuelta localmente, pero se reporta como `OPTIMAL_NO_KNOWN`. Evidence: `report/evidence/csv/benders_300s_campaign.csv`.
6. El timeout de 300 segundos fue aplicado externamente por wrappers Python en las campañas auditadas. Evidence: `report/evidence/docs/OVERNIGHT_TIMEOUT_AUDIT.md`, wrapper scripts.
7. La línea base monolítica F1 resolvió 5 instancias con `OPTIMAL` y 0 timeouts. Evidence: `report/evidence/csv/monolithic_f1_300s.csv` on `exp/monolithic-baselines`, `report/evidence/docs/MONOLITHIC_F1_BASELINE_HANDOFF.md`.
8. En las cinco instancias de solape, Benders fue más rápido que F1 salvo `toy1`. Evidence: `report/evidence/docs/BENDERS_VS_MONOLITHIC_HANDOFF.md`.
9. Las trazas de Fase 1 fueron generadas para toy1, pmed1, pmed6 y rl1304 p=5. Evidence: `report/evidence/docs/GAP_TRACE_HANDOFF.md` on `exp/gap-trace-integration`.
10. La campaña sintética ejecutó 18 instancias hasta N=5000, sin timeouts. Evidence: `report/evidence/csv/synthetic_stress_300s.csv` on `exp/synthetic-stress`, `report/evidence/docs/SYNTHETIC_STRESS_HANDOFF.md`.
11. OR-Library pmed16 fue descargada desde fuente oficial, convertida y resuelta con `OPT_MATCH` objetivo 8162. Evidence: `report/evidence/csv/orlib_pmed16_smoke_300s.csv`, `report/evidence/docs/ORLIB_PMED16_SMOKE_HANDOFF.md`.
12. Zebra no fue ejecutado localmente. Evidence: `report/evidence/docs/WEB_SOURCE_AND_REPLICATION_FEASIBILITY_AUDIT.md`, `report/evidence/docs/PAPER_REPLICATION_MATRIX.md`.
13. PopStar no fue implementado localmente. Evidence: `report/evidence/docs/PAPER_REPLICATION_MATRIX.md`, `src/heuristic.h`.
14. Reduced-cost fixing y constraint reduction no fueron implementados. Evidence: `report/evidence/docs/PAPER_REPLICATION_MATRIX.md`.
15. OR-Library `pmed17`–`pmed40` fue ejecutada con 24/24 `OPT_MATCH` y 0 timeouts. Evidence: `report/evidence/csv/orlib_pmed17_pmed40_300s.csv`, `report/ORLIB_PMED17_PMED40_EXTENSION_HANDOFF.md`.

## FORBIDDEN OR UNSUPPORTED CLAIMS

1. “Nuestra implementación supera a Zebra.” Unsupported: Zebra no fue ejecutado localmente.
2. “Se replicó completamente el paper.” Unsupported: faltan Zebra, PopStar, reducciones, fixing, BIRCH/RW/ODM completos y huge TSPLIB.
3. “PopStar fue implementado.” False según matrix y código.
4. “Reduced-cost fixing fue implementado.” False según matrix.
5. “Constraint reduction fue implementado.” False según matrix.
6. “Se corrió campaña completa BIRCH.” Unsupported.
7. “Se corrió campaña completa RW grande.” Unsupported; solo `rw12` y sintéticos/generador.
8. “Se corrió ODM.” Unsupported; no parser/modelo de asignaciones prohibidas.
9. “Se corrió huge TSPLIB.” Unsupported.
10. “OR-Library pmed1–pmed40 se ejecutó en una única campaña homogénea.” Unsupported: la evidencia existe, pero está consolidada desde varias corridas controladas.
11. “Los tiempos son independientes de hardware.” Unsupported.
12. “Las instancias sintéticas prueban comportamiento general de todas las instancias euclidianas.” Unsupported.
13. “El baseline monolítico local equivale al benchmark Zebra o al C baseline del paper.” Unsupported.
14. “El gap Benders y el gap monolítico son la misma métrica.” Incorrecto; deben definirse por separado.
