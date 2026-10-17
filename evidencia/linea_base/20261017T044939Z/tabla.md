# Línea base E3 vs. E2 — `20261017T044939Z`

Referencia: informe del E2 (`lab/momento1/referencia_e2.yaml`). Objetivo E3 = 0,90 × E2. Mismo método de percentil que el informe en cada fila (Q1 exclusive; Q2–Q5 inclusive); la columna «otro método» es la misma medición con el otro.

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Objetivo E3 (ms) | E3 (ms) | E3/E2 | Cumple | Otro método (ms) |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.159 | 0.155 | 0.88 | sí | 0.165 |
| Q1 | base | frio | p95 | 0.252 | 0.227 | 0.203 | 0.81 | sí | 0.209 |
| Q1 | base | frio | p99 | 3.575 | 3.218 | 0.548 | 0.15 | sí | 0.258 |
| Q1 | base | caliente | p50 | 0.161 | 0.145 | 0.137 | 0.85 | sí | 0.158 |
| Q1 | base | caliente | p95 | 0.217 | 0.195 | 0.154 | 0.71 | sí | 0.184 |
| Q1 | base | caliente | p99 | 0.386 | 0.347 | 0.204 | 0.53 | sí | 0.198 |
| Q2 | base | frio | p50 | 0.226 | 0.203 | 0.18 | 0.8 | sí | 0.211 |
| Q2 | base | frio | p95 | 0.944 | 0.85 | 0.254 | 0.27 | sí | 0.24 |
| Q2 | base | frio | p99 | 1.605 | 1.445 | 0.269 | 0.17 | sí | 0.504 |
| Q2 | base | caliente | p50 | 0.312 | 0.281 | 0.24 | 0.77 | sí | 0.275 |
| Q2 | base | caliente | p95 | 1.97 | 1.773 | 0.517 | 0.26 | sí | 0.692 |
| Q2 | base | caliente | p99 | 10.389 | 9.35 | 0.801 | 0.08 | sí | 3.594 |
| Q3 | base | frio | p50 | 0.167 | 0.15 | 0.171 | 1.02 | **no** | 0.163 |
| Q3 | base | frio | p95 | 0.249 | 0.224 | 0.497 | 2.0 | **no** | 0.182 |
| Q3 | base | frio | p99 | 0.464 | 0.418 | 0.656 | 1.41 | **no** | 0.197 |
| Q3 | base | caliente | p50 | 0.181 | 0.163 | 0.178 | 0.98 | **no** | 0.168 |
| Q3 | base | caliente | p95 | 0.336 | 0.302 | 0.22 | 0.65 | sí | 0.195 |
| Q3 | base | caliente | p99 | 0.927 | 0.834 | 0.504 | 0.54 | sí | 0.965 |
| Q4 | antes_indice | frio | p50 | 34.217 | — | 42.626 | 1.25 | — | 42.626 |
| Q4 | antes_indice | frio | p95 | 35.41 | — | 66.683 | 1.88 | — | 68.463 |
| Q4 | antes_indice | frio | p99 | 39.323 | — | 101.036 | 2.57 | — | 146.251 |
| Q4 | antes_indice | caliente | p50 | 36.413 | — | 44.314 | 1.22 | — | 44.314 |
| Q4 | antes_indice | caliente | p95 | 40.786 | — | 51.348 | 1.26 | — | 52.578 |
| Q4 | antes_indice | caliente | p99 | 74.687 | — | 60.556 | 0.81 | — | 111.469 |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.322 | 0.356 | 0.99 | **no** | 0.325 |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.377 | 0.417 | 1.0 | **no** | 0.387 |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.392 | 0.43 | 0.99 | **no** | 0.401 |
| Q4 | despues_indice | caliente | p50 | 2.839 | 2.555 | 2.545 | 0.9 | sí | 2.382 |
| Q4 | despues_indice | caliente | p95 | 9.334 | 8.401 | 8.54 | 0.91 | **no** | 8.384 |
| Q4 | despues_indice | caliente | p99 | 14.481 | 13.033 | 13.568 | 0.94 | **no** | 20.828 |
| Q5 | antes_indice | frio | p50 | 6.901 | — | 7.693 | 1.11 | — | 7.693 |
| Q5 | antes_indice | frio | p95 | 8.213 | — | 8.981 | 1.09 | — | 9.088 |
| Q5 | antes_indice | frio | p99 | 10.279 | — | 10.257 | 1.0 | — | 10.923 |
| Q5 | antes_indice | caliente | p50 | 6.994 | — | 8.023 | 1.15 | — | 8.023 |
| Q5 | antes_indice | caliente | p95 | 8.188 | — | 11.188 | 1.37 | — | 11.325 |
| Q5 | antes_indice | caliente | p99 | 9.346 | — | 11.797 | 1.26 | — | 12.072 |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.14 | 0.13 | 0.83 | sí | 0.162 |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.163 | 0.16 | 0.88 | sí | 0.197 |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.172 | 0.164 | 0.86 | sí | 0.236 |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.225 | 0.237 | 0.95 | **no** | 0.275 |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.294 | 0.323 | 0.99 | **no** | 0.391 |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.337 | 0.335 | 0.9 | sí | 0.545 |

## Fase 4 (5.000 órdenes, ruta del modulith; req/s = exitosas / duración)

| | E2 | Objetivo E3 | E3 | Cumple |
|---|---|---|---|---|
| Duración (s) | 3.6815 | ≤ 3.3134 | 1.4370 | sí |
| Throughput (req/s) | 413.69 | ≥ 459.66 | 1059.87 | |
| Exitosas | 1523 | | 1523 | |
