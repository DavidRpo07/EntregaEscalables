# Resultado X1-corr-worker-paralelo-v2_20261108T231125Z

- Experimento: **X1** — B2 (lock en franjas CEDI 5) + D2 (ext-sap 503 40 % tras 2 s) simultáneas
- Configuración de la falla B2: `{"id": "B2", "familia": "base_de_datos", "tipo": "externa", "target": "logistica.franja_descargue", "parametros": {"cedi_id": 5, "retencion_s": 30, "ciclo_s": 60}, "duracion_s": 330, "semilla": 42}`
- Configuración de la falla D2: `{"id": "D2", "familia": "disponibilidad", "tipo": "error", "target": "ext_sap.notificar", "codigo_http": 503, "ms_fijos": 2000, "probabilidad": 0.4, "duracion_s": 330, "semilla": 42}`
- Correcciones: **bulkhead** `{"pool_escritura": 3, "pool_lectura": 2, "pool_timeout_ms": 500, "lock_timeout_ms": 1000}`, **worker** `{"max_intentos": 3, "concurrencia": 25, "backoff": {"base_ms": 100, "factor": 2, "jitter": 0.5}, "breaker": {"fallos_para_abrir": 20, "semiabierto_tras_s": 30}}`
- Trazas (OpenTelemetry): encendidas
- Fases: baseline 300 s · falla 300 s · recuperación 120 s · tasa 20 req/s
- Marcas (UTC): baseline 2026-11-08T23:11:32.842+00:00 · falla 2026-11-08T23:16:32.858+00:00 · kill switch 2026-11-08T23:21:33.086+00:00 · fin 2026-11-08T23:23:34.948+00:00
- Predicción: no se exige (corrida con corrección o sin falla)
- Grafana: http://localhost:3000/d/lab-entregable3?from=1794179462842&to=1794180229948

## Por fase (cliente: k6, todas las peticiones; latencias de POST /ordenes)

No enviadas = iteraciones que k6 no pudo lanzar por falta de VUs (`dropped_iterations`). % errores (enviadas) = 5xx o sin respuesta / enviadas; % errores (planificada) = (errores + no enviadas) / planificadas; la peor ventana de 60 s y el SLO usan la carga planificada.

| Fase | Planificadas | Enviadas | No enviadas | req/s enviadas | p50 POST ms | p95 POST ms | p99 POST ms | % errores (enviadas) | % errores (planificada) | peor ventana 60 s % | lag máx s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 6003 | 6003 | 0 | 20.0 | 6.5 | 12.4 | 27.3 | 0.0 | 0.0 | 0.0 | 0.5 |
| falla | 6005 | 6005 | 0 | 20.0 | 8.4 | 1009.5 | 1118.0 | 7.81 | 7.81 | 8.917 | 132.8 |
| recuperación | 2393 | 2393 | 0 | 20.01 | 6.8 | 12.4 | 26.6 | 1.63 | 1.63 | 3.25 | 135.3 |

## SLO

| Fase | p95 ≤ 100 ms | p99 ≤ 250 ms | errores < 1.0 % (60 s) | lag < 10 s |
| --- | --- | --- | --- | --- |
| baseline | ✅ | ✅ | ✅ | ✅ |
| falla | ❌ | ❌ | ❌ | ❌ |
| recuperacion | ✅ | ✅ | ❌ | ❌ |

**Recuperación tras el kill switch:** 9.8 s (cliente 0.0 s, lag 9.8 s) → ✅ SLO < 20 s

## Evidencia

- Inyecciones registradas: 2402 (`evidencia/logs/X1-corr-worker-paralelo-v2_20261108T231125Z/inyecciones.csv`, con la clave de cada petición)
- Trazas guardadas: 40 (`evidencia/traces/X1-corr-worker-paralelo-v2_20261108T231125Z/indice.csv`)
- Métricas: `evidencia/metrics/X1-corr-worker-paralelo-v2_20261108T231125Z/` (peticiones.csv.gz de k6 y series de Prometheus)
- Logs: `evidencia/logs/X1-corr-worker-paralelo-v2_20261108T231125Z/` (JSON por servicio con trace_id; nginx con upstream/status)

## Antes vs. después (lo completa el equipo)

| Señal | Antes | Después | Por qué |
| --- | --- | --- | --- |
| | | | |
