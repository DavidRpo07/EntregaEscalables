# Tabla final: E2 vs. línea base E3 vs. final E3

Línea base E3: `evidencia/linea_base/20261017T034200Z` · Final E3: `evidencia/linea_base/20261017T044939Z` · E2: informe (`lab/momento1/referencia_e2.yaml`). Objetivo = 0,90 × E2. Mejora = (línea base − final) / línea base. Q4/Q5 «antes_indice» son solo referencia (sin objetivo).

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Línea base E3 (ms) | Final E3 (ms) | Objetivo (ms) | ¿Cumple? | Mejora vs. línea base |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.162 | 0.155 | 0.159 | sí | +4.3 % |
| Q1 | base | frio | p95 | 0.252 | 0.253 | 0.203 | 0.227 | sí | +19.8 % |
| Q1 | base | frio | p99 | 3.575 | 1.312 | 0.548 | 3.218 | sí | +58.2 % |
| Q1 | base | caliente | p50 | 0.161 | 0.16 | 0.137 | 0.145 | sí | +14.4 % |
| Q1 | base | caliente | p95 | 0.217 | 0.261 | 0.154 | 0.195 | sí | +41.0 % |
| Q1 | base | caliente | p99 | 0.386 | 0.405 | 0.204 | 0.347 | sí | +49.6 % |
| Q2 | base | frio | p50 | 0.226 | 0.238 | 0.18 | 0.203 | sí | +24.4 % |
| Q2 | base | frio | p95 | 0.944 | 0.373 | 0.254 | 0.85 | sí | +31.9 % |
| Q2 | base | frio | p99 | 1.605 | 0.453 | 0.269 | 1.445 | sí | +40.6 % |
| Q2 | base | caliente | p50 | 0.312 | 0.27 | 0.24 | 0.281 | sí | +11.1 % |
| Q2 | base | caliente | p95 | 1.97 | 1.009 | 0.517 | 1.773 | sí | +48.8 % |
| Q2 | base | caliente | p99 | 10.389 | 1.344 | 0.801 | 9.35 | sí | +40.4 % |
| Q3 | base | frio | p50 | 0.167 | 0.173 | 0.171 | 0.15 | **no** | +1.2 % |
| Q3 | base | frio | p95 | 0.249 | 0.235 | 0.497 | 0.224 | **no** | -111.5 % |
| Q3 | base | frio | p99 | 0.464 | 0.243 | 0.656 | 0.418 | **no** | -170.0 % |
| Q3 | base | caliente | p50 | 0.181 | 0.18 | 0.178 | 0.163 | **no** | +1.1 % |
| Q3 | base | caliente | p95 | 0.336 | 0.249 | 0.22 | 0.302 | sí | +11.6 % |
| Q3 | base | caliente | p99 | 0.927 | 0.277 | 0.504 | 0.834 | sí | -81.9 % |
| Q4 | antes_indice | frio | p50 | 34.217 | 57.859 | 42.626 | — | — | +26.3 % |
| Q4 | antes_indice | frio | p95 | 35.41 | 68.667 | 66.683 | — | — | +2.9 % |
| Q4 | antes_indice | frio | p99 | 39.323 | 73.489 | 101.036 | — | — | -37.5 % |
| Q4 | antes_indice | caliente | p50 | 36.413 | 60.961 | 44.314 | — | — | +27.3 % |
| Q4 | antes_indice | caliente | p95 | 40.786 | 105.042 | 51.348 | — | — | +51.1 % |
| Q4 | antes_indice | caliente | p99 | 74.687 | 181.888 | 60.556 | — | — | +66.7 % |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.362 | 0.356 | 0.322 | **no** | +1.7 % |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.418 | 0.417 | 0.377 | **no** | +0.2 % |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.464 | 0.43 | 0.392 | **no** | +7.3 % |
| Q4 | despues_indice | caliente | p50 | 2.839 | 3.407 | 2.545 | 2.555 | sí | +25.3 % |
| Q4 | despues_indice | caliente | p95 | 9.334 | 10.315 | 8.54 | 8.401 | **no** | +17.2 % |
| Q4 | despues_indice | caliente | p99 | 14.481 | 14.566 | 13.568 | 13.033 | **no** | +6.9 % |
| Q5 | antes_indice | frio | p50 | 6.901 | 13.167 | 7.693 | — | — | +41.6 % |
| Q5 | antes_indice | frio | p95 | 8.213 | 14.175 | 8.981 | — | — | +36.6 % |
| Q5 | antes_indice | frio | p99 | 10.279 | 16.21 | 10.257 | — | — | +36.7 % |
| Q5 | antes_indice | caliente | p50 | 6.994 | 11.038 | 8.023 | — | — | +27.3 % |
| Q5 | antes_indice | caliente | p95 | 8.188 | 12.963 | 11.188 | — | — | +13.7 % |
| Q5 | antes_indice | caliente | p99 | 9.346 | 13.87 | 11.797 | — | — | +14.9 % |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.193 | 0.13 | 0.14 | sí | +32.6 % |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.252 | 0.16 | 0.163 | sí | +36.5 % |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.273 | 0.164 | 0.172 | sí | +39.9 % |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.328 | 0.237 | 0.225 | **no** | +27.7 % |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.487 | 0.323 | 0.294 | **no** | +33.7 % |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.531 | 0.335 | 0.337 | sí | +36.9 % |

## Fase 4 (5.000 órdenes; req/s = exitosas / duración)

| Métrica | E2 | Línea base E3 | Final E3 | Objetivo | ¿Cumple? | Mejora vs. línea base |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 413.69 | 296.42 | 1059.87 | ≥ 459.66 | sí | +257.6 % |
| Duración (s) | 3.6815 | 5.1380 | 1.4370 | ≤ 3.3134 | sí | |
