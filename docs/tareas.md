# Tareas (TODO)

Estado: **propuesta de reparto, 2026-11-14.** Cada tarea es una unidad con su propio test, su código y su documentación. Las decisiones D-013 a D-018 de [decisiones.md](decisiones.md) mandan; el contrato `0.3` está en [contrato-datos.md](contrato-datos.md). Dueño y rama se rellenan al tomar la tarea (una persona por tarea, [AGENTS.md](../AGENTS.md) sección 5).

Leyenda: **M** Must, **S** Should, **C** Could. `Dep` = depende de. `Hecho cuando` = criterio de aceptación observable.

## Carril H · Arnés (listo)

| ID | Tarea | Nivel | Estado |
|---|---|---|---|
| H1 | Repositorio con `AGENTS.md`, capas `core`/`astronaut`/`ground`, `pytest`, `ruff`, `mypy`, `pre-commit` y CI | M | hecho (sin commit aún) |

## Carril C · Núcleo (`core`)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| C1 | Tipos del contrato `0.3` (`Measurement`, `IndicatorStatus`, `SystemStatus`, `CrewProfile`, `VoiceFeatures`, `SpacecraftProfile`) con (de)serialización JSON y validación | M | H1 | Tests de ida y vuelta JSON de cada objeto; un valor inválido (`environment` desconocido) se rechaza. **Hecho 2026-11-14:** `core/contract.py`, rama `core/contract-types` |
| C2 | Tabla de referencia poblacional del pulso en reposo por edad y sexo (NHSR nº 41): abrir el PDF, copiar los valores, definir qué percentil marca cada color (D-014) | M | C1 | Tabla en datos versionados con su cita; test por fila; el criterio de color está documentado |
| C3 | Motor de línea base por persona, indicador y espacio: mediana con banda robusta, desviación sostenida, `insufficient_data` (D-013) | M | C1 | Tests: sin datos suficientes es gris; 3 lecturas sostenidas fuera de banda dan ámbar; cada espacio tiene su línea base. **Hecho 2026-11-14:** `core/baseline.py`, rama `core/baseline-engine`; produce `ok`, `watch` o `insufficient_data` (el rojo y la referencia son de C4); defaults [SUPOSICION]: 5 días, 3 lecturas, banda 2.5 MAD; con MAD 0 usa la desviación media absoluta |
| C4 | Resolución de estado: `reference` (`personal`, `transition`, `population`), estado del sistema = peor indicador, sugerencia de escalamiento y razones con plantilla en inglés y español | M | C2, C3 | Tests de los cuatro estados; la razón nunca depende de un LLM; `population` rotula su referencia |
| C5 | Escenario simulado: tripulación ficticia con historial clínico en la Tierra y viaje Tierra → nave → Marte (R+0 a R+3), con caso gris y pulso manual | M | C1 | Genera `Measurement` con `source: simulated-scenario`; incluye los cuatro estados; reproducible con una semilla |
| C6 | Puerto `DeviceSource` y adaptador simulado de reloj y banda (D-011) | M | C1 | El motor consume lecturas del simulador sin cambiar; el adaptador se puede sustituir en un test |
| C7 | Perfil de nave `iss-analog`: verificar con fuente los equipos de la ISS, qué indicadores habilitan y qué ejercicios proponen, con cita (D-016) | S | C1 | Archivo de perfil con cada equipo respaldado por una URL; lo no verificado queda marcado [HUECO] y fuera |
| C8 | Exportación FHIR R4: `Observation` de signos vitales (LOINC) y códigos locales para estados, líneas base y medidas acústicas; `Bundle` | S | C1 | El Bundle valida contra la estructura FHIR; sin consentimiento no se genera (D-006) |

