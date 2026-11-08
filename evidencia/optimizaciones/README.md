# Optimizaciones del E3 sobre las cargas del E2

Objetivo (rúbrica): cada métrica de tiempo del E2 ≤ 0,90 × valor del informe del E2, con la misma
consulta, escenario, métrica y carga. Un commit por optimización; tras cada una se mide solo lo
afectado (Fase 4 para a, b, c; Q4/Q5 para d). La tabla final sale de `make linea-base`.

## Protocolo de medición por paso

`lab/momento1/linea_base.py fase4 --repeticiones 3`: 3 corridas de las mismas 5.000 órdenes
(`datos/csv/ordenes_fase4_5k.csv`), cada una desde el mismo estado (sin órdenes de la Fase 4, franjas
como en el CSV, `VACUUM ANALYZE`), lab apagado. Se reporta la mediana. Métrica del E2: órdenes exitosas
/ duración (req/s); las exitosas deben seguir siendo 1.523 (misma carga, mismo resultado de negocio).

| Paso | Carpeta | Mediana req/s | Corridas | Exitosas |
| --- | --- | --- | --- | --- |
| 0. Código del E2 | `0_original/` | 400,25 | 362,88 · 404,58 · 400,25 | 1.523 |
| a. Validar el estado antes de los módulos | `a_validar_estado/` | 960,48 | 941,20 · 960,48 · 964,38 | 1.523 |
| b. (+a) UPDATE de Q3 a una sola franja, SKIP LOCKED | `b_una_franja/` | 958,47 | 996,97 · 958,47 · 887,43 | 1.523 |
| c. (+a+b) Sentencias preparadas | `c_preparadas/` | 1.036,97 | 1.063,41 · 931,44 · 1.036,97 | 1.523 |

Nota: con este protocolo el código del E2 da ~400 req/s, frente a 296,42 req/s de la línea base
(`make linea-base`), que mide justo después de recargar la base: allí los datos recién copiados
todavía no tienen hint bits ni mapa de visibilidad y autovacuum está trabajando. Por eso la tabla
final se mide con el mismo `make linea-base` que la línea base (comparación justa), y el aporte de
cada optimización se lee en esta tabla (mismo protocolo entre pasos).

## a. Validar el estado de la orden antes de llamar a los módulos (corrección de comportamiento)

- **Antes (E2):** `OrdenesService.crear_orden_transaccional` ejecutaba Q1 (contrato), Q2 (precio) y
  el UPDATE de franjas de Q3, y recién en el `INSERT` de la cabecera PostgreSQL rechazaba la orden por
  el `CHECK chk_orden_estadoor` (estado `RECIBIDA` o `ENTREGADA`, que la tabla no admite). La
  transacción hacía `ROLLBACK`. Fueron 2.988 de las 5.000 órdenes (60 %): tres consultas, un UPDATE
  de varias franjas y un rollback por orden que de antemano no podía guardarse. El informe del E2
  atribuía los rechazos a contratos no vigentes y franjas completas; solo 489 eran de contrato.
- **Ahora:** el módulo Órdenes valida el estado contra el mismo conjunto del `CHECK` antes de llamar a
  Proveedores, Catálogo y Logística, y rechaza con `ValueError` (fail-fast, sin tocar la base). El
  `CHECK` sigue en la tabla como defensa en profundidad.
- **Por qué es una corrección:** es la validación fail-fast que el diseño del E2 declara («el sistema
  abortó la operación inmediatamente… sin incurrir en I/O innecesario»), y que no ocurría: una orden
  inválida no debe bloquear franjas ni consumir trabajo de otros módulos. El resultado de negocio no
  cambia: las mismas 1.523 órdenes exitosas y 3.477 rechazadas (ahora 3.323 por estado inválido y 154
  por contrato, porque el estado se revisa primero).
- **Alcance:** `OrdenesService(..., validar_estado_primero=True)`. La API del lab (`app/servicios.py`)
  lo deja en `False` para que las repeticiones de los experimentos de fallas sean comparables con las
  corridas originales.

## b. UPDATE de Q3 a una sola franja con SKIP LOCKED (corrección de comportamiento)

