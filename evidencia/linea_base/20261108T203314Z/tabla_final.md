# Tabla final: E2 vs. línea base E3 vs. final E3

Línea base E3: `evidencia/linea_base/20261017T034200Z` · Final E3: `evidencia/linea_base/20261108T203314Z` · E2: informe (`lab/momento1/referencia_e2.yaml`). Objetivo = 0,90 × E2. Mejora = (línea base − final) / línea base. Q4/Q5 «antes_indice» son solo referencia (sin objetivo).

| Consulta | Fase | Escenario | Métrica | E2 (ms) | Línea base E3 (ms) | Final E3 (ms) | Objetivo (ms) | ¿Cumple? | Mejora vs. línea base |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | base | frio | p50 | 0.177 | 0.162 | 0.133 | 0.159 | sí | +17.9 % |
| Q1 | base | frio | p95 | 0.252 | 0.253 | 0.155 | 0.227 | sí | +38.7 % |
| Q1 | base | frio | p99 | 3.575 | 1.312 | 0.371 | 3.218 | sí | +71.7 % |
| Q1 | base | caliente | p50 | 0.161 | 0.16 | 0.131 | 0.145 | sí | +18.1 % |
| Q1 | base | caliente | p95 | 0.217 | 0.261 | 0.145 | 0.195 | sí | +44.4 % |
| Q1 | base | caliente | p99 | 0.386 | 0.405 | 0.16 | 0.347 | sí | +60.5 % |
| Q2 | base | frio | p50 | 0.226 | 0.238 | 0.174 | 0.203 | sí | +26.9 % |
| Q2 | base | frio | p95 | 0.944 | 0.373 | 0.186 | 0.85 | sí | +50.1 % |
| Q2 | base | frio | p99 | 1.605 | 0.453 | 0.193 | 1.445 | sí | +57.4 % |
| Q2 | base | caliente | p50 | 0.312 | 0.27 | 0.214 | 0.281 | sí | +20.7 % |
| Q2 | base | caliente | p95 | 1.97 | 1.009 | 0.443 | 1.773 | sí | +56.1 % |
| Q2 | base | caliente | p99 | 10.389 | 1.344 | 0.557 | 9.35 | sí | +58.6 % |
| Q3 | base | frio | p50 | 0.167 | 0.173 | 0.144 | 0.15 | sí | +16.8 % |
| Q3 | base | frio | p95 | 0.249 | 0.235 | 0.157 | 0.224 | sí | +33.2 % |
| Q3 | base | frio | p99 | 0.464 | 0.243 | 0.162 | 0.418 | sí | +33.3 % |
| Q3 | base | caliente | p50 | 0.181 | 0.18 | 0.14 | 0.163 | sí | +22.2 % |
| Q3 | base | caliente | p95 | 0.336 | 0.249 | 0.152 | 0.302 | sí | +39.0 % |
| Q3 | base | caliente | p99 | 0.927 | 0.277 | 0.161 | 0.834 | sí | +41.9 % |
| Q4 | antes_indice | frio | p50 | 34.217 | 57.859 | 40.508 | — | — | +30.0 % |
| Q4 | antes_indice | frio | p95 | 35.41 | 68.667 | 50.273 | — | — | +26.8 % |
| Q4 | antes_indice | frio | p99 | 39.323 | 73.489 | 56.176 | — | — | +23.6 % |
| Q4 | antes_indice | caliente | p50 | 36.413 | 60.961 | 41.515 | — | — | +31.9 % |
| Q4 | antes_indice | caliente | p95 | 40.786 | 105.042 | 47.244 | — | — | +55.0 % |
| Q4 | antes_indice | caliente | p99 | 74.687 | 181.888 | 49.301 | — | — | +72.9 % |
| Q4 | despues_indice | frio | p50 | 0.358 | 0.362 | 0.224 | 0.322 | sí | +38.1 % |
| Q4 | despues_indice | frio | p95 | 0.419 | 0.418 | 0.286 | 0.377 | sí | +31.6 % |
| Q4 | despues_indice | frio | p99 | 0.435 | 0.464 | 0.324 | 0.392 | sí | +30.2 % |
| Q4 | despues_indice | caliente | p50 | 2.839 | 3.407 | 1.902 | 2.555 | sí | +44.2 % |
| Q4 | despues_indice | caliente | p95 | 9.334 | 10.315 | 7.055 | 8.401 | sí | +31.6 % |
| Q4 | despues_indice | caliente | p99 | 14.481 | 14.566 | 9.209 | 13.033 | sí | +36.8 % |
| Q5 | antes_indice | frio | p50 | 6.901 | 13.167 | 7.468 | — | — | +43.3 % |
| Q5 | antes_indice | frio | p95 | 8.213 | 14.175 | 7.932 | — | — | +44.0 % |
| Q5 | antes_indice | frio | p99 | 10.279 | 16.21 | 8.248 | — | — | +49.1 % |
| Q5 | antes_indice | caliente | p50 | 6.994 | 11.038 | 7.507 | — | — | +32.0 % |
| Q5 | antes_indice | caliente | p95 | 8.188 | 12.963 | 8.037 | — | — | +38.0 % |
| Q5 | antes_indice | caliente | p99 | 9.346 | 13.87 | 8.216 | — | — | +40.8 % |
| Q5 | despues_indice | frio | p50 | 0.156 | 0.193 | 0.111 | 0.14 | sí | +42.5 % |
| Q5 | despues_indice | frio | p95 | 0.181 | 0.252 | 0.131 | 0.163 | sí | +48.0 % |
| Q5 | despues_indice | frio | p99 | 0.191 | 0.273 | 0.137 | 0.172 | sí | +49.8 % |
| Q5 | despues_indice | caliente | p50 | 0.25 | 0.328 | 0.178 | 0.225 | sí | +45.7 % |
| Q5 | despues_indice | caliente | p95 | 0.327 | 0.487 | 0.206 | 0.294 | sí | +57.7 % |
| Q5 | despues_indice | caliente | p99 | 0.374 | 0.531 | 0.239 | 0.337 | sí | +55.0 % |

## Fase 4 (5.000 órdenes; req/s = exitosas / duración)

| Métrica | E2 | Línea base E3 | Final E3 | Objetivo | ¿Cumple? | Mejora vs. línea base |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 413.69 | 296.42 | 1121.23 | ≥ 459.66 | sí | +278.3 % |
| Duración (s) | 3.6815 | 5.1380 | 1.3583 | ≤ 3.3134 | sí | |
