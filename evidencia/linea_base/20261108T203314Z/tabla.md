# Línea base E3 vs. E2 — `20261108T203314Z`

Referencia: informe del E2 (`lab/momento1/referencia_e2.yaml`). Objetivo E3 = 0,90 × E2. Mismo método de percentil que el informe en cada fila (Q1 exclusive; Q2–Q5 inclusive); la columna «otro método» es la misma medición con el otro.

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Objetivo E3 (ms) | E3 (ms) | E3/E2 | Cumple | Otro método (ms) |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.159 | 0.133 | 0.75 | sí | 0.163 |
| Q1 | base | frio | p95 | 0.252 | 0.227 | 0.155 | 0.62 | sí | 0.189 |
| Q1 | base | frio | p99 | 3.575 | 3.218 | 0.371 | 0.1 | sí | 0.222 |
| Q1 | base | caliente | p50 | 0.161 | 0.145 | 0.131 | 0.81 | sí | 0.146 |
| Q1 | base | caliente | p95 | 0.217 | 0.195 | 0.145 | 0.67 | sí | 0.167 |
| Q1 | base | caliente | p99 | 0.386 | 0.347 | 0.16 | 0.41 | sí | 0.179 |
| Q2 | base | frio | p50 | 0.226 | 0.203 | 0.174 | 0.77 | sí | 0.187 |
| Q2 | base | frio | p95 | 0.944 | 0.85 | 0.186 | 0.2 | sí | 0.203 |
| Q2 | base | frio | p99 | 1.605 | 1.445 | 0.193 | 0.12 | sí | 0.219 |
| Q2 | base | caliente | p50 | 0.312 | 0.281 | 0.214 | 0.69 | sí | 0.226 |
| Q2 | base | caliente | p95 | 1.97 | 1.773 | 0.443 | 0.22 | sí | 0.539 |
| Q2 | base | caliente | p99 | 10.389 | 9.35 | 0.557 | 0.05 | sí | 3.118 |
| Q3 | base | frio | p50 | 0.167 | 0.15 | 0.144 | 0.86 | sí | 0.144 |
| Q3 | base | frio | p95 | 0.249 | 0.224 | 0.157 | 0.63 | sí | 0.156 |
| Q3 | base | frio | p99 | 0.464 | 0.418 | 0.162 | 0.35 | sí | 0.17 |
| Q3 | base | caliente | p50 | 0.181 | 0.163 | 0.14 | 0.77 | sí | 0.159 |
| Q3 | base | caliente | p95 | 0.336 | 0.302 | 0.152 | 0.45 | sí | 0.19 |
| Q3 | base | caliente | p99 | 0.927 | 0.834 | 0.161 | 0.17 | sí | 0.712 |
| Q4 | antes_indice | frio | p50 | 34.217 | — | 40.508 | 1.18 | — | 40.508 |
| Q4 | antes_indice | frio | p95 | 35.41 | — | 50.273 | 1.42 | — | 50.507 |
| Q4 | antes_indice | frio | p99 | 39.323 | — | 56.176 | 1.43 | — | 56.708 |
| Q4 | antes_indice | caliente | p50 | 36.413 | — | 41.515 | 1.14 | — | 41.515 |
| Q4 | antes_indice | caliente | p95 | 40.786 | — | 47.244 | 1.16 | — | 47.531 |
| Q4 | antes_indice | caliente | p99 | 74.687 | — | 49.301 | 0.66 | — | 53.403 |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.322 | 0.224 | 0.63 | sí | 0.239 |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.377 | 0.286 | 0.68 | sí | 0.283 |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.392 | 0.324 | 0.74 | sí | 0.312 |
| Q4 | despues_indice | caliente | p50 | 2.839 | 2.555 | 1.902 | 0.67 | sí | 2.085 |
| Q4 | despues_indice | caliente | p95 | 9.334 | 8.401 | 7.055 | 0.76 | sí | 8.161 |
| Q4 | despues_indice | caliente | p99 | 14.481 | 13.033 | 9.209 | 0.64 | sí | 16.328 |
| Q5 | antes_indice | frio | p50 | 6.901 | — | 7.468 | 1.08 | — | 7.468 |
| Q5 | antes_indice | frio | p95 | 8.213 | — | 7.932 | 0.97 | — | 7.948 |
| Q5 | antes_indice | frio | p99 | 10.279 | — | 8.248 | 0.8 | — | 8.318 |
| Q5 | antes_indice | caliente | p50 | 6.994 | — | 7.507 | 1.07 | — | 7.507 |
| Q5 | antes_indice | caliente | p95 | 8.188 | — | 8.037 | 0.98 | — | 8.108 |
| Q5 | antes_indice | caliente | p99 | 9.346 | — | 8.216 | 0.88 | — | 8.218 |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.14 | 0.111 | 0.71 | sí | 0.125 |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.163 | 0.131 | 0.72 | sí | 0.164 |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.172 | 0.137 | 0.72 | sí | 0.176 |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.225 | 0.178 | 0.71 | sí | 0.246 |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.294 | 0.206 | 0.63 | sí | 0.395 |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.337 | 0.239 | 0.64 | sí | 0.474 |

## Fase 4 (5.000 órdenes, ruta del modulith; req/s = exitosas / duración)

| | E2 | Objetivo E3 | E3 | Cumple |
|---|---|---|---|---|
| Duración (s) | 3.6815 | ≤ 3.3134 | 1.3583 | sí |
| Throughput (req/s) | 413.69 | ≥ 459.66 | 1121.23 | |
| Exitosas | 1523 | | 1523 | |