- **Antes (E2):** `LogisticaService.reservar_franja` ejecutaba
  `UPDATE … SET reservas_actuales = reservas_actuales + 1 … WHERE cedi_id = … AND fecha = … AND
  estado = 'DISPONIBLE' AND reservas_actuales < capacidad`: sumaba una reserva en **todas** las franjas
  disponibles de ese CEDI y día (5,4 filas por orden en promedio con la base recién cargada) y las
  bloqueaba todas hasta el commit. Medido en la corrida `0_original/fase4_r1`: las 1.523 órdenes
  exitosas consumieron **8.272** cupos y dejaron **1.534** franjas COMPLETAS.
- **Ahora:** la subconsulta elige la primera franja del día con cupo (`ORDER BY hora_inicio LIMIT 1`)
  con `FOR UPDATE SKIP LOCKED` y el UPDATE toca solo esa fila. En `b_una_franja/fase4_r1`: 1.523
  órdenes → **1.523** cupos, 278 franjas COMPLETAS; `desglose/` muestra 1 fila por UPDATE.
- **Por qué es una corrección:** una orden reserva un cupo de descargue, no uno en cada franja del
  día; el E2 agotaba la capacidad logística ~5 veces más rápido de lo real y retenía locks sobre
  todas las franjas del día, lo que serializa órdenes concurrentes del mismo CEDI. Con SKIP LOCKED
  una orden concurrente toma la siguiente franja libre en vez de esperar.
- **Sin cambio en el resultado de negocio:** igual que en el E2, Q3 no rechaza la orden si no hay
  franja con cupo (el UPDATE afecta 0 filas). Se mantuvo para no cambiar la carga ni las 1.523
  exitosas; queda anotado como pendiente de diseño.
- **Aporte medido:** dentro del ruido (960 → 958 req/s): tras la optimización a, Q3 solo corre para
  1.677 órdenes y, en una sola conexión, el costo de tocar ~5 filas en vez de 1 es pequeño. El
  beneficio está en la corrección y en la concurrencia (menos locks), que esta carga secuencial
  del E2 no ejercita.
- **Alcance:** `LogisticaService(cursor, una_franja=True)`; la API del lab usa `una_franja=False`
  (B2 bloquea franjas con `FOR UPDATE`: con SKIP LOCKED el experimento sería otro).

## c. Sentencias preparadas

- **Antes:** cada orden enviaba el texto completo de Q1, Q2, Q3 y los dos INSERT; PostgreSQL los
  analizaba y planificaba en cada ejecución.
- **Ahora:** `preparar_sentencia` hace `PREPARE` una vez por conexión y la ruta usa `EXECUTE`
  (`datos/ejecutar_fase4_modulith.py`, `preparar=True` en los cuatro servicios). Mismo SQL, mismos
  resultados; la API del lab usa `preparar=False` (psycopg 3 con pool: el PREPARE por conexión es otro
  diseño).
- **Aporte medido:** 958,47 → 1.036,97 req/s (+8 %), con la dispersión habitual entre corridas
  (931–1.063).

## d. Índices cubrientes (INCLUDE) + VACUUM para Q4 y Q5

- **Antes (E2):** `idx_orden_proveedor_confirmada (proveedor_id, fecha_creacion) WHERE estado =
  'CONFIRMADA'`, `idx_linea_orden_id (orden_id)` e `idx_orden_proveedor_fecha (proveedor_id,
  fecha_creacion DESC)`, seguidos de `ANALYZE`: los planes visitan el heap por cada fila.
- **Ahora** (`datos/crear_indice_q4.py`, `datos/crear_indice_q5.py`; mismos nombres, se recrean):
  `INCLUDE (fecha_recepcion, fecha_entrega_solicitada)` en el de órdenes confirmadas, `INCLUDE
  (categoria, cantidad_solicitada, cantidad_recibida)` en el de líneas e `INCLUDE (orden_id, cedi_id,
  estado, total)` en el de paginación, seguidos de `VACUUM (ANALYZE)` para el mapa de visibilidad.
