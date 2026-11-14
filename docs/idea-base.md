# Idea base del proyecto

Estado: **v2 (2026-11-14)**, actualizada con las decisiones D-013 a D-022 de [decisiones.md](decisiones.md). Sustituye a la v1 del 28 oct, cuyo stack (SPA en TypeScript) y varios puntos de alcance cambiaron. Cualquier cambio de alcance se registra en `decisiones.md`.
Base: enunciado oficial ([research/08](../research/08-enunciado-oficial.md)) + investigación previa ([research/04](../research/04-ideas.md), [research/07](../research/07-angulos-de-idea.md)).
Etiquetas: [VERIFICADO] / [SUPOSICION] / [HUECO]. Las puntuaciones son estimaciones propias.
Para el texto del envío y las diapositivas: [submission-pack.md](submission-pack.md).

## 1. En una frase

Una herramienta con la que el astronauta **se compara consigo mismo**: el estado de cada indicador depende de **su propia línea base**, por espacio (Tierra, nave, planeta), no de un umbral poblacional. Además, dice contra qué se comparó, **se pone en gris cuando no tiene datos suficientes para opinar** y comparte con Tierra solo lo que el astronauta decide enviar, en formato estándar FHIR.

Nombre: **Crew Self-Check** (el formulario del reto muestra "Project PeWoNu": confirmar cuál va como título).

## 2. Reanálisis de los conceptos frente al enunciado oficial

| Concepto (research/04) | Relevance antes | Relevance ahora | Papel en la idea base |
|---|---|---|---|
| A Línea base + incertidumbre + abstención | 4 | 4 | **Motor y diferenciador.** Le da significado al código de colores que pide el enunciado |
| B Offline + retraso de comunicaciones | 5 | 3 | Marco del **escalamiento**: el aviso a Tierra llega con retraso, así que se actúa primero a bordo |
| C Tendencias multidominio + OSDR | 4 | 3 | Solo como contexto, si sobra tiempo |
| D Panel + contramedidas | 3 | 5 | **Cáscara visible:** figura, colores, orientación y rutina, todos pedidos por el enunciado |
| E Insight Lab (investigadores) | 2 | 1 | Descartado: el usuario del enunciado es el astronauta |
| Tarjeta de decisión del CMO (07, ángulo 2) | — | — | Se convierte en la **tarjeta del sistema** para el astronauta, con el CMO como escalamiento |
| PVT-B de 3 min (07, ángulo 3) | — | — | Opcional: es una "medición que se puede hacer en el espacio" |

[SUPOSICION] Riesgo principal: D y la figura corporal son lo que sugiere el enunciado, así que muchos equipos los harán. Lo que nos diferencia sale de A + B:
1. **Color relativo a la persona**: verde significa "dentro de tu rango", no "dentro del rango de un terrícola promedio".
2. **Gris honesto**: "aún no te conozco lo suficiente; mide N días más". Evita las falsas alarmas y la falsa tranquilidad.
3. **Referencia de transición**: al entrar en un espacio nuevo se compara con la línea base del anterior y se rotula así (D-013).
4. **Escalamiento con conciencia del retraso**: autocuidado → CMO a bordo → flight surgeon en Tierra.
5. **Gamificar la técnica y la constancia, no la salud**: los puntos premian medir bien y con regularidad, nunca "estar sano" ni un valor (D-021).

## 3. Usuario y escenario

- **Usuario principal:** astronauta sin formación médica, en una misión larga (tránsito a Marte o base lunar). Entra con su **código único** (`AST-0000`, D-020).
- **Usuarios secundarios:** CMO de la tripulación y flight surgeon en Tierra, que reciben un resumen cuando el astronauta confirma el envío (D-018).
- **Escenario de demo (hecho, C5):** tripulación **ficticia** de dos personas en un viaje simulado de 28 días: 14 en la Tierra, 10 en la nave y la llegada a Marte (R+0 a R+3). `crew-01` tiene historial; `crew-02` no tiene y solo mide el pulso a mano, así que su estado sale de la referencia poblacional.

## 4. Arquitectura (D-017, D-018)

- Dos sistemas y un núcleo: `core` (contrato, motor de línea base, mapeo FHIR), `astronaut` (app Flet que corre a bordo, sin internet) y `ground` (FastAPI, recibe FHIR).
- Puertos y adaptadores: `core` es Python puro; las fuentes de datos (`DeviceSource`) y la exportación son adaptadores.
- **Nunca un LLM en la ruta de alertas.** Los estados y las razones son deterministas.

## 5. Flujo de la demo

Escenario con base documental ([research/09](../research/09-humanos-en-el-espacio.md), sección 3): la tripulación aterriza tras meses en microgravedad y debe arreglarse sola (D-007).

