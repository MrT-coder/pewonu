# Tareas (TODO)

Estado: **actualizado el 2026-11-14.** Hecho: C1 a C6, A1, A9 y partes de A2, A5 y A6 (ver cada fila). Todo está en ramas locales sin fusionar (orden al final). Cada tarea es una unidad con su propio test, su código y su documentación. Las decisiones D-013 a D-023 de [decisiones.md](decisiones.md) mandan; el contrato `0.3` está en [contrato-datos.md](contrato-datos.md). Dueño y rama se rellenan al tomar la tarea (una persona por tarea, [AGENTS.md](../AGENTS.md) sección 5).

Leyenda: **M** Must, **S** Should, **C** Could. `Dep` = depende de. `Hecho cuando` = criterio de aceptación observable.

## Carril H · Arnés (listo)

| ID | Tarea | Nivel | Estado |
|---|---|---|---|
| H1 | Repositorio con `AGENTS.md`, capas `core`/`astronaut`/`ground`, `pytest`, `ruff`, `mypy`, `pre-commit` y CI | M | hecho (sin commit aún) |

## Carril C · Núcleo (`core`)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| C1 | Tipos del contrato `0.3` (`Measurement`, `IndicatorStatus`, `SystemStatus`, `CrewProfile`, `VoiceFeatures`, `SpacecraftProfile`) con (de)serialización JSON y validación | M | H1 | Tests de ida y vuelta JSON de cada objeto; un valor inválido (`environment` desconocido) se rechaza. **Hecho 2026-11-14:** `core/contract.py`, rama `core/contract-types` |
| C2 | Tabla de referencia poblacional del pulso en reposo por edad y sexo (NHSR nº 41): abrir el PDF, copiar los valores, definir qué percentil marca cada color (D-014) | M | C1 | Tabla en datos versionados con su cita; test por fila; el criterio de color está documentado. **Hecho 2026-11-14** (6 filas adultas, 20-79 años; criterio propuesto por confirmar): [pulso-referencia.md](pulso-referencia.md), rama `core/pulse-reference` |
| C3 | Motor de línea base por persona, indicador y espacio: mediana con banda robusta, desviación sostenida, `insufficient_data` (D-013) | M | C1 | Tests: sin datos suficientes es gris; 3 lecturas sostenidas fuera de banda dan ámbar; cada espacio tiene su línea base. **Hecho 2026-11-14:** `core/baseline.py`, rama `core/baseline-engine`; produce `ok`, `watch` o `insufficient_data` (el rojo y la referencia son de C4); defaults [SUPOSICION]: 5 días, 3 lecturas, banda 2.5 MAD; con MAD 0 usa la desviación media absoluta |
| C4 | Resolución de estado: `reference` (`personal`, `transition`, `population`), estado del sistema = peor indicador, sugerencia de escalamiento y razones con plantilla en inglés y español | M | C2, C3 | Tests de los cuatro estados; la razón nunca depende de un LLM; `population` rotula su referencia. **Hecho 2026-11-14:** `core/status.py` y `core/reasons.py`, rama `core/status-resolution` (apilada sobre C2 y C3). [SUPOSICION]: escalamiento por estado (ámbar → `crew_cmo`, rojo → `ground_surgeon`), lectura vieja tras 3 días, asignación de indicadores a sistemas |
| C5 | Escenario simulado: tripulación ficticia con historial clínico en la Tierra y viaje Tierra → nave → Marte (R+0 a R+3), con caso gris y pulso manual | M | C1 | Genera `Measurement` con `source: simulated-scenario`; incluye los cuatro estados; reproducible con una semilla. **Hecho 2026-11-14:** `core/scenario.py`, rama `core/scenario`: 2 tripulantes ficticios, 14 días en la Tierra, 10 en la nave y R+0 a R+3; el rojo sale del pulso manual de `crew-02` con referencia poblacional |
| C6 | Puerto `DeviceSource` y adaptador simulado de reloj y banda (D-011) | M | C1 | El motor consume lecturas del simulador sin cambiar; el adaptador se puede sustituir en un test. **Hecho 2026-11-14:** puerto en `core/devices.py`, adaptador en `astronaut/simulated_device.py`, rama `core/device-source` (apilada sobre C5). `DeviceReading` es un tipo del puerto, no del contrato |
| C7 | Perfil de nave `iss-analog`: verificar con fuente los equipos de la ISS, qué indicadores habilitan y qué ejercicios proponen, con cita (D-016) | S | C1 | Archivo de perfil con cada equipo respaldado por una URL; lo no verificado queda marcado [HUECO] y fuera |
| C8 | Exportación FHIR R4: `Observation` de signos vitales (LOINC) y códigos locales para estados, líneas base y medidas acústicas; `Bundle` | S | C1 | El Bundle valida contra la estructura FHIR; sin consentimiento no se genera (D-006). **Hecho 2026-11-14:** `core/fhir.py`, rama `core/fhir-export`; un Bundle con los 11 indicadores y los 4 estados da **0 errores** en el validador oficial de HL7. Pendiente: LOINC de presión, glucosa y sueño, un `CodeSystem` para los códigos locales, el envío (A10) y la recepción (G1) |