- **Planes** (`medir_despues_d.log`): Q5 pasa a `Index Only Scan … Heap Fetches: 0` (0,006–0,04 ms en
  el servidor); en Q4 el join con `linea_orden` es `Index Only Scan` (Heap Fetches: 3) y el acceso a
  `orden_compra` sigue siendo Bitmap Heap Scan (elección del planificador).
- **Medición:** `linea_base.py medir --consultas q4 q5 --repeticiones 3`, mediana por percentil
  (método inclusive, como el informe), sobre la misma base antes y después del cambio.

| Consulta | Escenario | Métrica | E2 | Objetivo | Antes de d | Después de d | Cumple |
|---|---|---|---|---|---|---|---|
| Q4 | frio | p50 | 0.358 | 0.322 | 0.354 | 0.341 | no |
| Q4 | frio | p95 | 0.419 | 0.377 | 0.398 | 0.384 | no |
| Q4 | frio | p99 | 0.435 | 0.392 | 0.41 | 0.397 | no |
| Q4 | caliente | p50 | 2.839 | 2.555 | 2.929 | 2.249 | sí |
| Q4 | caliente | p95 | 9.334 | 8.401 | 9.356 | 7.977 | sí |
| Q4 | caliente | p99 | 14.481 | 13.033 | 12.699 | 9.534 | sí |
| Q5 | frio | p50 | 0.156 | 0.14 | 0.155 | 0.14 | sí |
| Q5 | frio | p95 | 0.181 | 0.163 | 0.186 | 0.181 | no |
| Q5 | frio | p99 | 0.191 | 0.172 | 0.204 | 0.184 | no |
| Q5 | caliente | p50 | 0.25 | 0.225 | 0.274 | 0.223 | sí |
| Q5 | caliente | p95 | 0.327 | 0.294 | 0.329 | 0.321 | no |
| Q5 | caliente | p99 | 0.374 | 0.337 | 0.36 | 0.456 | no |

- **Lectura:** Q4 caliente (la consulta pesada) cumple los tres objetivos; Q4 frío y Q5 mejoran pero
  quedan cerca del objetivo sin alcanzarlo en varias métricas. En Q5 el servidor resuelve en
  < 0,04 ms y el cliente mide 0,14–0,22 ms: el resto es el viaje de ida y vuelta de psycopg2 por la
  red de Docker Desktop, que ningún índice reduce.

## e. Q1–Q3: mediana de 3 corridas

Q1–Q3 no cambian de SQL ni de índices. `make linea-base MEDIANA_Q1_Q3=on` las mide 3 veces más (100
ejecuciones por escenario cada vez) y la tabla usa la mediana de cada percentil
(`linea_base/<UTC>/medir_mediana.json`); la línea base E3 es de 1 corrida.

## Tabla final

`evidencia/linea_base/20261017T035415Z/tabla_final.md` (E2 / línea base E3 / final E3 / objetivo /
¿cumple? / mejora vs. línea base E3). **Reemplazada como oficial por `20261017T044939Z` (ver f).** Resumen de la primera:

- **Fase 4:** 413,69 (E2) → 296,42 (línea base E3) → **1.036,37 req/s** (final); objetivo ≥ 459,66: cumple.
- **Q1–Q3:** los 18 valores cumplen 0,90 × E2.
- **Q4 con índice:** caliente p95 y p99 cumplen; caliente p50 (2,721 vs. 2,555) y frío p50/p95/p99 no.
- **Q5 con índice:** ninguno cumple en la corrida final (p. ej. frío p50 0,154 vs. 0,140).

**Lectura de la mejora vs. la línea base E3.** Q1–Q3 y Q4/Q5 «antes_indice» no cambiaron entre las
dos corridas (mismo SQL, mismos índices) y aun así mejoraron entre 9 y 67 %: es variación del entorno
entre corridas (Docker Desktop en el mismo Mac), no efecto de las optimizaciones. Esas filas sirven de
control: el aporte atribuible a cada optimización es el de la tabla por pasos de arriba (mismo protocolo,
mediana de 3). Q1–Q3 cumplen el objetivo, pero ese cumplimiento depende del entorno, no de un cambio.

