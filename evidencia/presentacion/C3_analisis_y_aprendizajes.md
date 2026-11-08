# Criterio 3 — Análisis de resultados y aprendizajes (20 pts)

Material para las diapositivas. Fuentes: informe E3 (secciones 5, 7 y 9), `evidencia/results/X1_*`,
`evidencia/optimizaciones/README.md` (pasos f y g).

---

## Diapositiva 1 — Hipótesis vs. resultado: dónde nos equivocamos y por qué

| ID | Qué predijimos | Qué pasó | Por qué nos equivocamos |
|---|---|---|---|
| A2 | Lecturas sin cambio | Lecturas p99 34 → 420 ms | Olvidamos que lecturas y escrituras **comparten el pool** |
| B1 | p50 de 2–3 s; las lecturas fallan menos | p50 20 s; lecturas fallan igual | Había **dos filas encadenadas** (hilos de uvicorn + pool), no una |
| B2 | ~40 % de errores promedio | 25 % (con picos de 94 %) | Las peticiones esperaban un hilo sin timeout y respondían 201 al liberarse el lock |
| C1 | p95 de 60–120 ms | **493 ms (4×)** | El **GIL** de Python deja un solo núcleo efectivo |
| C2 | Drena en ~30 s | ~95 s | Usamos la capacidad bruta del worker, no la neta (siguen entrando órdenes) |
| D1 | ~0,5 % de 502 | 0 | nginx resuelve por DNS y **reintentó** el único POST fallido |
| D2 | 40 % de eventos perdidos | 0 perdidos, **cola paralizada** | El worker reintenta en orden: **head-of-line blocking** |
| X1 | El outbox no drena en la ventana | Drenó en ~2 min | Menos backlog (B2 frenó la entrada) y la capacidad neta alcanzó |

Para decir: **"Tres predicciones fallaron por lo mismo: no modelamos los recursos compartidos ni las colas encadenadas."**

---

## Diapositiva 2 — Comportamientos inesperados que más aprendimos

1. **Una falla local se vuelve global** (B2): un lock en 1 de 5 CEDI tumbó el 25 % de todas las órdenes y subió las lecturas a ~10 s.
2. **Un solo mensaje paraliza la cola** (D2): un evento rechazado se reintentó 119 veces y bloqueó todo el outbox 4,5 min.
3. **La protección puede empeorar la falla** (B1): `max_fails=1` de nginx marcó las dos réplicas como caídas y subió el error a 89–100 %.
4. **La observabilidad también falla** (Jaeger): sin límite de memoria acumuló 6,8 GiB y terminó por OOM en plena corrida.
5. **Una optimización puede empeorar un caso** (Q2 caliente): las sentencias preparadas usan un plan genérico que es peor para los proveedores grandes (+14 a +20 %).
6. **El entorno cambia la medición 2×**: la misma tabla dio 9/30 con el Mac cargado y 30/30 en reposo, con 7 min de diferencia.

---

## Diapositiva 3 — Errores de diseño que encontramos (heredados del E2)

| Error | Consecuencia | Cómo lo vimos |
|---|---|---|
| **Pool único** para lecturas y escrituras | Cualquier lentitud en escritura contagia las lecturas | A2, B1, B2, X1 |
| **Sin timeouts** (pool 5 s, sin `lock_timeout`) | Las peticiones se cuelgan hasta 30–60 s en vez de fallar rápido | B1, B2 |
| El UPDATE de Q3 reservaba **todas las franjas del día** (5,4 por orden) | 5× más locks y capacidad logística agotada 5× más rápido | Reconstrucción del E2 |
| Validar el estado de la orden **después** de Q1–Q3 | 60 % de las órdenes hacían todo el trabajo para terminar en ROLLBACK | Fase 4: 2.988 rechazos tardíos |
| Worker **en serie** y sin cola de muertos | Head-of-line blocking; ~0,5 eventos/s con fallas frente a ~14/s que entran | D2 |

---

## Diapositiva 4 — Qué NO repetiríamos y qué haríamos diferente

| No lo repetiríamos | Lo haríamos así | Evidencia |
|---|---|---|
| Un pool de conexiones compartido por todo | **Bulkhead** desde el diseño: pools separados para lectura y escritura | B2: p99 de 25,7 s a 1,1 s |
| Dependencias sin timeout | **Timeout fijado contra el SLO** (uno de 200 ms no cumple un SLO de 100 ms) | A1 |
| Reintentar en orden sin límite | **Cola de mensajes muertos** + máximo de intentos | D2: el bloqueo se resolvió (8 eventos a muertos) |
| Corregir sin encontrar el cuello de botella | **Medir la capacidad primero**: en D2 el problema era el worker en serie, no los reintentos | D2 corregido: el lag no mejoró (312 s) |
| Observabilidad sin límites de recursos | **Límites de memoria y retención** en Jaeger desde el día 1 | OOM a las 6,5 h |
| Medir con el equipo ocupado | **Host en reposo, filas de control y mediana de 3** | 9/30 vs. 30/30 |
| Validar al final de la transacción | **Fail-fast**: validar lo barato primero | Fase 4: ×2,4 de throughput |
| Confiar en el promedio | **Percentiles y ventanas cortas** | B2: el 25 % promedio escondía picos de 94 % |

---

## Diapositiva 5 — Aprendizajes por eje

**Resiliencia**
- Los recursos compartidos son el riesgo principal: convierten fallas locales en globales.
- Fallar rápido es mejor que fallar lento (B1: de cuelgues de 60 s a respuestas en 2,6 s).
- Retry y breaker **no agregan capacidad** (D2).

**Escalabilidad**
- El bulkhead **redistribuye** capacidad, no la crea (A2: la escritura empeoró con 3 conexiones en vez de 5).
- Python con GIL: más hilos no dan más CPU (C1). Para escalar hacen falta réplicas o procesos.
- Casi toda la mejora de la Fase 4 vino de **no hacer trabajo inútil** (rechazar temprano), no de hacerlo más rápido.

**Observabilidad**
- En 6 de 8 fallas, la tasa de error de la API **no mostró nada**.
- Las trazas localizan; los logs explican; las métricas detectan. Hacen falta las tres.
- Tiene costo: +3 ms en el p95, el doble en el p99 y +17 % de CPU con trazas encendidas.