1. **Ingreso con código** y cambio de idioma español/inglés. *Hecho.*
2. **Chequeo diario.** *Hecho:* caritas de ánimo (cinco niveles) y **misión del pulso** (cuatro estaciones, la persona cuenta con los dedos en la muñeca durante 30 o 60 s y escribe cuántos latidos contó, puntos e insignia por la técnica).
3. **Estado calculado:** gris mientras la línea base madura; en la nave el sueño se marca contra la línea base de la Tierra (transición); al llegar a Marte suben el pulso y los síntomas vestibulares; el pulso manual de `crew-02` llega a rojo con referencia poblacional. *El motor está hecho (C3, C4, C5); falta mostrarlo en la interfaz.*
4. **Figura corporal y tarjeta del sistema** con tendencia, explicación simple, orientación con cita y checklist. *Pendiente (A3, A4).*
5. **Caso gris:** la glucosa es un análisis ocasional; sin datos recientes se muestra gris y no "normal". *Motor hecho.*
6. **Escalamiento privado:** el astronauta confirma qué enviar; llega a la base como un FHIR Bundle tras un retraso simulado. *Pendiente (A10, C8, G1 a G3).*
7. **Evolución R+0 → R+3:** reproductor del viaje. *Pendiente (A7).*

## 5b. Principios de diseño que salen de la evidencia

- **Privado por defecto (D-006):** los datos crudos solo los ve el astronauta; compartir con el CMO o con Tierra es su decisión. Motivo: el miedo a la descalificación es la causa documentada del subreporte (*Safe Passage*, IOM 2001).
- **El escalamiento sugiere, no notifica automáticamente.**
- **La voz no mueve ningún estado (D-015, D-019):** el ánimo es la encuesta de caritas; de la bitácora de audio solo se guardan medidas acústicas numéricas, sin etiquetas de emoción, y el audio se descarta.
- **Checklist, no diagnóstico:** el CMO no es médico (~25 h de entrenamiento). La orientación lleva cita y no receta medicamentos ni dosis.
- **Modo entorno:** la línea base es por espacio; no cambian los umbrales clínicos porque no los hay.
- **Glucosa de baja frecuencia:** en la ISS no se mide a diario.

## 6. Alcance (MoSCoW vigente: D-016 y D-021)

- **Must:** tres espacios con línea base y referencia de transición; pulso manual; ánimo por caritas; perfil de nave; figura corporal y tarjetas; escenario simulado de punta a punta; interfaz en ambos idiomas; acceso por código (D-020).
- **Should:** voz como entrada y salida; **exportación FHIR (C8)**; pantalla de emergencia; escalamiento con retraso; racha de adherencia.
- **Could:** análisis acústico (bitácora de audio); ejercicios por equipo; radiación y huesos simulados; caso con traje.
- **Won't:** diagnóstico, umbrales clínicos inventados, LLM en la ruta de alertas, inferir emoción de la voz, hardware y datos personales reales.

Estado tarea por tarea: [tareas.md](tareas.md).

## 7. Datos

- Todos los datos de la demo son **simulados y ficticios**, rotulados como tales (`source: simulated-scenario`).
- **No hay datos oficiales de salud de astronautas** ni datasets del reto ([research/11](../research/11-recursos-oficiales.md)). Se usan **recursos** de NASA (HRP, ARCHeR, Standard Measures) y de la CSA, citados en el envío.
- Referencia poblacional del pulso en reposo: NCHS NHSR nº 41 ([pulso-referencia.md](pulso-referencia.md)).
- Técnica del pulso manual: MedlinePlus (NIH), ver D-021.
- Sleep-Accel y WESAD figuraban en la v1; **no se usan** en el código actual.

## 8. Estimación frente a los criterios (1-5, [SUPOSICION])

Impact 4 · Creativity 3-4 (por el color relativo, el gris y el pulso gamificado) · Validity 4 · Relevance 5 · Presentation 4. Total estimado: 20-21 de 25. Escala real 2026: [HUECO], falta leer la guía de jueces.

## 9. Preguntas abiertas

- Nombre definitivo del proyecto (ver arriba).
- Licencia del repositorio y publicación del enlace público.
- Marca de agua visible en las imágenes generadas con IA (requisito del formulario, ver D-023).
- Si el rojo puede salir solo de la referencia poblacional (ver [pulso-referencia.md](pulso-referencia.md)).
- Qué cuatro o cinco sistemas del cuerpo entran en la figura (hay una propuesta en `core/status.py`).
- Análisis de imágenes: la v1 lo consideraba obligatorio; sigue sin analizarse (viabilidad offline, privacidad y no diagnosticar).
