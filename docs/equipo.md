# Equipo y forma de trabajo

Equipo de 3 personas, todas trabajando con asistentes de IA. Las reglas para humanos y agentes están en [AGENTS.md](../AGENTS.md).

## 1. Todólogos con dueños de área

Los tres hacemos de todo: no hay roles por especialidad (D-005). Para no pisarnos, el trabajo se reparte **por tarea**, y cada área tiene un **dueño que coordina** (no es quien hace todo ahí).

- **Tarea:** cada trabajo es un issue con una sola persona asignada. Solo esa persona (y su agente) edita los archivos de esa tarea.
- **Dueño de área:** revisa los PR de su área, mantiene coherente el diseño y desempata las dudas. Cualquiera puede tomar tareas de cualquier área.
- **Rotación:** los dueños se pueden rotar entre bloques de trabajo si alguien quiere aprender otra área.

| Área | Dueño (coordina) | Carpetas | Qué incluye |
|---|---|---|---|
| Motor y datos | _(por asignar)_ | `engine/`, `research/` | Línea base, adaptador de datos, tripulación ficticia, citas científicas |
| App | _(por asignar)_ | `app/` | Figura corporal, tarjetas, gráficos, recordatorios, simulador de escalamiento |
| Producto y relato | _(por asignar)_ | `content/`, `pitch/`, `docs/` | Textos y orientación, pantalla "Limits", video de 30 s, slides, página del proyecto, [registro de uso de IA](uso-de-ia.md), checklist de envío |

Archivos compartidos (para cambiarlos hace falta avisar a las otras dos personas): `AGENTS.md`, `docs/contrato-datos.md`, `docs/idea-base.md`, `docs/decisiones.md`.

**Regla de oro:** dos personas no trabajan a la vez en el mismo archivo. Si una tarea necesita tocar un archivo que está en otra tarea abierta, se coordina primero.

## 2. Flujo con Git

- `main` siempre tiene una demo que corre.
- Ramas cortas: `<rol>/<tema>`, por ejemplo `engine/baseline-band` o `app/body-map`.
- PR pequeños (idealmente menos de 400 líneas) y una persona del equipo revisa antes de fusionar.
- Mensajes en inglés con Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Si un cambio toca el contrato de datos: primero se registra la decisión, luego se cambia el código.

## 3. Ritmo

- **Hasta el 13 nov:** maqueta de la figura y de las tarjetas, motor con Sleep-Accel y tripulación ficticia, contenido HRP para las tarjetas.
- **13 nov:** leer los recursos oficiales y la guía de jueces; adaptar los datos y las reglas de envío.
- **14-15 nov:** plan de 48 h ([research/06](../research/06-plan-48h.md)), ajustado a 3 personas y a esta idea base.

## 4. Sincronización

- Un mensaje diario corto en el chat del equipo: qué hice, qué sigue, qué me bloquea.
- Las dudas de alcance se resuelven en `docs/decisiones.md`, no en el chat, para que los agentes también las lean.