## Carril A · App del astronauta (`astronaut`)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| A1 | **Spike de offline:** probar `flet build web --no-cdn` o el servidor local sin internet, con la versión fijada; registrar el resultado | M | H1 | La app abre y responde con la red desconectada, o queda registrado el fallo y la salida a TypeScript (D-017). **Bloquea todo el carril.** **Hecho 2026-11-14:** pasa con `no_cdn=True` ([spike-offline-flet.md](spike-offline-flet.md)); rama `app/offline-spike` |
| A2 | Estructura de la app, cambio de idioma español/inglés y persistencia local en SQLite detrás de un puerto de almacenamiento | M | A1, C1 | Cambiar de idioma actualiza toda la pantalla; los datos sobreviven a un reinicio; el almacenamiento se puede sustituir en un test. **Parcial 2026-11-14:** carcasa, idioma y acceso por código (D-020) en `astronaut/`, rama `app/shell`; **Almacenamiento hecho 2026-11-14:** puerto `MeasurementStore` en `core/storage.py` y adaptador SQLite (solo biblioteca estándar) en `astronaut/sqlite_store.py`; `AppState` recibe el puerto y usa memoria por defecto; la app guarda en `data/crew-self-check.db` (`CREW_SELF_CHECK_DB` lo cambia), rama `app/sqlite-storage`. [SUPOSICION] solo las mediciones persisten; la bandeja de envíos sigue en memoria |
| A3 | Figura corporal con arte SVG y zonas clicables, coloreada por `SystemStatus` | M | A2, C4 | Cada sistema abre su tarjeta; el color sale del estado y no está fijo en el código. **Hecho 2026-11-14** en `astronaut/ui/body.py` (rama `app/body-view`): seis zonas clicables coloreadas por `SystemStatus` sobre la silueta de un ícono de Flet, con leyenda y texto en cada estado. [SUPOSICION] no es arte SVG; el SVG sigue [HUECO] |
| A4 | Tarjeta del sistema: tendencia con banda, explicación simple, orientación con cita y checklist | M | A3 | Cada afirmación de orientación tiene su cita; sin diagnóstico ni dosis. **Hecho 2026-11-14** en `astronaut/ui/system_card.py`: qué mide, con qué se comparó, cada indicador con su razón, tendencia con banda (dibujada con el lienzo de Flet, sin dependencia nueva), sugerencia de escalamiento y orientación genérica con cita de la NASA y sin pasos clínicos |
| A5 | Entrada manual del pulso: el astronauta cuenta y la app calcula, con el gráfico explicativo | M | A2, C3 | Un conteo produce un `Measurement` con `method: palpation`. **Hecho 2026-11-14** como misión guiada (D-021) en `astronaut/pulse_mission.py` y `ui/checkin.py`, rama `app/pulse-mission`; se guarda vía el puerto de almacenamiento (A2) |
| A6 | Burbuja de ánimo: encuesta clásica (Must) y bitácora de audio opcional (Could): el audio se descarta y se guardan solo medidas acústicas numéricas (D-015, D-019) | M | A2 | La encuesta mueve el estado de `mood`; el audio no queda en disco ni en SQLite; las medidas acústicas no mueven ningún estado. **Parcial 2026-11-14:** la encuesta de cinco caritas está hecha (`astronaut/mood.py`, `ui/checkin.py`, rama `app/mood-faces`); faltan la bitácora de audio y SQLite |
| A7 | Reproductor del viaje: cambio de espacio y rótulos de referencia de transición | M | A3, C5 | Se recorre Tierra → nave → Marte y la figura cambia; cada estado muestra contra qué referencia se comparó. **Parcial 2026-11-14:** barra del viaje (`ui/journey.py`) con control de día, espacio y tiempo simulado; falta la reproducción automática y los rótulos de transición por día |
| A8 | Recordatorios de rutina del escenario simulado | M | A7 | Aparece el recordatorio del día con la medición pedida |
| A9 | Pantalla "Limits": datos análogos, nada validado en órbita, sin diagnóstico | M | A2 | Visible desde cualquier pantalla, en ambos idiomas. **Hecho 2026-11-14** en la carcasa (login y app), rama `app/shell` |
| A10 | Escalamiento: sugiere, el astronauta confirma y se envía un Bundle a la base con el retraso simulado | S | A4, C8, G1 | Sin confirmación no sale nada; con ella llega a `ground`. **Parcial 2026-11-14:** elegir, confirmar y empaquetar un Bundle FHIR (`astronaut/share_model.py`, `ui/share.py`, rama `app/summary`); llega con retraso simulado a una **bandeja local**. Un paquete de la app dio 0 errores en el validador de HL7. **Recepción real hecha 2026-11-14:** `astronaut/ground_client.py` envía el Bundle por HTTP a `ground` y toma de la base la hora de llegada; si la base no responde, el paquete queda en cola y se reenvía (rama `ground/receiver`) |
| A11 | Pantalla fija de emergencia en la nave (¿respira?, ¿responde?, escalar y seguir el procedimiento oficial) | S | A2 | Sin pasos clínicos propios (D-016) |
| A12 | Racha de adherencia: premia medir con regularidad, nunca "estar sano" | S | A5 | La racha depende de mediciones hechas, no de su valor |
| A13 | Voz como entrada y salida (dictar datos, leer guías) | S | A2 | Un dato dictado produce el mismo `Measurement` que el manual |
| A15 | Resumen por astronauta ("KPIs humanos", D-020): estados por sistema, chequeo de hoy, constancia, qué tan lista está la línea base aquí, qué requiere atención y las últimas lecturas | M | A3, C4 | Todo sale del estado ya calculado, sin umbrales nuevos; la constancia mide con qué frecuencia se mide, nunca cómo está la persona. **Hecho 2026-11-14** en `astronaut/summary_model.py` y `ui/summary.py`, rama `app/summary` |
| A16 | Accesibilidad del shell de la app (hallazgos B1 y B2 del gate de QA 2026-11-14): nombre accesible en los botones de ícono (glosario, límites, día anterior y siguiente), etiqueta del campo oculto y recorrido por teclado | S | A2 | `a11y-scan` sin violaciones `critical`/`serious` en el Resumen y Tab recorre los controles. [SUPOSICION] puede ser una limitación de Flet 1.1.2: si lo es, se documenta |

