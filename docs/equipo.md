# Equipo y forma de trabajo

Equipo de 3 personas, todas trabajando con asistentes de IA. Las reglas para humanos y agentes están en [AGENTS.md](../AGENTS.md). Quién usó qué herramienta de IA: [uso-de-ia.md](uso-de-ia.md).

## 1. Todólogos con dueños de área

Los tres hacemos de todo: no hay roles por especialidad (D-005). Para no pisarnos, el trabajo se reparte **por tarea** ([tareas.md](tareas.md)), y cada área tiene un **dueño que coordina** (no es quien hace todo ahí).

- **Tarea:** cada trabajo es una unidad con una sola persona asignada. Solo esa persona (y su agente) edita los archivos de esa tarea.
- **Dueño de área:** revisa los PR de su área, mantiene coherente el diseño y desempata las dudas. Cualquiera puede tomar tareas de cualquier área.
- **Rotación:** los dueños se pueden rotar entre bloques de trabajo si alguien quiere aprender otra área.

| Carril | Dueño (coordina) | Carpetas | Qué incluye |
|---|---|---|---|
| Núcleo (C) | _(por asignar)_ | `src/crew_self_check/core/`, `research/` | Contrato, línea base, referencia poblacional, estados y razones, escenario simulado, puerto de dispositivos, FHIR |
| App del astronauta (A) | _(por asignar)_ | `src/crew_self_check/astronaut/` | Acceso por código, interfaz, misión del pulso, caritas, figura corporal, tarjetas, escalamiento |
| Base en Tierra (G) | _(por asignar)_ | `src/crew_self_check/ground/` | Receptor FHIR, cola de retraso, interfaz del flight surgeon |
| Producto y relato (P) | _(por asignar)_ | `docs/`, `pitch/` | Textos, [pack de envío](submission-pack.md), video o slides, página del proyecto, [registro de uso de IA](uso-de-ia.md), [checklist](submission-checklist.md) |

Aportes ya registrados: las ilustraciones de la guía del pulso las hizo Kevin Toalombo (Gemini y Meta AI); el resto del trabajo de código y documentación consta en [uso-de-ia.md](uso-de-ia.md).

Archivos compartidos (para cambiarlos hace falta avisar a las otras dos personas): `AGENTS.md`, `docs/contrato-datos.md`, `docs/idea-base.md`, `docs/decisiones.md`.

**Regla de oro:** dos personas no trabajan a la vez en el mismo archivo. Si una tarea necesita tocar un archivo que está en otra tarea abierta, se coordina primero.

## 2. Flujo con Git

- Ramas `<carril>/<tema>` (`core/`, `app/`, `ground/`, `docs/`, `pitch/`) salen de `develop` y vuelven a `develop` con PR pequeños revisados por otra persona. `main` solo recibe lo que ya corre de punta a punta (la entrega al reto).
- **Un worktree por sesión:** `git worktree add ../crew-self-check-worktrees/<tema> -b <carril>/<tema>`. Nunca dos sesiones editan el mismo checkout.
- PR pequeños (idealmente menos de 400 líneas). Mensajes en inglés con Conventional Commits.
- Si un cambio toca el contrato de datos: primero se registra la decisión, luego se cambia el código.
- Los cuatro comandos de [AGENTS.md](../AGENTS.md) (sección 9) deben pasar antes de pedir revisión. CI instala el extra `astronaut` para que `mypy` y `pytest` vean Flet.

### Estado de las ramas (2026-11-14)

Todo el trabajo está en ramas locales y **nada se fusionó todavía a `develop` ni a `main`**. Ramas apiladas: se fusionan en este orden.

`core/contract-types` → `core/pulse-reference` y `core/baseline-engine` → `core/status-resolution` → `core/scenario` → `core/device-source` → `app/shell` → `app/pulse-mission` → `app/mood-faces`. Independientes: `docs/gitattributes`, `docs/audio-log`, `app/offline-spike`. La rama `docs/submission-pack` reúne la documentación de todas las anteriores.

## 3. Ritmo

- **14-15 nov:** hackathon. El envío cierra el domingo 15 nov a las 23:59, hora local del evento. Objetivo: primer envío completo con margen, no a último minuto.
- Qué falta para el envío: ver "Antes de enviar" en [submission-checklist.md](submission-checklist.md) y los bloqueadores de [submission-pack.md](submission-pack.md).

## 4. Sincronización

- Un mensaje diario corto en el chat del equipo: qué hice, qué sigue, qué me bloquea.
- Las dudas de alcance se resuelven en `docs/decisiones.md`, no en el chat, para que los agentes también las lean.
