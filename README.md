# pmedian-benders

Replicación en C de la descomposición de Benders eficiente para el **problema de las p-medianas (pMP)**, basada en:

> Duran-Mateluna, C., Ales, Z. & Elloumi, S. (2023). *An efficient Benders decomposition for the p-median problem*. European Journal of Operational Research, 308, 84–96.

Proyecto del curso **Optimización Computacional** (PUCV). El objetivo es construir un repositorio limpio, modular, documentado y reproducible que reproduzca la lógica central del paper y sirva de base para futuras optimizaciones de modelamiento y solver.

## Estado del proyecto

| Etapa | Descripción | Estado |
|-------|-------------|--------|
| 0 | Esqueleto, plan, instancia toy | en curso |
| 1 | Parser de instancias + distancias | pendiente |
| 2 | Evaluador fuerza bruta (oráculo) | pendiente |
| 3 | Matriz S (sitios ordenados) | pendiente |
| 4 | Separación (Alg. 1 y 2) | pendiente |
| 5 | Fase 1 (maestro LP + loop de cortes) | pendiente |
| 6 | Fase 2 (branch-and-Benders-cut) | pendiente |
| 7 | Generación de instancias + benchmark | pendiente |
| 8 | Análisis preliminar + informe | pendiente |

El plan completo y la hoja de ruta están en [`PLAN.md`](PLAN.md) (en inglés).
La teoría completa y las entregas del curso van en [`docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md`](docs/PMEDIAN_BENDERS_PROJECT_BRIEF.md) (en español, pendiente).

## Arquitectura (resumen)

- **Núcleo en C:** lectura de instancias, acceso a distancias `d(i,j)`, matriz S, algoritmo de separación O(NM), loop de Fase 1, heurística de redondeo, cotas y logging.
- **Motor:** API de C de **Gurobi** para resolver el maestro (LP en Fase 1; MIP + callback de lazy constraints en Fase 2).
- **Prototipo opcional en Python+Gurobi:** referencia legible de los callbacks y oráculo de correctitud sobre instancias pequeñas.

## Requisitos (preliminar)

- Compilador C (gcc/clang) y `make`.
- Gurobi con licencia académica activa (variable `GUROBI_HOME`).
- Python 3 (solo para scripts de generación/benchmark y prototipo).

## Uso (preliminar — se completará en Etapa 5)

```bash
# compilar
make

# ejecutar (modo a elección)
./pmedian instances/toy/toy1.pmp --p 2 --mode phase1
./pmedian instances/toy/toy1.pmp --p 2 --mode full
```

## Control de versiones

```bash
cd pmedian-benders
git init
git add .
git commit -m "Etapa 0: esqueleto, plan e instancia toy"
```

## Formato de instancias

Ver [`docs/INSTANCE_FORMAT.md`](docs/INSTANCE_FORMAT.md).
