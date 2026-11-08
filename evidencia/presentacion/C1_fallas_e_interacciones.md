# Criterio 1 — Las ocho fallas, cómo se combinan y cómo se observan (25 pts)

Material para las diapositivas. Fuente de cada número: informe E3 (secciones 4–6) y corridas en `evidencia/results/`.
**Medido** = salió de una corrida; **inferido** = se deduce de la arquitectura y de las corridas individuales, sin corrida combinada propia.

---

## Diapositiva 1 — Mapa del sistema y dónde pega cada falla

```
                 k6 (20 req/s)
                      │
                   nginx ──────────────── D1 (cae api-2)
                 ┌────┴────┐
              api-1      api-2 ─────────── C1 (CPU 90 % en api-1)
                 │  pool compartido (5 conexiones/réplica) ◄── B1 (+300 ms por consulta)
   POST /ordenes │
   Q1 Proveedores → Q2 Catálogo → Q3 Logística → INSERT orden + outbox
                    ▲ A1 (+800 ms)   ▲ A2 (jitter)    ▲ B2 (lock 30 s en franjas CEDI 5)
                 │
            PostgreSQL ── outbox_evento ── worker ── ext-sap (SAP)
                                             ▲ C2 (pausa)   ▲ D2 (503 40 % tras 2 s)
```

Idea para decir: **hay tres recursos compartidos (el pool de conexiones, las réplicas detrás de nginx y la cola del outbox) y cada falla golpea uno de ellos.** Eso decide cómo se combinan.

---

## Diapositiva 2 — Las ocho fallas por familia (medido)

| ID | Familia | Falla | Efecto medido | Se propaga a… |
|---|---|---|---|---|
| A1 | Latencia | +800 ms en Catálogo, 30 % | p95 811 ms, **0 % errores** | Nada más; invisible para alertas por error |
| A2 | Latencia | Jitter lognormal en Logística | p99 2,38 s; **lecturas p99 34 → 420 ms** | Lecturas, vía pool compartido |
| B1 | Base de datos | Pool agotado (+300 ms/consulta) | **70 % errores**, p50 20 s | Todo: nginx marcó ambas réplicas caídas |
| B2 | Base de datos | `FOR UPDATE` 30 s cada 60 s, CEDI 5 | 25 % errores en **todos** los CEDI, picos 94 % | Otros CEDI y lecturas, vía pool |
| C1 | Degradación | CPU 90 % en api-1 | p95 api-1 493 ms (4× lo previsto, GIL) | Solo api-1; el p95 global lo esconde |
| C2 | Degradación | Worker pausado 3 min | API sin cambio; lag 178 s | Solo la cola; silenciosa |
| D1 | Disponibilidad | Caída de api-2 | **0 errores**; api-1 absorbe | Nada; nginx reintentó |
| D2 | Disponibilidad | SAP 503 en 40 % tras 2 s | API sin cambio; lag 300 s; **un evento bloquea la cola** | Toda la cola (head-of-line) |

Patrón: **seis de ocho no generan errores visibles en la API** (A1, A2, C1, C2, D1, D2): solo B1 y B2 suben la tasa de error. Por eso la observabilidad no puede ser solo "tasa de error".

---

## Diapositiva 3 — Cómo se combinan: interacciones por recurso compartido

| Recurso compartido | Fallas | Tipo de interacción | Base |
|---|---|---|---|
| **Pool de conexiones** de la API | A1, A2, B1, B2 | **Se amplifican**: todas retienen conexiones más tiempo; juntas agotan el pool antes y lo mantienen agotado. Una falla local se vuelve global | Medido por separado (A2 y B2 contagian lecturas; B1 tumba todo); combinación **inferida** |
| **Réplicas** detrás de nginx | C1, D1 | **Se amplifican**: D1 sola no se nota porque queda api-1; con C1 activa, la única réplica que queda está degradada → se pierde la redundancia | Inferido de C1 y D1 por separado |
| **Cola del outbox** | C2, D2 | **Redundantes**: con el worker pausado, el 503 de SAP no importa hasta que se reanuda; al reanudar, D2 bloquea el drenaje | Inferido |
| **Escritura → cola** (entre recursos) | B2 → D2 | **Aditivas, acopladas por la cola**: B2 frena las órdenes que entran y deja menos backlog para D2 | **Medido en X1** |