## Carril G · Base en Tierra (`ground`)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| G1 | Servicio FastAPI con SQLite que recibe y valida Bundles FHIR (D-018) | M | C8 | Un Bundle válido se guarda; uno inválido se rechaza con error claro. **Hecho 2026-11-14** en `ground/` (`ingest.py`, `service.py`, `api.py`, `sqlite_inbox.py`; puerto `BundleInbox` en `core/inbox.py`), rama `ground/receiver`: `POST /bundles` responde 202 o 422 con todos los problemas; solo acepta `Patient` y `Observation`, sin nombre ni fecha de nacimiento; el mismo Bundle dos veces se guarda una vez |
| G2 | Cola de retraso de comunicación simulado y configurable (~3 a 22 min) | M | G1 | Lo enviado aparece en la base pasado el retraso; el retraso se configura. **Hecho 2026-11-14** (D-026): `GET/PUT /config` (0 a 60 min, 12 por defecto) y reloj inyectable `PUT/DELETE /clock` que la app sincroniza con el viaje |
| G3 | Interfaz de la base (flight surgeon): estado por tripulante, Bundles recibidos y resumen del escalamiento, en español e inglés. [SUPOSICION] Flet por coherencia con `astronaut`; falta decidirlo | M | G2 | Solo muestra lo que el astronauta envió; no muestra datos crudos ni audio. **Hecho 2026-11-14** como páginas HTML del propio servicio, no Flet (D-026): `/` y `/crew/{id}`, es/en con `?lang=`, estado por indicador con razón, qué requiere atención, últimas lecturas y los límites visibles; `python -m crew_self_check.ground` sirve en 127.0.0.1:8560 |
| G4 | Vista de tendencias de lo recibido | S | G3 | Gráfico por indicador con la banda enviada |

