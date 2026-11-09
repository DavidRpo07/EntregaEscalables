# X1 con corrección (bulkhead + worker) vs. X1 sin corrección

Misma falla (B2 + D2), misma semilla y misma carga. Correcciones activas toda la corrida (también en el baseline):
`bulkhead` (pool escritura 3 + lectura 2, `pool_timeout` 500 ms, `lock_timeout` 1 s) y `worker`
(3 intentos con backoff + jitter, cola de muertos, breaker hacia ext-sap).

| Fase de falla | Sin corrección (`X1_20261108T163553Z`) | Con corrección | Cambio |
|---|---|---|---|
| POST p50 / p95 / p99 | 11,4 / 9.813 / 25.721 ms | 8,4 / 1.010 / 1.116 ms | p99 **−96 %** |
| Errores (503) | 24,8 % (1.487) | **7,9 %** (474) | −68 % |
| Peor ventana de 60 s | 25,8 % | 9,0 % | |
| Lecturas p95 listar / precio | 9.721 / 9.783 ms | **7,3 / 6,7 ms** | aisladas por el bulkhead |
| Órdenes creadas (201) | 3.131 | 3.722 | +19 % |
| Lag máximo del outbox | 297 s | 294 s | **sin mejora** |
| Pendientes máximos | 3.095 | **3.900** | **+26 %** |
| Eventos a la cola de muertos | — | 6 | head-of-line resuelto |
| Recuperación API (cliente) | 0 s | 0 s | |
| Pendientes al final de la ventana | 0 | 713 (drenando) | |

## Lectura

1. **B2 queda contenida:** `lock_timeout` hace fallar rápido (≤ 1 s) solo a las órdenes que chocan con el lock y
   el bulkhead deja las lecturas en ~7 ms. Es el mismo resultado que B2 corregida sola (p99 1,1 s, 7,9 %): la
   combinación con D2 no cambia la corrección de B2.
2. **D2 no mejora el lag:** los 6 eventos rechazados se van a la cola de muertos (ya no hay head-of-line
   blocking), pero el worker procesa en serie y cada llamada fallida a ext-sap tarda 2 s: su capacidad con
   la falla está por debajo de los ~14 eventos/s que entran. Igual que D2 corregida sola: retry, DLQ y breaker
   no agregan capacidad.
3. **Interacción nueva entre las correcciones:** al corregir B2 se crean un 19 % más de órdenes, y cada una es
   un evento más en el outbox. **Arreglar la API le pasó más carga al consumidor que sigue degradado**
   (3.900 pendientes frente a 3.095). La corrección de un camino empeoró el síntoma del otro.
4. **Lo que faltaría:** paralelizar el worker o publicar por lotes (atacar la capacidad), que es la corrección
   que D2 señaló y no se implementó.