Para decir: **"Las fallas que comparten recurso se amplifican; las que viven en caminos distintos se suman. Lo probamos con X1, que junta dos caminos distintos."**

---

## Diapositiva 4 — La combinación ejecutada: X1 = B2 + D2 (medido)

Corrida completa: `evidencia/results/X1_20261108T163553Z/resumen.md` (predicción versionada antes de correr).

| Fase | POST p95 / p99 | Errores | Lag outbox | Pendientes |
|---|---|---|---|---|
| Baseline | 13,8 / 27,4 ms | 0 % | 1 s | 12 |
| **B2 + D2** | **9.813 / 25.721 ms** | **24,8 %** | **297 s** | **3.095** |
| Recuperación | 11,9 / 24,8 ms | 0 % | 303 → 36 s | 0 |

Predicción vs. resultado: **5 de 6 aciertos**.
- ✅ API igual que B2 sola (24,8 % y p99 25,7 s, igual que B2).
- ✅ Outbox paralizado como D2 sola (lag de ~300 s).
- ✅ ~3.000 pendientes (menos que los 4.201 de D2, porque B2 rechaza ~25 % de las órdenes).
- ✅ Efecto aditivo, sin amplificación.
- ✅ API recuperada en < 3 s.
- ❌ Dijimos que el outbox no drenaría en la ventana: **drenó en ~2 min**.

Cascada observada: **las lecturas (listar, precio), que no tocan franjas, subieron a p95 ~9,7 s.**

---

## Diapositiva 5 — Correlacionar métricas, logs y trazas (causa → consecuencia)

Recorrido de diagnóstico en X1 (capturas en `evidencia/demo/`):

| Pregunta | Señal | Lo que muestra |
|---|---|---|
| ¿Hay un problema? | **Métrica**: % 5xx y p99 (Grafana) | 25 % de errores, p99 27 s, diente de sierra de 60 s |
| ¿Es una réplica? | **Métrica**: p95 por réplica | No: ambas fallan igual |
| ¿Dónde se atasca? | **Métrica**: pool en uso / esperando | 5/5 conexiones, ~200 peticiones en espera |
| ¿Por qué? | **Métrica**: locks de PostgreSQL | Locks con el mismo ciclo de 60 s → B2 |
| ¿Qué siente una orden? | **Traza** (Jaeger) | Petición de 5 s: el trabajo real son ~7 ms; los otros ~4,9 s esperó turno |
| ¿Hay algo más roto? | **Métrica**: lag del outbox, publicados | Lag crece 1 s/s, publicados = 0 → D2 |
| ¿Por qué no drena? | **Logs** del worker | Siempre el mismo `outbox_id=1112` reintentado → head-of-line blocking |

Para decir: **"La métrica dice que algo anda mal, la traza dice dónde y el log dice por qué."**

---

## Diapositiva 6 — Qué señal sirve para cada falla (medido)

| ID | Señal que detectó | Señal que NO ayudó o engañó |
|---|---|---|
| A1 | p95/p99 + spans de Catálogo | Tasa de error (0 %), promedio |
| A2 | Distancia p50–p99, espera del pool | Promedio, métricas de Postgres |
| B1 | Pool en uso/espera, log de nginx | CPU de Postgres (parecía sana) |
| B2 | `pg_locks` sincronizado con el diente de sierra | Promedio de error (25 % escondía picos de 94 %) |
| C1 | CPU por contenedor, p95 por réplica | p95 global |
| C2 | Lag y pendientes del outbox | Latencia y errores de la API |
| D1 | Log de nginx, tráfico por réplica | Prometheus (no ve el reintento de nginx) |
| D2 | Lag del outbox + logs del worker | Latencia y errores de la API |
| **X1** | **Errores y pool para B2; lag y logs para D2** | **La tasa de error de la API no ve D2** |