## Carril P · Producto, relato y envío

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| P1 | Leer la Project Submission Guide y la Judging & Awards Guide (publicadas el 13 nov) y completar [submission-checklist.md](submission-checklist.md) | M | — | Cada [HUECO] del checklist queda resuelto o justificado. **Parcial 2026-11-14:** el texto del formulario cerró varios [HUECO] ([submission-checklist.md](submission-checklist.md)); faltan las guías completas |
| P2 | Guion y storyboard de la demo de 30 s (Tierra → nave → Marte) y versión de 7 slides | M | A7 | Guion en inglés con subtítulos; muestra el gris, el color relativo y la privacidad |
| P3 | Grabar el video y alojarlo en un enlace público externo | M | P2 | Se abre en una ventana privada sin pedir registro |
| P4 | Página del proyecto en inglés con todos los campos obligatorios y referencias | M | P1 | Campos completos; cita los datos de NASA y de la CSA usados |
| P5 | Descripción del uso de IA en inglés a partir de [uso-de-ia.md](uso-de-ia.md) | M | — | Resume las herramientas usadas y qué revisó el humano |
| P6 | Preparar el repositorio público: README, licencia, citas de datos, sin logos de NASA | M | — | Licencia decidida; ningún dato con licencia no confirmada |
| P7 | Verificar que todos los integrantes están registrados en el mismo evento local | M | — | Lista confirmada antes del envío |
| P8 | Envío completo con margen y verificación de enlaces | M | P3, P4, P5, P6, P9 | Enviado antes del domingo 23:59; enlaces probados |
| P9 | **Marca de agua visible** en las imágenes generadas con IA (las ocho ilustraciones del pulso y cualquier diapositiva que las use), según D-023 | M | — | Cada imagen con IA muestra una marca visible que lo indica; sin marca de NASA |

## Carril Q · Integración

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| Q1 | Flujo de punta a punta: viaje simulado → escalamiento → recepción en la base | M | A10, G3 | Un guion automático lo recorre sin errores. **Parcial 2026-11-14:** `tests/test_end_to_end.py` recorre app → HTTP real → base → vista, y el gate de QA manual (`feature-qa`) dio APTO a la base; falta el guion del viaje completo hasta Marte |
| Q2 | Congelar funcionalidades y ensayar la demo | M | Q1 | La demo corre desde cero en un equipo limpio |

## Herramienta de desarrollo (decisión pendiente)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| X1 | MCP de Flet (`flet-mcp`) como ayuda para los agentes: verifica controles, propiedades y enums de la versión instalada. Verificado el 2026-11-14 en el spike: `flet-mcp 1.1.2` (misma versión que Flet) responde `get_api` y devuelve `on_select` y no `on_change` en `Dropdown`, el error que ya tuvimos; un control inexistente da "not found". No probado: el arranque por stdio (`flet mcp`) desde un cliente real | S | H1 | Decisión registrada (herramienta de desarrollo, no entra en la app); `flet-mcp==1.1.2` en el grupo de desarrollo y entrada en `.mcp.json` |

## Orden sugerido y ruta crítica

1. **Ya, en paralelo:** C1 (núcleo), A1 (spike offline) y P1 (guía de envío).
2. **Luego:** C2, C3, C5 y C6 en el núcleo; A2 en cuanto A1 pase.
3. **Después:** C4 → A3, A4, A5, A7; C8 → G1 → G2 → G3.
4. **Cierre:** A10, Q1, Q2 y todo el carril P.

**Ruta crítica:** A1 → A2 → A3 → A7 → Q1 → P2 → P3 → P8. Si A1 falla, se activa la salida a TypeScript y se replanifica el carril A.

**Paralelismo seguro (archivos disjuntos):** `core/` (C), `astronaut/` (A), `ground/` (G) y `docs/`/`pitch/` (P) no comparten archivos; lo único compartido es el contrato, que solo cambia con una decisión registrada.

## Orden de fusión de las ramas (2026-11-14)

Ninguna rama se fusionó aún a `develop`. Están apiladas; se fusionan en este orden, con PR pequeños:

1. `core/contract-types` (C1) → `core/pulse-reference` (C2) y `core/baseline-engine` (C3) → `core/status-resolution` (C4) → `core/scenario` (C5) → `core/device-source` (C6).
2. `app/shell` (acceso por código, D-020) → `app/pulse-mission` (A5, D-021) → `app/mood-faces` (A6, parte de la encuesta, D-022).
3. Independientes: `docs/gitattributes`, `docs/audio-log` (D-019) y `app/offline-spike` (A1).
4. `docs/submission-pack` reúne la documentación de todas las anteriores; al fusionar el resto, puede haber conflictos simples en `tareas.md`, `decisiones.md` y `uso-de-ia.md`.

**Lo que sigue (propuesta):** C8 (exportación FHIR, validada con el validador de HL7), A3 y A4 (figura corporal y tarjetas), A2 (SQLite), G1 a G3 (base en Tierra), A10 (escalamiento) y P9 (marca de agua).
