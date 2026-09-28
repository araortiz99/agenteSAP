# SAP Help MM Retrieval Benchmark

## Objetivo

Validar que la incorporación de SAP Help mejora la recuperación sin degradar la separación Standard/Internal.

| Caso | Consulta | Fuente esperada | Entidades | Incertidumbre |
|---|---|---|---|---|
| A | qué es el movimiento 551 | SAP_STANDARD | Movement Type 551 | release debe declararse |
| B | diferencia entre 551 y 552 | SAP_STANDARD | 551, 552 | no inferir equivalencia |
| C | qué hace ZMM_IM_0002 | INTERNAL | ZMM_IM_0002 | SAP Help no confirma Z |
| D | ZMM_IM_0002 utiliza 551 y qué dice SAP sobre 551 | SAP_STANDARD + INTERNAL | ZMM_IM_0002, 551 | Standard/Internal deben separarse |
| E | analizá ticket 31426 | INTERNAL | ticket 31426 | K1/K4 conflict |
| F | ticket 31426 + ZMM_IMX_0004 + SNC K1 | INTERNAL | ticket, Z object, process | no inventar root cause |
| G | comportamiento estándar vs implementación interna | SAP_STANDARD + INTERNAL | según consulta | difference requiere análisis |

## Criterios

- No permitir que stopwords dominen retrieval.
- Identificadores SAP cortos como MM, FI, SD, MIGO, MIRO y movimientos 551/552 no son stopwords.
- Versiones de SAP Help deben aparecer en provenance.
- SAP_STANDARD no puede satisfacer por sí solo una afirmación sobre configuración interna.
- El ticket 31426 debe conservar K1/K4 como conflicto no resuelto.
