# Resultado X1-corr-worker-paralelo_20261108T225719Z

- Experimento: **X1** — B2 (lock en franjas CEDI 5) + D2 (ext-sap 503 40 % tras 2 s) simultáneas
- Configuración de la falla B2: `{"id": "B2", "familia": "base_de_datos", "tipo": "externa", "target": "logistica.franja_descargue", "parametros": {"cedi_id": 5, "retencion_s": 30, "ciclo_s": 60}, "duracion_s": 330, "semilla": 42}`
- Configuración de la falla D2: `{"id": "D2", "familia": "disponibilidad", "tipo": "error", "target": "ext_sap.notificar", "codigo_http": 503, "ms_fijos": 2000, "probabilidad": 0.4, "duracion_s": 330, "semilla": 42}`
- Correcciones: **bulkhead** `{"pool_escritura": 3, "pool_lectura": 2, "pool_timeout_ms": 500, "lock_timeout_ms": 1000}`, **worker** `{"max_intentos": 3, "concurrencia": 25, "backoff": {"base_ms": 100, "factor": 2, "jitter": 0.5}, "breaker": {"fallos_para_abrir": 5, "semiabierto_tras_s": 30}}`
- Trazas (OpenTelemetry): encendidas
- Fases: baseline 300 s · falla 300 s · recuperación 120 s · tasa 20 req/s
- Marcas (UTC): baseline 2026-11-08T22:57:27.335+00:00 · falla 2026-11-08T23:02:37.859+00:00 · kill switch 2026-11-08T23:07:38.130+00:00 · fin 2026-11-08T23:09:29.412+00:00
- Predicción: no se exige (corrida con corrección o sin falla)
- Grafana: http://localhost:3000/d/lab-entregable3?from=1794178617335&to=1794179384412

## Por fase (cliente: k6, todas las peticiones; latencias de POST /ordenes)

No enviadas = iteraciones que k6 no pudo lanzar por falta de VUs (`dropped_iterations`). % errores (enviadas) = 5xx o sin respuesta / enviadas; % errores (planificada) = (errores + no enviadas) / planificadas; la peor ventana de 60 s y el SLO usan la carga planificada.

| Fase | Planificadas | Enviadas | No enviadas | req/s enviadas | p50 POST ms | p95 POST ms | p99 POST ms | % errores (enviadas) | % errores (planificada) | peor ventana 60 s % | lag máx s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 6217 | 6217 | 0 | 20.02 | 8.1 | 9305.8 | 17955.4 | 4.584 | 4.584 | 67.136 | 21.3 |
| falla | 6000 | 6000 | 0 | 19.98 | 9.1 | 1010.5 | 1221.8 | 8.0 | 8.0 | 9.0 | 168.5 |
| recuperación | 2183 | 2183 | 0 | 20.01 | 7.9 | 13.1 | 25.8 | 0.0 | 0.0 | 0.0 | 192.5 |

## SLO

| Fase | p95 ≤ 100 ms | p99 ≤ 250 ms | errores < 1.0 % (60 s) | lag < 10 s |
| --- | --- | --- | --- | --- |
| baseline | ❌ | ❌ | ❌ | ❌ |
| falla | ❌ | ❌ | ❌ | ❌ |
| recuperacion | ✅ | ✅ | ✅ | ❌ |

**Recuperación tras el kill switch:** 29.2 s (cliente 0.0 s, lag 29.2 s) → ❌ SLO < 20 s

## Evidencia

- Inyecciones registradas: 1842 (`evidencia/logs/X1-corr-worker-paralelo_20261108T225719Z/inyecciones.csv`, con la clave de cada petición)
- Trazas guardadas: 40 (`evidencia/traces/X1-corr-worker-paralelo_20261108T225719Z/indice.csv`)
- Métricas: `evidencia/metrics/X1-corr-worker-paralelo_20261108T225719Z/` (peticiones.csv.gz de k6 y series de Prometheus)
- Logs: `evidencia/logs/X1-corr-worker-paralelo_20261108T225719Z/` (JSON por servicio con trace_id; nginx con upstream/status)

## Antes vs. después (lo completa el equipo)

| Señal | Antes | Después | Por qué |
| --- | --- | --- | --- |
| | | | |
