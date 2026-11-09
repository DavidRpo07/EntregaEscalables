# Línea base E3 vs. E2 — `20261108T205729Z`

Referencia: informe del E2 (`lab/momento1/referencia_e2.yaml`). Objetivo E3 = 0,90 × E2. Mismo método de percentil que el informe en cada fila (Q1 exclusive; Q2–Q5 inclusive); la columna «otro método» es la misma medición con el otro.

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Objetivo E3 (ms) | E3 (ms) | E3/E2 | Cumple | Otro método (ms) |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.159 | 0.107 | 0.6 | sí | 0.134 |
| Q1 | base | frio | p95 | 0.252 | 0.227 | 0.127 | 0.5 | sí | 0.184 |
| Q1 | base | frio | p99 | 3.575 | 3.218 | 0.233 | 0.07 | sí | 0.258 |
| Q1 | base | caliente | p50 | 0.161 | 0.145 | 0.107 | 0.66 | sí | 0.13 |
| Q1 | base | caliente | p95 | 0.217 | 0.195 | 0.121 | 0.56 | sí | 0.241 |
| Q1 | base | caliente | p99 | 0.386 | 0.347 | 0.138 | 0.36 | sí | 0.322 |
| Q2 | base | frio | p50 | 0.226 | 0.203 | 0.144 | 0.64 | sí | 0.159 |
| Q2 | base | frio | p95 | 0.944 | 0.85 | 0.161 | 0.17 | sí | 0.179 |
| Q2 | base | frio | p99 | 1.605 | 1.445 | 0.176 | 0.11 | sí | 0.187 |
| Q2 | base | caliente | p50 | 0.312 | 0.281 | 0.247 | 0.79 | sí | 0.273 |
| Q2 | base | caliente | p95 | 1.97 | 1.773 | 0.527 | 0.27 | sí | 0.669 |
| Q2 | base | caliente | p99 | 10.389 | 9.35 | 0.642 | 0.06 | sí | 3.958 |
| Q3 | base | frio | p50 | 0.167 | 0.15 | 0.132 | 0.79 | sí | 0.146 |
| Q3 | base | frio | p95 | 0.249 | 0.224 | 0.143 | 0.57 | sí | 0.165 |
| Q3 | base | frio | p99 | 0.464 | 0.418 | 0.149 | 0.32 | sí | 0.174 |
| Q3 | base | caliente | p50 | 0.181 | 0.163 | 0.127 | 0.7 | sí | 0.157 |
| Q3 | base | caliente | p95 | 0.336 | 0.302 | 0.143 | 0.43 | sí | 0.198 |
| Q3 | base | caliente | p99 | 0.927 | 0.834 | 0.157 | 0.17 | sí | 0.368 |
| Q4 | antes_indice | frio | p50 | 34.217 | — | 35.62 | 1.04 | — | 35.62 |
| Q4 | antes_indice | frio | p95 | 35.41 | — | 36.878 | 1.04 | — | 36.942 |
| Q4 | antes_indice | frio | p99 | 39.323 | — | 37.278 | 0.95 | — | 37.307 |
| Q4 | antes_indice | caliente | p50 | 36.413 | — | 38.748 | 1.06 | — | 38.748 |
| Q4 | antes_indice | caliente | p95 | 40.786 | — | 43.501 | 1.07 | — | 43.769 |
| Q4 | antes_indice | caliente | p99 | 74.687 | — | 46.842 | 0.63 | — | 48.299 |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.322 | 0.226 | 0.63 | sí | 0.231 |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.377 | 0.275 | 0.66 | sí | 0.278 |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.392 | 0.295 | 0.68 | sí | 0.297 |
| Q4 | despues_indice | caliente | p50 | 2.839 | 2.555 | 1.847 | 0.65 | sí | 1.964 |
| Q4 | despues_indice | caliente | p95 | 9.334 | 8.401 | 6.937 | 0.74 | sí | 7.634 |
| Q4 | despues_indice | caliente | p99 | 14.481 | 13.033 | 8.519 | 0.59 | sí | 15.268 |
| Q5 | antes_indice | frio | p50 | 6.901 | — | 6.785 | 0.98 | — | 6.785 |
| Q5 | antes_indice | frio | p95 | 8.213 | — | 7.643 | 0.93 | — | 7.695 |
| Q5 | antes_indice | frio | p99 | 10.279 | — | 8.039 | 0.78 | — | 8.958 |
| Q5 | antes_indice | caliente | p50 | 6.994 | — | 6.842 | 0.98 | — | 6.842 |
| Q5 | antes_indice | caliente | p95 | 8.188 | — | 7.261 | 0.89 | — | 7.486 |
| Q5 | antes_indice | caliente | p99 | 9.346 | — | 7.621 | 0.82 | — | 7.703 |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.14 | 0.112 | 0.72 | sí | 0.127 |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.163 | 0.136 | 0.75 | sí | 0.168 |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.172 | 0.147 | 0.77 | sí | 0.215 |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.225 | 0.167 | 0.67 | sí | 0.246 |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.294 | 0.205 | 0.63 | sí | 0.4 |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.337 | 0.223 | 0.6 | sí | 0.46 |

## Fase 4 (5.000 órdenes, ruta del modulith; req/s = exitosas / duración)

| | E2 | Objetivo E3 | E3 | Cumple |
|---|---|---|---|---|
| Duración (s) | 3.6815 | ≤ 3.3134 | 1.4082 | sí |
| Throughput (req/s) | 413.69 | ≥ 459.66 | 1081.5 | |
| Exitosas | 1523 | | 1523 | |