## Decisiones tomadas

1. La API del lab (`app/servicios.py`) conserva el comportamiento del E2 (sin a, b ni c) para que las
   repeticiones de los experimentos de fallas sean comparables con las corridas originales.
2. b no rechaza la orden si no hay franja con cupo (como el E2), para no cambiar la carga ni las 1.523
   exitosas.
3. La tabla final se mide con el mismo `make linea-base` que la línea base (base recién cargada); el
   aporte por paso, con el protocolo de estado preparado y mediana de 3 (ver «Protocolo»).
4. Q4/Q5 «antes_indice»: solo referencia, sin objetivo.
5. Antes de las repeticiones del lab, la base se dejó como en las corridas originales (sin órdenes de la
   Fase 4 ni índices de Q4/Q5); después se recrearon los índices finales (`crear_indice_q4/q5.py`).

## f. Intento final sobre Q4 y Q5 (sin cambiar consulta, escenario ni métrica)

Carpeta `f_q4q5/`. Lab apagado; cada cambio por separado con `linea_base.py medir --consultas q4 q5
--repeticiones 3` (mediana de 3).

**1. Dónde se va el tiempo** (`servidor_vs_cliente/`, `lab/momento1/analisis_q4q5.py`): misma secuencia
de parámetros que los `medir_q*.py`; por ejecución, tiempo del cliente y, enseguida, `EXPLAIN (ANALYZE,
BUFFERS)` con el mismo parámetro (planificación + ejecución). p50 en ms:

| Consulta | Cliente (host) | Servidor | Servidor / cliente | Cliente (contenedor) | Servidor (contenedor) |
|---|---|---|---|---|---|
| Q4 frio | 0.298 | 0.11 | 37 % | 0.164 | 0.101 |
| Q4 caliente | 3.167 | 2.091 | 66 % | 1.585 | 1.489 |
| Q5 frio | 0.209 | 0.019 | 9 % | 0.05 | 0.012 |
| Q5 caliente | 0.305 | 0.024 | 8 % | 0.082 | 0.017 |

`SELECT 1` (ida y vuelta mínima): ~0,13 ms desde el host y 0,031 ms desde un contenedor en la red de
Postgres. Q4 caliente se va en el servidor (Parallel Bitmap Heap Scan sobre `orden_compra` + Index Only
Scan de `linea_orden`, todo en `shared hit`); Q4 frío y Q5 se resuelven en 0,01–0,1 ms en el servidor y
el resto es cliente + red. `planes_q4q5.txt` tiene el plan con BUFFERS de cada escenario.

**2. Cambios probados por separado** (`medir_<cambio>.json`; referencia = promedio de `control_1` y
`control_2`; media geométrica de los 12 percentiles, < 1 mejora):

| Cambio | Media geométrica | Decisión |
|---|---|---|
| `jit = off` | 1,040 | descartado (no hay JIT en estos planes: costo bajo el umbral) |
| `random_page_cost = 1.1` | 0,902 en la prueba aislada; **1,09 · 1,47 · 1,14** en el A/B intercalado (`ab_rpc/`) | descartado: el plan no cambia y la mejora no se repite |
| `work_mem = 32MB` | 0,925 | descartado: los planes ya usan 1 batch y sort en memoria (27–193 kB); sin mecanismo, dentro del ruido |
| Índice de Q4 con `orden_id` en el INCLUDE | 0,988 | descartado: el planificador sigue con Bitmap Heap Scan (no pasa a Index Only Scan) |
| `CLUSTER orden_compra USING idx_orden_proveedor_fecha` | 0,992 | descartado: baja los heap blocks de Q4 caliente (1.741 → 53) pero no el tiempo; el índice parcial no admite CLUSTER |

Ruido: `control_2` frente al promedio da 0,951, y 6 mediciones de control idénticas (`ruido_6_controles/`)
dan 0,93–1,05. Ningún cambio supera ese ruido de forma repetible: **no se conserva ninguno**.

**3. Red del entorno (análisis, no resultado oficial)** (`red_contenedor/`): los mismos `medir_q4/q5.py`
ejecutados desde un contenedor con `--network container:postgres-escalables` (host = promedio de una
medición antes y otra después):

