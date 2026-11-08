# Guion de la demo en vivo — Criterio 2 (estado inicial + falla combinada X1)

Duración: **~8 min** el estado inicial (pasos 1–4) + **~6 min** el estado final (paso 5). Falla mostrada: **X1 = B2 (lock en franjas del CEDI 5) + D2 (ext-sap 503 en 40 % tras 2 s)**.
Ensayada el 2026-11-08 (21:26–21:32 UTC); las capturas de esta carpeta salen de ese ensayo y son el **plan B**.

Roles sugeridos (ajustar a los integrantes):
- **Persona A** — maneja la terminal (carga, `curl`, logs).
- **Persona B** — maneja Grafana y Jaeger y explica lo que se ve.

---

## 0. Antes de la sustentación (15 min antes, NO en vivo)

```bash
# Solo el proyecto: apagar contenedores de otros proyectos para evitar puertos ocupados y ruido
docker ps --format '{{.Names}}'          # revisar qué está corriendo
cd /Users/david/ProyectoASE
make lab-up                               # API, worker, ext-sap, nginx, Prometheus, Grafana, Jaeger
make lab-reset                            # mismo estado inicial (sin órdenes de la API, outbox vacío)
curl -s localhost:8080/admin/faults       # debe decir "fallas": []
```

Dejar abiertas tres pestañas:
1. **Grafana:** `http://localhost:3000/d/lab-entregable3?orgId=1&from=now-10m&to=now&refresh=5s&kiosk&var-proyecto=proyectoase&var-metodo=POST&var-ruta=/ordenes`
   (las variables deben quedar en **POST /ordenes**; por defecto aparece GET /admin/faults).
2. **Jaeger:** `http://localhost:16686/search?service=ordenes-api&operation=POST%20%2Fordenes&minDuration=5s&lookback=10m`
3. Una **terminal** con letra grande.

Cerrar Chrome y otras apps pesadas (la corrida con el Mac cargado salió 2× más lenta).

---

## 1. Estado inicial — línea base (≈ 1,5 min)

**Persona A** arranca la carga (k6 a 20 req/s, semilla 42, órdenes válidas):

```bash
make lab-carga DURACION=8m ETIQUETA=demo
```

**Persona B** muestra la fila *Resumen* de Grafana tras ~60 s (captura `1_estado_inicial.jpg`):

| Señal | Valor esperado |
|---|---|
| Throughput | ~20 req/s |
| Errores 5xx | 0 % / sin datos |
| p95 / p99 POST /ordenes | ~10 ms / ~20 ms |
| Lag del outbox | < 1 s |
| Fallas activas | 0 |

> **Qué decir:** "Este es el sistema del E2 sin correcciones, con el volumen canónico (4,38 M filas, semilla 42).
> Dos réplicas detrás de nginx, pool de 5 conexiones por réplica y un worker que publica el outbox a SAP.
> Esta es la línea base contra la que vamos a comparar."

---

## 2. Inyección en vivo de la combinación (≈ 30 s)

**Persona A**, en la terminal (que se vea el comando):

```bash
curl -X POST localhost:8080/admin/faults -H 'Content-Type: application/json' -d '{"id":"B2","duracion_s":300}'
curl -X POST localhost:8080/admin/faults -H 'Content-Type: application/json' -d '{"id":"D2","duracion_s":300}'
```

> **Qué decir:** "Sin redesplegar: escribimos el `faults.yaml` compartido y cada proceso lo relee cada 0,25 s.
> B2 toma un `FOR UPDATE` de 30 s cada 60 s sobre las franjas del CEDI 5. D2 hace que SAP tarde 2 s y
> responda 503 en el 40 % de las llamadas. Las dos tienen `duracion_s` de 300 como red de seguridad: expiran solas."

---

## 3. Diagnóstico con observabilidad (≈ 4 min)

Esperar ~60–90 s para que pase el primer ciclo del lock. Recorrer en este orden:

### 3.1 Síntoma en la API — fila *Resumen* / *Latencia y errores* (captura `2_falla_resumen.jpg`)
- Errores 5xx ~25 %, p99 con picos de ~27 s, **diente de sierra de 60 s** (= el ciclo del lock).
- Zona roja = falla activa; "Fallas activas = 2".
- Las dos réplicas fallan igual → no es una réplica caída.

### 3.2 Dónde está la causa — *Pool de conexiones* (captura `3_falla_pool.jpg`)
- Conexiones en uso 5/5 en ambas réplicas, **~200 peticiones esperando conexión**, espera p95 ~7 s.
- > "El lock está solo en el CEDI 5, pero las órdenes bloqueadas retienen su conexión y agotan el pool:
  > el resto de las órdenes, y hasta las lecturas, se quedan sin conexión. **Falla en cascada.**"

### 3.3 Confirmación en la base — *PostgreSQL → Locks por modo* (captura `5_falla_locks_postgres.jpg`)
- Locks en el mismo patrón de 60 s y sesiones activas que suben a ~12.

### 3.4 La traza — Jaeger (captura `6_traza_jaeger_espera.jpg`)
- Abrir la traza más lenta de POST /ordenes (~5 s).
- > "La petición tardó 5 s, pero el trabajo real (contrato, SKU, franja, inserts) toma ~7 ms al final.
  > Los primeros ~4,9 s **esperó turno**. Esta orden ni siquiera era del CEDI 5: la latencia es contagiada."

### 3.5 La segunda falla, invisible para la API — *Outbox → worker → ext-sap* (captura `4_falla_outbox_y_fallas.jpg`)
- Pendientes suben (cientos → ~1.400), lag crece 1 s/s, **publicados caen a 0**, llamadas a ext-sap ~3 s con error.
- Logs del worker, **Persona A**:

```bash
docker compose logs worker --since 2m | grep "ext-sap falló" | tail -5
```

- > "Es siempre el mismo `outbox_id`: el worker reintenta en orden el evento que falla y bloquea toda la cola.
  > Head-of-line blocking. Ojo: la tasa de error de la API **no ve** esta falla; solo el lag y los logs."

### 3.6 Cómo interactúan (cierre del diagnóstico)
- > "Las dos fallas viven en caminos distintos (pool de la API vs. worker), así que se suman sin amplificarse.
  > Pero se acoplan por la cola: B2 frena las órdenes que entran y deja menos backlog para D2.
  > Cada falla tiene su propia señal: con un solo panel de la API, D2 habría pasado inadvertida."

---

## 4. Kill switch y recuperación (≈ 1,5 min)

**Persona A**:

```bash
curl -X DELETE localhost:8080/admin/faults
```

Respuesta esperada: `"apagadas_localmente": ["B2","D2"]` (también libera el lock de B2).

**Persona B** muestra (capturas `8_recuperacion_antes_durante_despues.jpg` y `9_recuperacion_outbox.jpg`):
- API: errores 0 % y p95 ~10 ms en la primera ventana de 60 s.
- Outbox: publicados suben a ~39/s y los pendientes drenan a ~0 en ~2 min.
- > "La API se recupera en segundos; el outbox tarda más porque tiene que drenar el backlog.
  > Recuperación de la API ≠ recuperación del sistema."

Si sobra tiempo, apuntar a la evidencia de la corrida completa: `evidencia/results/X1_20261108T163553Z/resumen.md`
(5 min de falla, predicción versionada antes de correr y 5 de 6 predicciones acertadas).

---

## 5. Estado final — la misma falla con las correcciones (criterio 4, ≈ 6 min)

Ensayado el 2026-11-08 (23:31–23:37 UTC); capturas `10` a `13`. Puede ir justo después del paso 4, con el lab ya arriba.

**Persona A** deja el sistema limpio y enciende las correcciones **en caliente** (sin redesplegar, igual que las fallas):

```bash
make lab-reset
curl -X PUT localhost:8080/admin/correcciones -H 'Content-Type: application/json' -d '{"activas":["bulkhead","worker"]}'
make lab-carga DURACION=7m ETIQUETA=demo-final
```

