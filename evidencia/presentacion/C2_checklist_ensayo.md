# Criterio 2 — Checklist de ensayo del equipo (25 pts)

El guion completo está en `evidencia/demo/GUION_DEMO.md`. Este checklist es para **ensayarlo ustedes** al menos una vez antes de la sustentación.

## Ensayo 1 (obligatorio)

- [ ] Asignar **Persona A** (terminal) y **Persona B** (Grafana/Jaeger). Los demás integrantes toman otros criterios.
- [ ] Apagar contenedores de otros proyectos (`docker ps`) y cerrar Chrome y apps pesadas.
- [ ] `make lab-up` + `make lab-reset` → `curl -s localhost:8080/admin/faults` debe devolver `"fallas": []`.
- [ ] Abrir Grafana con la URL del guion (variables en **POST /ordenes**) y Jaeger.
- [ ] Correr el guion completo con cronómetro. Meta: **≤ 8 min**.
- [ ] En cada paso, tomar una captura en **buena resolución** (Cmd+Shift+4) y reemplazar las de `evidencia/demo/` (las actuales son de baja resolución).
- [ ] Confirmar que se ven: diente de sierra de 60 s, pool 5/5, traza de ~5 s en Jaeger, `outbox_id` repetido en los logs y recuperación después del kill switch.
- [ ] `make lab-down` al terminar.

## Antes de entrar a la sustentación

- [ ] Lab arriba y limpio 15 min antes (`make lab-up && make lab-reset`).
- [ ] Pestañas abiertas: Grafana, Jaeger, terminal con letra grande.
- [ ] Capturas del plan B a mano (carpeta abierta o en las diapositivas).
- [ ] Mac conectado a la corriente; notificaciones apagadas.

## Preguntas probables del profesor (respuestas cortas)

| Pregunta | Respuesta |
|---|---|
| ¿Cómo activan la falla sin redesplegar? | `POST /admin/faults` escribe el `faults.yaml` compartido; cada proceso lo relee cada 0,25 s |
| ¿Por qué fallan órdenes de otros CEDI? | Las órdenes bloqueadas retienen su conexión y agotan el pool de 5 por réplica |
| ¿Por qué la API no muestra D2? | El worker es otro proceso; la API ya respondió 201. Solo lo ven el lag y los logs |
| ¿Es reproducible? | Sí: semilla 42, decisión de inyección por hash (semilla, falla, petición), `make lab-reset` |
| ¿Qué pasa si el kill switch falla? | Cada falla tiene `duracion_s`: expira sola. El runner además escribe el archivo directo |
