# X1 — cuatro versiones: de atacar el síntoma a atacar la capacidad

Misma falla (B2 + D2), misma semilla, misma carga (20 req/s), fases 5 + 5 + 2 min.

| Versión | Corrida | Corrección del worker |
|---|---|---|
| 0. Sin corrección | `X1_20261108T163553Z` | — |
| 1. Corrección original | `X1-corr_20261108T223627Z` | retry + backoff + DLQ + breaker, **en serie** |
| 2. Worker paralelo | `X1-corr-worker-paralelo_20261108T225719Z` | + 25 llamadas en paralelo por lote. **Descartada como evidencia**: el host se congeló ~10 s al final del baseline (502/503 antes de activar la falla) |
| 3. Paralelo + breaker calibrado | `X1-corr-worker-paralelo-v2_20261108T231125Z` | + breaker a 20 fallos seguidos (con 5 se abría por los mensajes rechazados, con SAP vivo) |

## Resultados (fase de falla salvo donde se indica)

| Métrica | 0. Sin corrección | 1. Original | 3. Paralelo + breaker |
|---|---|---|---|
| POST p99 | 25.721 ms | 1.116 ms | **1.118 ms** |
| Errores | 24,8 % | 7,9 % | **7,8 %** |
| Lecturas p95 (listar) | 9.721 ms | 7,3 ms | **7,8 ms** |
| **Lag máximo del outbox** | 297 s | 294 s | **133 s** (−55 %) |
| **Pendientes máximos** | 3.095 | 3.900 | **1.608** (−59 % vs. 1) |
| Pendientes al final de la ventana | 0 | 713 | **~0** |
| **Recuperación total (API + outbox)** | no (lag > 10 s) | no | **9,8 s, cumple el SLO** |
| Eventos a la cola de muertos | — | 6 | 795 |

## Lectura

1. **La API ya estaba resuelta desde la versión 1** (bulkhead + `lock_timeout`): p99 −96 %, errores −68 %,
   lecturas aisladas. Las versiones 2 y 3 no la cambian.
2. **La versión 1 atacó el síntoma** (head-of-line blocking) pero no la capacidad: el lag no mejoró y, como
   la API ya dejaba pasar más órdenes, el backlog creció (+26 %).
3. **La versión 3 atacó la capacidad:** llamadas a SAP en paralelo y breaker calibrado. El lag máximo bajó a
   menos de la mitad y el sistema completo se recupera en 9,8 s después del kill switch (antes nunca dentro
   de la ventana).
4. **El breaker mal calibrado era otra falla de diseño:** contaba fallos seguidos y no distinguía "SAP rechaza
   este mensaje" (D2: 40 % de mensajes rechazados siempre) de "SAP está caído".
5. **Límite que queda:** durante la falla el lag sigue creciendo (~0,4 s/s) y no cumple el SLO de 10 s. Cada
   mensaje rechazado cuesta 3 intentos × 2 s de espera de SAP; con 25 llamadas en paralelo el worker hace
   ~12 llamadas/s y la falla exige ~25. Siguientes pasos: timeout más corto hacia SAP (cada rechazo hoy
   tarda 2 s), más concurrencia (el mock admite ~40) o menos intentos para errores que no son transitorios.
6. **Costo de negocio de la corrección:** 795 órdenes en la cola de muertos durante la falla. Ya no bloquean
   a las demás, pero hay que revisarlas y reenviarlas a mano.