## Carril A · App del astronauta (`astronaut`)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| A1 | **Spike de offline:** probar `flet build web --no-cdn` o el servidor local sin internet, con la versión fijada; registrar el resultado | M | H1 | La app abre y responde con la red desconectada, o queda registrado el fallo y la salida a TypeScript (D-017). **Bloquea todo el carril** |
| A2 | Estructura de la app, cambio de idioma español/inglés y persistencia local en SQLite detrás de un puerto de almacenamiento | M | A1, C1 | Cambiar de idioma actualiza toda la pantalla; los datos sobreviven a un reinicio; el almacenamiento se puede sustituir en un test |
| A3 | Figura corporal con arte SVG y zonas clicables, coloreada por `SystemStatus` | M | A2, C4 | Cada sistema abre su tarjeta; el color sale del estado y no está fijo en el código |
| A4 | Tarjeta del sistema: tendencia con banda, explicación simple, orientación con cita y checklist | M | A3 | Cada afirmación de orientación tiene su cita; sin diagnóstico ni dosis |
| A5 | Entrada manual del pulso: el astronauta cuenta y la app calcula, con el gráfico explicativo | M | A2, C3 | Un conteo produce un `Measurement` con `method: palpation` |
| A6 | Burbuja de ánimo: encuesta clásica, luego conversación opcional por voz con un LLM; la conversación no se guarda; se guardan solo medidas acústicas numéricas (D-015) | M | A2 | La encuesta mueve el estado de `mood`; la conversación no queda en SQLite; las medidas acústicas no mueven ningún estado |
| A7 | Reproductor del viaje: cambio de espacio y rótulos de referencia de transición | M | A3, C5 | Se recorre Tierra → nave → Marte y la figura cambia; cada estado muestra contra qué referencia se comparó |
| A8 | Recordatorios de rutina del escenario simulado | M | A7 | Aparece el recordatorio del día con la medición pedida |
| A9 | Pantalla "Limits": datos análogos, nada validado en órbita, sin diagnóstico | M | A2 | Visible desde cualquier pantalla, en ambos idiomas |
| A10 | Escalamiento: sugiere, el astronauta confirma y se envía un Bundle a la base con el retraso simulado | S | A4, C8, G1 | Sin confirmación no sale nada; con ella llega a `ground` |
| A11 | Pantalla fija de emergencia en la nave (¿respira?, ¿responde?, escalar y seguir el procedimiento oficial) | S | A2 | Sin pasos clínicos propios (D-016) |
| A12 | Racha de adherencia: premia medir con regularidad, nunca "estar sano" | S | A5 | La racha depende de mediciones hechas, no de su valor |
| A13 | Voz como entrada y salida (dictar datos, leer guías) | S | A2 | Un dato dictado produce el mismo `Measurement` que el manual |

## Carril G · Base en Tierra (`ground`)

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| G1 | Servicio FastAPI con SQLite que recibe y valida Bundles FHIR (D-018) | M | C8 | Un Bundle válido se guarda; uno inválido se rechaza con error claro |
| G2 | Cola de retraso de comunicación simulado y configurable (~3 a 22 min) | M | G1 | Lo enviado aparece en la base pasado el retraso; el retraso se configura |
| G3 | Interfaz de la base (flight surgeon): estado por tripulante, Bundles recibidos y resumen del escalamiento, en español e inglés. [SUPOSICION] Flet por coherencia con `astronaut`; falta decidirlo | M | G2 | Solo muestra lo que el astronauta envió; no muestra datos crudos ni conversaciones |
| G4 | Vista de tendencias de lo recibido | S | G3 | Gráfico por indicador con la banda enviada |

## Carril P · Producto, relato y envío

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| P1 | Leer la Project Submission Guide y la Judging & Awards Guide (publicadas el 13 nov) y completar [submission-checklist.md](submission-checklist.md) | M | — | Cada [HUECO] del checklist queda resuelto o justificado |
| P2 | Guion y storyboard de la demo de 30 s (Tierra → nave → Marte) y versión de 7 slides | M | A7 | Guion en inglés con subtítulos; muestra el gris, el color relativo y la privacidad |
| P3 | Grabar el video y alojarlo en un enlace público externo | M | P2 | Se abre en una ventana privada sin pedir registro |
| P4 | Página del proyecto en inglés con todos los campos obligatorios y referencias | M | P1 | Campos completos; cita los datos de NASA y de la CSA usados |
| P5 | Descripción del uso de IA en inglés a partir de [uso-de-ia.md](uso-de-ia.md) | M | — | Resume las herramientas usadas y qué revisó el humano |
| P6 | Preparar el repositorio público: README, licencia, citas de datos, sin logos de NASA | M | — | Licencia decidida; ningún dato con licencia no confirmada |
| P7 | Verificar que todos los integrantes están registrados en el mismo evento local | M | — | Lista confirmada antes del envío |
| P8 | Envío completo con margen y verificación de enlaces | M | P3, P4, P5, P6 | Enviado antes del domingo 23:59; enlaces probados |

## Carril Q · Integración

| ID | Tarea | Nivel | Dep | Hecho cuando |
|---|---|---|---|---|
| Q1 | Flujo de punta a punta: viaje simulado → escalamiento → recepción en la base | M | A10, G3 | Un guion automático lo recorre sin errores |
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
