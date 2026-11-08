# Línea base E3 vs. E2 — `20261108T202644Z`

Referencia: informe del E2 (`lab/momento1/referencia_e2.yaml`). Objetivo E3 = 0,90 × E2. Mismo método de percentil que el informe en cada fila (Q1 exclusive; Q2–Q5 inclusive); la columna «otro método» es la misma medición con el otro.

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Objetivo E3 (ms) | E3 (ms) | E3/E2 | Cumple | Otro método (ms) |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.159 | 0.222 | 1.25 | **no** | 0.298 |
| Q1 | base | frio | p95 | 0.252 | 0.227 | 0.347 | 1.38 | **no** | 1.849 |
| Q1 | base | frio | p99 | 3.575 | 3.218 | 1.424 | 0.4 | sí | 4.458 |
| Q1 | base | caliente | p50 | 0.161 | 0.145 | 0.233 | 1.45 | **no** | 0.402 |
| Q1 | base | caliente | p95 | 0.217 | 0.195 | 0.478 | 2.2 | **no** | 0.967 |
| Q1 | base | caliente | p99 | 0.386 | 0.347 | 1.484 | 3.84 | **no** | 1.604 |
| Q2 | base | frio | p50 | 0.226 | 0.203 | 0.293 | 1.3 | **no** | 0.308 |
| Q2 | base | frio | p95 | 0.944 | 0.85 | 0.321 | 0.34 | sí | 0.381 |
| Q2 | base | frio | p99 | 1.605 | 1.445 | 1.223 | 0.76 | sí | 0.686 |
| Q2 | base | caliente | p50 | 0.312 | 0.281 | 0.294 | 0.94 | **no** | 0.338 |
| Q2 | base | caliente | p95 | 1.97 | 1.773 | 0.566 | 0.29 | sí | 1.054 |
| Q2 | base | caliente | p99 | 10.389 | 9.35 | 1.213 | 0.12 | sí | 4.152 |
| Q3 | base | frio | p50 | 0.167 | 0.15 | 0.247 | 1.48 | **no** | 0.256 |
| Q3 | base | frio | p95 | 0.249 | 0.224 | 0.323 | 1.3 | **no** | 0.288 |
| Q3 | base | frio | p99 | 0.464 | 0.418 | 1.478 | 3.19 | **no** | 0.327 |
| Q3 | base | caliente | p50 | 0.181 | 0.163 | 0.245 | 1.35 | **no** | 0.258 |
| Q3 | base | caliente | p95 | 0.336 | 0.302 | 0.36 | 1.07 | **no** | 0.498 |
| Q3 | base | caliente | p99 | 0.927 | 0.834 | 1.383 | 1.49 | **no** | 1.363 |
| Q4 | antes_indice | frio | p50 | 34.217 | — | 41.552 | 1.21 | — | 41.552 |
| Q4 | antes_indice | frio | p95 | 35.41 | — | 46.183 | 1.3 | — | 46.451 |
| Q4 | antes_indice | frio | p99 | 39.323 | — | 64.56 | 1.64 | — | 106.453 |
| Q4 | antes_indice | caliente | p50 | 36.413 | — | 43.644 | 1.2 | — | 43.644 |
| Q4 | antes_indice | caliente | p95 | 40.786 | — | 49.812 | 1.22 | — | 49.993 |
| Q4 | antes_indice | caliente | p99 | 74.687 | — | 51.108 | 0.68 | — | 54.438 |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.322 | 0.323 | 0.9 | **no** | 0.277 |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.377 | 0.382 | 0.91 | **no** | 0.509 |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.392 | 1.008 | 2.32 | **no** | 1.498 |
| Q4 | despues_indice | caliente | p50 | 2.839 | 2.555 | 2.205 | 0.78 | sí | 2.333 |
| Q4 | despues_indice | caliente | p95 | 9.334 | 8.401 | 7.888 | 0.85 | sí | 8.595 |
| Q4 | despues_indice | caliente | p99 | 14.481 | 13.033 | 10.371 | 0.72 | sí | 24.473 |
| Q5 | antes_indice | frio | p50 | 6.901 | — | 7.931 | 1.15 | — | 7.931 |
| Q5 | antes_indice | frio | p95 | 8.213 | — | 9.154 | 1.11 | — | 9.249 |
| Q5 | antes_indice | frio | p99 | 10.279 | — | 10.061 | 0.98 | — | 10.24 |
| Q5 | antes_indice | caliente | p50 | 6.994 | — | 8.601 | 1.23 | — | 8.601 |
| Q5 | antes_indice | caliente | p95 | 8.188 | — | 13.656 | 1.67 | — | 14.353 |
| Q5 | antes_indice | caliente | p99 | 9.346 | — | 17.631 | 1.89 | — | 17.734 |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.14 | 0.198 | 1.27 | **no** | 0.219 |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.163 | 0.319 | 1.76 | **no** | 1.126 |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.172 | 1.025 | 5.37 | **no** | 2.106 |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.225 | 0.322 | 1.29 | **no** | 0.334 |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.294 | 0.456 | 1.39 | **no** | 0.707 |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.337 | 1.296 | 3.47 | **no** | 1.448 |

## Fase 4 (5.000 órdenes, ruta del modulith; req/s = exitosas / duración)

| | E2 | Objetivo E3 | E3 | Cumple |
|---|---|---|---|---|
| Duración (s) | 3.6815 | ≤ 3.3134 | 3.0786 | sí |
| Throughput (req/s) | 413.69 | ≥ 459.66 | 494.71 | |
| Exitosas | 1523 | | 1523 | |
