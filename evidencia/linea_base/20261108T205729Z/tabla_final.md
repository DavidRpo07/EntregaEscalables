# Tabla final: E2 vs. línea base E3 vs. final E3

Línea base E3: `evidencia/linea_base/20261017T034200Z` · Final E3: `evidencia/linea_base/20261108T205729Z` · E2: informe (`lab/momento1/referencia_e2.yaml`). Objetivo = 0,90 × E2. Mejora = (línea base − final) / línea base. Q4/Q5 «antes_indice» son solo referencia (sin objetivo).

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Línea base E3 (ms) | Final E3 (ms) | Objetivo (ms) | ¿Cumple? | Mejora vs. línea base |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.162 | 0.107 | 0.159 | sí | +34.0 % |
| Q1 | base | frio | p95 | 0.252 | 0.253 | 0.127 | 0.227 | sí | +49.8 % |
| Q1 | base | frio | p99 | 3.575 | 1.312 | 0.233 | 3.218 | sí | +82.2 % |
| Q1 | base | caliente | p50 | 0.161 | 0.16 | 0.107 | 0.145 | sí | +33.1 % |
| Q1 | base | caliente | p95 | 0.217 | 0.261 | 0.121 | 0.195 | sí | +53.6 % |
| Q1 | base | caliente | p99 | 0.386 | 0.405 | 0.138 | 0.347 | sí | +65.9 % |
| Q2 | base | frio | p50 | 0.226 | 0.238 | 0.144 | 0.203 | sí | +39.5 % |
| Q2 | base | frio | p95 | 0.944 | 0.373 | 0.161 | 0.85 | sí | +56.8 % |
| Q2 | base | frio | p99 | 1.605 | 0.453 | 0.176 | 1.445 | sí | +61.1 % |
| Q2 | base | caliente | p50 | 0.312 | 0.27 | 0.247 | 0.281 | sí | +8.5 % |
| Q2 | base | caliente | p95 | 1.97 | 1.009 | 0.527 | 1.773 | sí | +47.8 % |
| Q2 | base | caliente | p99 | 10.389 | 1.344 | 0.642 | 9.35 | sí | +52.2 % |
| Q3 | base | frio | p50 | 0.167 | 0.173 | 0.132 | 0.15 | sí | +23.7 % |
| Q3 | base | frio | p95 | 0.249 | 0.235 | 0.143 | 0.224 | sí | +39.1 % |
| Q3 | base | frio | p99 | 0.464 | 0.243 | 0.149 | 0.418 | sí | +38.7 % |
| Q3 | base | caliente | p50 | 0.181 | 0.18 | 0.127 | 0.163 | sí | +29.4 % |
| Q3 | base | caliente | p95 | 0.336 | 0.249 | 0.143 | 0.302 | sí | +42.6 % |
| Q3 | base | caliente | p99 | 0.927 | 0.277 | 0.157 | 0.834 | sí | +43.3 % |
| Q4 | antes_indice | frio | p50 | 34.217 | 57.859 | 35.62 | — | — | +38.4 % |
| Q4 | antes_indice | frio | p95 | 35.41 | 68.667 | 36.878 | — | — | +46.3 % |
| Q4 | antes_indice | frio | p99 | 39.323 | 73.489 | 37.278 | — | — | +49.3 % |
| Q4 | antes_indice | caliente | p50 | 36.413 | 60.961 | 38.748 | — | — | +36.4 % |
| Q4 | antes_indice | caliente | p95 | 40.786 | 105.042 | 43.501 | — | — | +58.6 % |
| Q4 | antes_indice | caliente | p99 | 74.687 | 181.888 | 46.842 | — | — | +74.2 % |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.362 | 0.226 | 0.322 | sí | +37.6 % |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.418 | 0.275 | 0.377 | sí | +34.2 % |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.464 | 0.295 | 0.392 | sí | +36.4 % |
| Q4 | despues_indice | caliente | p50 | 2.839 | 3.407 | 1.847 | 2.555 | sí | +45.8 % |
| Q4 | despues_indice | caliente | p95 | 9.334 | 10.315 | 6.937 | 8.401 | sí | +32.7 % |
| Q4 | despues_indice | caliente | p99 | 14.481 | 14.566 | 8.519 | 13.033 | sí | +41.5 % |
| Q5 | antes_indice | frio | p50 | 6.901 | 13.167 | 6.785 | — | — | +48.5 % |
| Q5 | antes_indice | frio | p95 | 8.213 | 14.175 | 7.643 | — | — | +46.1 % |
| Q5 | antes_indice | frio | p99 | 10.279 | 16.21 | 8.039 | — | — | +50.4 % |
| Q5 | antes_indice | caliente | p50 | 6.994 | 11.038 | 6.842 | — | — | +38.0 % |
| Q5 | antes_indice | caliente | p95 | 8.188 | 12.963 | 7.261 | — | — | +44.0 % |
| Q5 | antes_indice | caliente | p99 | 9.346 | 13.87 | 7.621 | — | — | +45.1 % |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.193 | 0.112 | 0.14 | sí | +42.0 % |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.252 | 0.136 | 0.163 | sí | +46.0 % |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.273 | 0.147 | 0.172 | sí | +46.2 % |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.328 | 0.167 | 0.225 | sí | +49.1 % |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.487 | 0.205 | 0.294 | sí | +57.9 % |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.531 | 0.223 | 0.337 | sí | +58.0 % |

## Fase 4 (5.000 órdenes; req/s = exitosas / duración)

| Métrica | E2 | Línea base E3 | Final E3 | Objetivo | ¿Cumple? | Mejora vs. línea base |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 413.69 | 296.42 | 1081.5 | ≥ 459.66 | sí | +264.9 % |
| Duración (s) | 3.6815 | 5.1380 | 1.4082 | ≤ 3.3134 | sí | |
