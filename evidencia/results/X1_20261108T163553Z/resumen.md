# Resultado X1_20261108T163553Z — Falla combinada B2 + D2

- Fallas: **B2** (FOR UPDATE 30 s cada 60 s sobre franjas del CEDI 5) + **D2** (ext-sap 503 en 40 % tras 2 s), activadas juntas a las 16:40:59 UTC; kill switch a las 16:45:59.
- Carga: k6 a 20 req/s, semilla fija; fases de 5 min de baseline, 5 min de falla y 2 min de recuperación.
- Nota: el runner falló al escribir este archivo (bug con la lista de fallas, ya corregido); se redactó a mano desde `resumen.json`, el log del runner y Prometheus.

| Fase | POST p50 / p95 / p99 (ms) | Lecturas p95 listar / precio (ms) | Errores | Lag outbox máx | Pendientes máx |
|---|---|---|---|---|---|
| Baseline | 6,9 / 13,8 / 27,4 | 7,5 / 8,5 | 0 % | 1,2 s | 12 |
| Falla B2+D2 | 11,4 / 9.813 / 25.721 | 9.721 / 9.783 | 24,8 % (1.487 × 503); picos 33 % en ventanas de 60 s | 297 s | 3.095 |
| Recuperación | 5,5 / 11,9 / 24,8 | 7,0 / 6,5 | 0 % | 303 s → 36 s | 0 al final |

## Predicción vs resultado

| Predicción | Resultado | ¿Acertó? |
|---|---|---|
| API como B2 solo: diente de sierra de 60 s, ~25 % de errores, p99 ≈ 25 s | p95 alterna ~12,5 s / ~15 ms cada 30 s; 24,8 % de errores; p99 25,7 s (B2 solo: 24,8 % y 25,7 s) | Sí |
| Outbox paralizado, lag ≈ 300 s | lag subió lineal 1 s/s hasta 297 s | Sí |
| Pendientes ≈ 3.000 (< 4.201 de D2) | 3.095 | Sí |
| Efecto aditivo, sin amplificación | Métricas de API idénticas a B2; lag idéntico a D2 | Sí |
| API se recupera < 3 s | errores 0 % en la primera ventana limpia; p95 9,9 ms a los 30 s | Sí |
| Outbox no se recupera en la ventana | **drenó los 3.095 eventos en ~2 min** (0 pendientes a las 16:48:30) | **No** |

## Hallazgos para la sustentación

1. **Cascada de B2 también a las lecturas:** listar y precio, que no tocan franjas, tuvieron p95 ~9,7 s: el pool compartido propaga el lock.
2. **Acoplamiento entre fallas por la cola:** los pendientes crecen en escalones; durante cada lock entran menos órdenes (B2 frena al productor), y entre locks suben ~550 en 30 s. B2 actúa como un limitador involuntario de la carga que D2 acumula.
3. **Señales disjuntas:** la tasa de error de la API solo ve B2; el lag y los logs del worker solo ven D2. Con un único panel de la API, D2 habría pasado inadvertido.
4. **Sorpresa:** a diferencia de D2 solo (1.216 sin drenar), aquí el outbox se vació. Con menos backlog (3.095 vs 4.201) y sin la falla, el worker drenó a ~25 eventos/s. Hipótesis: el evento envenenado quedó liberado por el kill switch y la capacidad neta bastó para el backlog menor. Falta confirmarlo repitiendo.
5. **El SLO de recuperación marca "no recuperado"** porque el lag no bajó de 10 s dentro de los 2 min, aunque la API ya estaba sana: recuperación de la API ≠ recuperación del sistema.