Esperar **~1,5 min** de baseline: al arrancar la carga con el bulkhead (pool de escritura de 3) hay un pico breve de
~3 s por el calentamiento del pool, y no conviene que se mezcle con la falla.

> **Qué decir:** "Encendemos dos correcciones: el bulkhead (pools separados para lectura y escritura, `lock_timeout` de 1 s)
> y el worker corregido (reintentos con backoff, cola de muertos, llamadas a SAP en paralelo y breaker calibrado)."

Después, **la misma inyección** del paso 2:

```bash
curl -X POST localhost:8080/admin/faults -H 'Content-Type: application/json' -d '{"id":"B2","duracion_s":300}'
curl -X POST localhost:8080/admin/faults -H 'Content-Type: application/json' -d '{"id":"D2","duracion_s":300}'
```

Esperar ~90 s y mostrar, en los mismos paneles que en la demo inicial:

| Panel | Demo inicial (sin corrección) | Estado final (con corrección) | Captura |
|---|---|---|---|
| Errores 5xx | ~25 % | **~8 %** | `10_final_resumen_con_correcciones` |
| p99 POST | picos de ~27 s | **mesetas de ~1,4 s** (el `lock_timeout` corta a 1 s) | `10` |
| Outbox: publicados | **caen a 0** | **siguen saliendo** (~4–5/s) | `11_final_outbox_con_correcciones` |
| Fila *Correcciones* | — | bulkhead y worker activos, breaker ext_sap **cerrado**, picos de `lock_timeout` cada 60 s, mensajes a la cola de muertos | `12_final_fila_correcciones` |

> **Qué decir:** "El lock sigue ahí cada 60 s, pero ya no se contagia: solo fallan, y en 1 s, las órdenes que chocan con él.
> El outbox sigue publicando aunque SAP rechace el 40 %, porque los mensajes rechazados van a la cola de muertos
> y las llamadas van en paralelo. Lo que no logramos: el lag sigue creciendo durante la falla, porque cada rechazo
> cuesta 3 intentos de 2 s y el worker no tiene capacidad suficiente."

Kill switch y apagar las correcciones al final:

```bash
curl -X DELETE localhost:8080/admin/faults
curl -X PUT localhost:8080/admin/correcciones -H 'Content-Type: application/json' -d '{"activas":[]}'
```

Captura `13_final_recuperacion`: 0 % de errores, p95 ~10 ms y lag del outbox de **65 ms** en ~1 min
(sin corrección tardaba ~2 min en drenar).

Evidencia completa (5 min de falla, cuatro versiones comparadas):
`evidencia/results/X1-corr-worker-paralelo-v2_20261108T231125Z/analisis.md`.

---

## Plan B (si el entorno falla en vivo)

La rúbrica dice que una demo fallida por el entorno se evalúa según las evidencias alternativas y la preparación.

| Si falla… | Hacer |
|---|---|
| `make lab-up` (puerto ocupado) | `docker ps` → detener lo que use 5432/9090/3000/8080 y repetir |
| Grafana sin datos | Revisar variables POST /ordenes y rango "Last 10 minutes"; si sigue vacío, usar capturas 1–9 |
| La carga no arranca | Mostrar capturas 1–9 en orden y narrar igual que arriba |
| Todo | Capturas de esta carpeta + `resumen.md` de la corrida X1 completa |

Capturas en orden de narración: `1_estado_inicial` → `2_falla_resumen` → `3_falla_pool` → `5_falla_locks_postgres`
→ `6_traza_jaeger_espera` → `4_falla_outbox_y_fallas` + `7_logs_worker_head_of_line.txt` → `8_recuperacion_antes_durante_despues` → `9_recuperacion_outbox`.
Estado final: `10_final_resumen_con_correcciones` → `11_final_outbox_con_correcciones` → `12_final_fila_correcciones` → `13_final_recuperacion`.

## Después de la demo

```bash
make lab-down    # deja solo postgres
```
