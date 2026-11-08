# Criterio 4 — Corrección, re-experimentación y estado final (30 pts)

## Diapositiva 1 — X1 antes y después de corregir (medido)

Detalle: `evidencia/results/X1-corr_20261108T223627Z/analisis.md`.

| Fase de falla | Sin corrección | Con corrección |
|---|---|---|
| POST p99 | 25.721 ms | **1.116 ms** |
| Errores | 24,8 % | **7,9 %** |
| Lecturas p95 | ~9.700 ms | **~7 ms** |
| Lag outbox | 297 s | 294 s (sin mejora) |
| Pendientes | 3.095 | 3.900 (**empeora**) |

Para decir: **"La corrección de B2 funciona. La de D2 resuelve el bloqueo de la cola, pero no la capacidad.
Y al arreglar la API entran más órdenes, que van a un consumidor que sigue lento: una corrección le pasó la carga al otro camino."**

## Diapositiva 2 — Las correcciones y su justificación

| Falla | Corrección | Justificación | ¿Funcionó? |
|---|---|---|---|
| A1 | Timeout 200 ms + breaker + caché de precio | Sin timeout la falla es invisible y nada se protege | Cambia lentitud por errores (25,6 %) |
| A2 | Bulkhead lectura/escritura | Las lecturas no deben pagar por las escrituras lentas | Lecturas sí; escritura peor |
| B1 | Bulkhead + fail-fast del pool (500 ms) | Mejor fallar en 0,5 s que colgarse 60 s | Sí: p99 60 s → 2,6 s |
| B2 | Bulkhead + `lock_timeout` 1 s | Que falle solo quien choca con el lock | **Sí: p99 25,7 s → 1,1 s** |
| D2 | Retry + backoff + DLQ + breaker | Un mensaje malo no debe bloquear la cola | Bloqueo sí; lag no |
| **X1** | **Bulkhead + worker** | **Las correcciones de cada falla, juntas** | **API sí; outbox no** |

## Diapositiva 3 — Tabla E2 vs. E3 (latencia)

Archivo: `evidencia/linea_base/20261108T205729Z/tabla_final.md`. Objetivo = 0,90 × E2 (misma consulta, escenario y métrica).

| Consulta | Escenario | p50 E2 → E3 | p95 E2 → E3 | p99 E2 → E3 | Cumple |
|---|---|---|---|---|---|
| Q1 | frío | 0,177 → 0,107 | 0,252 → 0,127 | 3,575 → 0,233 | 3/3 |
| Q1 | caliente | 0,161 → 0,107 | 0,217 → 0,121 | 0,386 → 0,138 | 3/3 |
| Q2 | frío | 0,226 → 0,144 | 0,944 → 0,161 | 1,605 → 0,176 | 3/3 |
| Q2 | caliente | 0,312 → 0,247 | 1,970 → 0,527 | 10,389 → 0,642 | 3/3 |
| Q3 | frío | 0,167 → 0,132 | 0,249 → 0,143 | 0,464 → 0,149 | 3/3 |
| Q3 | caliente | 0,181 → 0,127 | 0,336 → 0,143 | 0,927 → 0,157 | 3/3 |
| Q4 | frío | 0,358 → 0,226 | 0,419 → 0,275 | 0,435 → 0,295 | 3/3 |
| Q4 | caliente | 2,839 → 1,847 | 9,334 → 6,937 | 14,481 → 8,519 | 3/3 |
| Q5 | frío | 0,156 → 0,112 | 0,181 → 0,136 | 0,191 → 0,147 | 3/3 |
| Q5 | caliente | 0,250 → 0,167 | 0,327 → 0,205 | 0,374 → 0,223 | 3/3 |

**30 de 30** (tiempos en ms; valores verificados contra `tabla_final.md`).

## Diapositiva 4 — Throughput (aparte: no es latencia)

| Carga | E2 | Objetivo | Final E3 |
|---|---|---|---|
| Fase 4 (órdenes exitosas/s) | 413,69 | ≥ 459,66 | **1.081,5** |

Para decir: **"Esto es throughput y lo mostramos aparte; la meta de latencia es la tabla anterior."**

## Diapositiva 5 — Qué causó cada mejora

| Mejora | Consultas | Evidencia (medición intercalada control vs. cambio) |
|---|---|---|
| a. Validar el estado antes de los módulos | Fase 4 | ×2,4 de throughput |
| b. UPDATE de Q3 a una sola franja | Fase 4 | Cupos consumidos 8.272 → 1.523 |
| c. Sentencias preparadas en la ruta de órdenes | Fase 4 | +8 % |
| d. Índices INCLUDE + VACUUM | Q4, Q5 | Q5 pasa a Index Only Scan |
| g. Sentencias preparadas | Q1–Q5 | Q1 −14 a −37 %; Q4 frío p50 −25 % |

Control: Q4 y Q5 *antes del índice* (mismo SQL que el E2) dieron 0,66–1,43 × E2. El entorno no favoreció la medición.

## Diapositiva 6 — Lo que no alcanzó o quedó pendiente

- **El lag de D2 no mejora** (ni sola ni en X1): falta paralelizar el worker o publicar por lotes.
- **Q2 caliente empeora con las sentencias preparadas** (+14 a +20 %, por el plan genérico); cumple igual por margen.
- **A1 corregida cambia lentitud por errores**, y el timeout de 200 ms no cumple el SLO de 100 ms.
- **Q1–Q3:** parte de la mejora frente al E2 también es entorno; la parte atribuible es la del paso g.
- **La medición depende del host:** con el Mac cargado, 9/30; en reposo, 30/30.

## Demo del estado final (en vivo, después de la demo del criterio 2)

```bash
make experimento-prueba ID=X1 CORRECCION=on      # ~90 s: baseline, falla, recuperación con correcciones
```
Mostrar en Grafana la fila **Correcciones**: bulkhead en uso por pool, `lock_timeout`/s, worker con reintentos y muertos.
