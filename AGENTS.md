# AGENTS.md — Reglas del equipo (humanos y agentes de IA)

Fuente única de reglas de este repositorio. Vale para cualquier agente (Claude Code, Codex, Cursor, Gemini CLI, Copilot, OpenCode, etc.) y para cualquier persona. `CLAUDE.md` solo apunta aquí.

## 1. Contexto

- NASA Space Apps Challenge 2026, reto "Create Health Monitoring Software for Astronauts on Space Missions". Hackathon: 14-15 nov 2026. Envío hasta el domingo 15 nov 23:59 (hora local del evento).
- Qué construimos: [docs/idea-base.md](docs/idea-base.md) y las decisiones D-013 a D-018 de [docs/decisiones.md](docs/decisiones.md). Enunciado oficial: [research/08](research/08-enunciado-oficial.md).
- Este repositorio es **el que se entrega al reto**. La documentación y la investigación viven aquí y también en `nasa-space-apps-2026` (repo de trabajo del equipo); si cambian en uno, se avisa para sincronizar el otro.

## 2. Antes de actuar, lee

1. [docs/decisiones.md](docs/decisiones.md): lo ya decidido; no lo reabras sin que un humano lo pida.
2. [docs/contrato-datos.md](docs/contrato-datos.md): formatos compartidos (versión 0.3).
3. [docs/tareas.md](docs/tareas.md): el trabajo dividido en tareas y su estado.
4. [docs/idea-base.md](docs/idea-base.md) y [docs/equipo.md](docs/equipo.md).

## 3. Idioma

- Documentación interna (`docs/`, `research/`): español neutro.
- Código, identificadores, comentarios, textos de la interfaz, commits, README y entregables (página del proyecto, video, slides): **inglés**. La interfaz se entrega también en español (D-016), con el inglés como idioma fuente.

## 4. Arquitectura (D-017)

- Tres paquetes en `src/crew_self_check/`: `core` (contrato, motor de línea base, mapeo FHIR), `astronaut` (app Flet, servidor local, SQLite) y `ground` (FastAPI y SQLite, recibe FHIR).
- Capas con puertos y adaptadores. `core` es Python puro: **no importa** `astronaut` ni `ground`, ni Flet, ni FastAPI, ni acceso a archivos o red. Los puertos (por ejemplo `DeviceSource`, almacenamiento, exportación FHIR) se definen en `core`; sus adaptadores viven en los sistemas.
- La lógica de estados y razones es determinista. **Nunca un LLM en la ruta de alertas.**

## 5. Alcance y propiedad

- Trabaja solo en los archivos de la tarea asignada ([docs/tareas.md](docs/tareas.md)). Para tocar archivos de otra tarea abierta, pide confirmación al humano.
- No cambies los archivos compartidos (`AGENTS.md`, `docs/contrato-datos.md`, `docs/idea-base.md`, `docs/decisiones.md`) sin que el humano lo pida. Un cambio de contrato requiere primero una decisión registrada.
- No agregues funcionalidades fuera del Must o el Should. Si algo parece necesario, propónlo como una nueva decisión.
- No agregues dependencias sin una decisión registrada.
- No reformatees ni renombres archivos que no forman parte de la tarea.

## 6. Reglas de contenido de salud (no negociables)

- **No hay diagnóstico.** Nunca escribas "detects disease", "diagnoses" ni porcentajes de riesgo o precisión que no estén validados.
- No inventes umbrales clínicos. El estado sale de la línea base personal; mientras no haya datos suficientes, el pulso usa la referencia poblacional rotulada (D-014) y el resto de indicadores queda `insufficient_data`.
- Rotula siempre los datos análogos o simulados como tales; no los presentes como datos de astronautas.
- La orientación (guidance) es educativa y lleva cita (NASA HRP u otra fuente pública). No recetes medicamentos ni dosis, y no escribas pasos clínicos propios (la reanimación es una pantalla fija, D-016).
- **Privado por defecto (D-006, D-015):** nada sale del astronauta sin su confirmación. La conversación con el LLM no se envía a la base; solo medidas acústicas numéricas y sin etiquetas de emoción, y nunca mueven un estado.

## 7. Evidencia y fuentes

- En `docs/` y `research/`, marca cada afirmación con [VERIFICADO] (con URL), [SUPOSICION] o [HUECO]. No inventes fuentes, URL ni cifras.
- Cita en la app y en el pitch los datos de NASA o de agencias socias que uses (requisito de envío).

## 8. Datos y licencias

- Los datos crudos van en `data/` y no se suben (ver `.gitignore`); solo JSON pequeños que la demo necesita.
- Tripulación y datos clínicos **ficticios**. Ningún dato personal real.
- Antes de redistribuir un dataset, comprueba su licencia. No uses logos ni insignias de NASA.

## 9. Código y arnés

- Cambios pequeños y enfocados en una sola tarea. **Test primero** cuando exista un caso runnable: escribe el test que falla y después el código.
- Comandos (todos deben pasar antes de pedir revisión):
  - `uv sync --group dev` (y `--extra astronaut` para la app)
  - `uv run pytest`
  - `uv run ruff check .` y `uv run ruff format --check .`
  - `uv run mypy`
- `pre-commit install` ejecuta ruff y mypy en cada commit. CI repite los mismos pasos.
- Tipado estricto (`mypy --strict`). Sin `print` de depuración, sin código comentado, sin funciones de más de lo necesario.
- Respeta el contrato: si necesitas un campo nuevo, propónlo; no lo inventes.
- Flet 1.x: la API difiere de la de muchos ejemplos de internet (`on_select`, no `on_change`). Verifica cada control con la versión fijada (`flet==1.1.2`) antes de usarlo.

## 10. Git

- Ramas `<carril>/<tema>` (`core/`, `app/`, `ground/`, `docs/`, `pitch/`) salen de `develop` y vuelven a `develop` con PR pequeños revisados por otra persona. `main` solo recibe lo que ya corre de punta a punta (la entrega al reto); `develop` siempre pasa los comandos de la sección 9.
- **Un worktree por sesión.** Si hay varias sesiones a la vez, cada una trabaja en su propio `git worktree` y su propia rama; nunca dos sesiones editan el mismo checkout. La carpeta principal se queda en `main`. Crea los worktrees como carpetas hermanas: `git worktree add ../crew-self-check-worktrees/<tema> -b <carril>/<tema>`. Al terminar: PR y `git worktree remove`.
- Commits en inglés con Conventional Commits. No hagas push, fusiones ni reescrituras de historia sin que el humano lo pida. Nunca subas secretos, claves ni `.env`.

## 11. Uso de IA (requisito oficial)

- El envío debe describir cómo se usó la IA. Cuando tu trabajo llegue al repositorio o al pitch, recuérdale al humano que agregue una fila en [docs/uso-de-ia.md](docs/uso-de-ia.md).
- El humano revisa y entiende todo lo que se sube. Si generas algo que no puedes explicar, dilo. Si generas imágenes o video, déjalo indicado en ese registro.

## 12. Cuando dudes

Pregunta al humano antes de suponer. Si una regla de este archivo choca con un pedido, señálalo y espera.