| Consulta y métrica | Host (ms) | Contenedor (ms) | Diferencia |
|---|---|---|---|
| Q4 frio p50 | 0.334 | 0.165 | 51 % |
| Q4 frio p95 | 0.369 | 0.184 | 50 % |
| Q4 frio p99 | 0.384 | 0.2 | 48 % |
| Q4 caliente p50 | 1.889 | 1.545 | 18 % |
| Q4 caliente p95 | 6.199 | 5.364 | 13 % |
| Q4 caliente p99 | 9.915 | 7.245 | 27 % |
| Q5 frio p50 | 0.126 | 0.049 | 61 % |
| Q5 frio p95 | 0.15 | 0.061 | 59 % |
| Q5 frio p99 | 0.167 | 0.066 | 60 % |
| Q5 caliente p50 | 0.209 | 0.082 | 61 % |
| Q5 caliente p95 | 0.238 | 0.092 | 61 % |
| Q5 caliente p99 | 0.265 | 0.112 | 58 % |

El reenvío de puertos de Docker Desktop agrega ~0,1 ms por consulta: es 50–60 % de Q4 frío y Q5. Con
ese costo descontado, Q4 frío y Q5 quedarían muy por debajo del objetivo, pero la medición oficial
conserva el mismo método del E2 (cliente en el host).

**4. Tabla final oficial:** como no se conservó ningún cambio, se volvió a medir el mismo estado con la
base recargada (el CLUSTER la había reordenado) y con la mediana de 3 también para Q4/Q5:
`evidencia/linea_base/20261017T044939Z/tabla_final.md` (`make linea-base MEDIANA_Q1_Q3=on
MEDIANA_Q4_Q5=on`). La corrida final anterior (`20261017T035415Z`, mismo código) queda como repetición:
19/30 frente a 20/30 objetivos de consultas; difieren por el ruido del entorno (p. ej. Q3 frío p95 0,161
frente a 0,497 ms: una de las tres repeticiones nuevas dio 0,727).

## g. Sentencias preparadas en Q4 y Q5 (2026-11-08)

Carpeta `g_preparadas/`. `datos/medir_q4.py` y `datos/medir_q5.py` aceptan `PREPARADAS=on`: hacen
`PREPARE` de la **misma consulta** una vez por conexión y miden `EXECUTE` con los mismos parámetros
(misma semilla, mismos proveedores frío/caliente, mismo cliente psycopg2 en el host). Sin la variable
la medición es idéntica a la del E2. Base recargada desde los CSV canónicos (500.000 órdenes) con los
índices INCLUDE del paso d; lab apagado. Protocolo: 3 rondas intercaladas control → preparadas, cada
una `linea_base.py medir --repeticiones 3`; se reporta la mediana de las 3 rondas
(`g_preparadas/comparacion.md`).

| Consulta | Escenario | Métrica | Objetivo | Control | Preparadas | Cambio | Rondas a favor |
|---|---|---|---|---|---|---|---|
| Q4 | frío | p50 | 0,322 | 0,424 | **0,317** | −25 % | 3/3 |
| Q4 | caliente | p50 | 2,555 | 2,428 | **2,249** | −7 % | 3/3 |
| Q4 | caliente | p99 | 13,033 | 10,821 | 10,442 | −4 % | 3/3 |
| Q5 | caliente | p50 | 0,225 | 0,308 | 0,286 | −7 % | 2/3 |
| Q4/Q5 | resto (p95/p99, Q5 frío) | | | | | −7 % a +66 % | 0–2/3 |

- **Lectura:** el efecto es consistente en las medianas (p50) de Q4, donde la planificación del join pesa:
  Q4 frío p50 pasa a cumplir el objetivo. En Q5 el servidor ya resuelve en ~0,02 ms y el ahorro de
  planificación queda por debajo del ruido de la red de Docker Desktop.
- **Ruido:** esta sesión tuvo el host cargado (load average ~5,6 por otras aplicaciones). El propio
  control dio colas 2–5× peores que en octubre (Q5 frío p99 1,09 ms frente a 0,199 ms), así que los
  p95/p99 de este paso no son concluyentes ni comparables con la tabla oficial.
