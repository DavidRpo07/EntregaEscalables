# Resultado X1-corr_20261108T223627Z

- Experimento: **X1** — B2 (lock en franjas CEDI 5) + D2 (ext-sap 503 40 % tras 2 s) simultáneas
- Configuración de la falla B2: `{"id": "B2", "familia": "base_de_datos", "tipo": "externa", "target": "logistica.franja_descargue", "parametros": {"cedi_id": 5, "retencion_s": 30, "ciclo_s": 60}, "duracion_s": 330, "semilla": 42}`
- Configuración de la falla D2: `{"id": "D2", "familia": "disponibilidad", "tipo": "error", "target": "ext_sap.notificar", "codigo_http": 503, "ms_fijos": 2000, "probabilidad": 0.4, "duracion_s": 330, "semilla": 42}`
- Correcciones: **bulkhead** `{"pool_escritura": 3, "pool_lectura": 2, "pool_timeout_ms": 500, "lock_timeout_ms": 1000}`, **worker** `{"max_intentos": 3, "backoff": {"base_ms": 100, "factor": 2, "jitter": 0.5}, "breaker": {"fallos_para_abrir": 5, "semiabierto_tras_s": 30}}`
- Trazas (OpenTelemetry): encendidas
- Fases: baseline 300 s · falla 300 s · recuperación 120 s · tasa 20 req/s
- Marcas (UTC): baseline 2026-11-08T22:36:35.614+00:00 · falla 2026-11-08T22:41:35.627+00:00 · kill switch 2026-11-08T22:46:35.834+00:00 · fin 2026-11-08T22:48:37.672+00:00
- Predicción: no se exige (corrida con corrección o sin falla)
- Grafana: http://localhost:3000/d/lab-entregable3?from=1794177365614&to=1794178132672

## Por fase (cliente: k6, todas las peticiones; latencias de POST /ordenes)

No enviadas = iteraciones que k6 no pudo lanzar por falta de VUs (`dropped_iterations`). % errores (enviadas) = 5xx o sin respuesta / enviadas; % errores (planificada) = (errores + no enviadas) / planificadas; la peor ventana de 60 s y el SLO usan la carga planificada.

| Fase | Planificadas | Enviadas | No enviadas | req/s enviadas | p50 POST ms | p95 POST ms | p99 POST ms | % errores (enviadas) | % errores (planificada) | peor ventana 60 s % | lag máx s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 6001 | 6001 | 0 | 20.0 | 7.1 | 11.4 | 24.3 | 0.0 | 0.0 | 0.0 | 1.1 |
| falla | 6004 | 6004 | 0 | 20.0 | 8.4 | 1010.1 | 1116.0 | 7.895 | 7.895 | 9.0 | 294.1 |
| recuperación | 2396 | 2396 | 0 | 20.01 | 6.5 | 10.9 | 23.7 | 0.0 | 0.0 | 0.0 | 314.1 |

## SLO

| Fase | p95 ≤ 100 ms | p99 ≤ 250 ms | errores < 1.0 % (60 s) | lag < 10 s |
| --- | --- | --- | --- | --- |
| baseline | ✅ | ✅ | ✅ | ✅ |
| falla | ❌ | ❌ | ❌ | ❌ |
| recuperacion | ✅ | ✅ | ✅ | ❌ |

**Recuperación tras el kill switch:** no se recuperó dentro de la fase de recuperación (cliente 0.0, lag None)

## Evidencia

- Inyecciones registradas: 22 (`evidencia/logs/X1-corr_20261108T223627Z/inyecciones.csv`, con la clave de cada petición)
- Trazas guardadas: 40 (`evidencia/traces/X1-corr_20261108T223627Z/indice.csv`)
- Métricas: `evidencia/metrics/X1-corr_20261108T223627Z/` (peticiones.csv.gz de k6 y series de Prometheus)
- Logs: `evidencia/logs/X1-corr_20261108T223627Z/` (JSON por servicio con trace_id; nginx con upstream/status)

## Antes vs. después (lo completa el equipo)

| Señal | Antes | Después | Por qué |
| --- | --- | --- | --- |
| | | | |