- **Decisión:** se conserva como opción de medición (`PREPARADAS=on`), justificada por el mecanismo y
  por la mejora repetible del p50 de Q4. Queda pendiente repetir la tabla final con el host en reposo
  para confirmar el efecto en las colas.

### g.1 Tabla final con preparadas (2026-11-08)

`PREPARADAS=on make linea-base MEDIANA_Q1_Q3=on MEDIANA_Q4_Q5=on`, dos corridas con 7 min de diferencia:

| Corrida | Condición del host | Métricas Q1–Q5 que cumplen | Fase 4 |
|---|---|---|---|
| `20261108T202644Z` | cargado (app de Claude ~180 % CPU, Chrome) | 9 / 30 | 494,71 req/s |
| `20261108T203314Z` | en reposo, solo terminal y Docker | **30 / 30** | **1.121,23 req/s** |

- **Controles** de la corrida en reposo: Q4 y Q5 *antes del índice* (mismo SQL y plan que el E2) dan
  0,66–1,43 × E2, es decir, iguales o más lentos que el E2. El entorno no favorece la medición, así
  que el cumplimiento de Q4 y Q5 *con índice* se atribuye a las optimizaciones (d: índices INCLUDE +
  VACUUM; g: sentencias preparadas), no al host.
- **Q1–Q3** no cambiaron de SQL: su cumplimiento sigue dependiendo del entorno (ver e).
- **Sensibilidad al host:** la misma medición varió hasta ~2× entre las dos corridas. Ese es el motivo
  de usar mediana de 3 y filas de control, y de declarar las condiciones del host.
- **Tabla final oficial:** `evidencia/linea_base/20261108T205729Z/tabla_final.md` (preparadas en Q1–Q5, host en reposo; línea base E3
  `20261017T034200Z` vs. final). Reemplaza a `20261017T044939Z`.

### g.2 Sentencias preparadas en Q1–Q3 (2026-11-08)

Mismo cambio en `datos/medir_q1.py`, `medir_q2.py` y `medir_q3.py` (`PREPARADAS=on`), mismo protocolo
que g: 3 rondas intercaladas control → preparadas, cada una con mediana de 3
(`g_preparadas_q1q3_v2/comparacion.md`). Con esto Q1–Q3 dejan de ser solo filas de control: su
mejora tiene un mecanismo medido.

| Consulta | Efecto de las preparadas | Rondas a favor |
|---|---|---|
| Q1 | −14 % a −37 % en los 6 percentiles | 3/3 en todos |
| Q2 frío | −10 % a −12 % | 3/3 |
| **Q2 caliente** | **+14 % a +20 % (empeora)** | 0/3 |
| Q3 | −3 % a −9 % (p99 caliente sin cambio) | 3/3 en 5 de 6 |

- **Q2 caliente empeora con el plan genérico.** Tras 5 ejecuciones PostgreSQL reutiliza un plan que
  no ve el proveedor ni la lista de SKU; para los proveedores calientes ese plan es peor. Con
  `plan_cache_mode = force_custom_plan` (`Q2_PLAN_CUSTOM=on`, corridas `prepcustom_*`) Q2 caliente
  vuelve a valores del control o mejores (p95 0,389 ms, p99 0,458 ms), pero se pierde la mejora de Q2
  frío. Queda como trade-off documentado: con o sin plan a la medida, Q2 cumple el objetivo en todas
  las métricas, porque el margen frente al E2 es amplio.
- `g_preparadas_q1q3/` es una corrida abortada (fallo de Q1 corregido) con solo `ctrl_1`; no se usa.

### g.3 Tabla final oficial (preparadas en Q1–Q5)

`20261108T205729Z`, host en reposo y solo `postgres-escalables` corriendo: **30/30** métricas de
Q1–Q5 cumplen 0,90 × E2 y la Fase 4 da 1.081,5 req/s (objetivo ≥ 459,66). Reemplaza como oficial a
`20261108T203314Z`, que se midió con Q1–Q3 sin preparar.
