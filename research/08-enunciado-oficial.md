# 08 - Enunciado oficial del reto (publicado el 28 oct 2026)

Fecha de lectura: 2026-10-28. Etiquetas: [VERIFICADO] / [SUPOSICION] / [HUECO].
Fuente: https://www.spaceappschallenge.org/2026/challenges/create-health-monitoring-software-for-astronauts-on-space-missions/
Cómo se leyó: la página carga contenido dinámico; se consultó la API pública `https://api.spaceappschallenge.org/graphql` (consulta `page(id: "aWQ6NTUxMzA=")`, con cabecera `Origin: https://www.spaceappschallenge.org`).

## 1. Resumen del enunciado [VERIFICADO]

- **Título:** Create Health Monitoring Software for Astronauts on Space Missions. Habilidades: Human Exploration, Software, Space Exploration.
- **Problema:** en misiones largas, los astronautas están expuestos a radiación, aislamiento, gravedad alterada y un ambiente cerrado hostil, con riesgos inmunes, de pérdida ósea, cardiovasculares y de salud conductual. En misiones largas, **ellos mismos** deben detectar estos cambios.
- **Objetivo literal:** crear una **herramienta visual** que ayude a los astronautas a **evaluar su propia salud** durante la misión y que **oriente sobre tratamientos y mejoras de salud**.
- **Entrada de datos:** cualquier tipo: texto por teclado, clics o imágenes de cámara. Cualquier dato vale si representa un indicador de salud (p. ej. glucosa en mg/dL o imágenes de ecografía).
- **Indicadores de ejemplo:** presión arterial, frecuencia cardíaca, glucosa, temperatura corporal, horas de sueño diarias y estado de ánimo.
- **Fuentes sugeridas:** recursos del Human Research Program (HRP) de NASA y recursos públicos de otras agencias, para decidir qué indicadores son útiles.
- **Preguntas guía:** qué mediciones se pueden hacer en el espacio; por qué hace falta un examen; cómo afectan los peligros del vuelo a los indicadores; **cuándo un resultado amerita atención de la tripulación o de los flight surgeons en tierra**; qué acciones previenen un cuadro crítico.
- **Interfaz:** se destaca su importancia. Se sugieren animaciones e interactividad; el ejemplo es una **figura humana con partes clicables** que muestran su función y su estado de salud.
- **Consideraciones opcionales:**
  - Distintos entornos: nave, estación espacial, rover, base en otro planeta o luna.
  - Pedir mediciones o acciones periódicas como parte de la rutina de la misión.
  - Gamificación para mantener tareas de salud.
  - Gráficos dinámicos de la evolución de los indicadores.
  - Código de colores para leer el estado de un vistazo.
  - No asumir que el astronauta sabe evaluar su salud: dar instrucciones y explicaciones simples sobre mediciones, indicadores y riesgos.
- **Recursos:** la pestaña Resources dice "Resources will be available on Friday, November 13."

## 2. Reglas generales 2026 confirmadas en el FAQ oficial [VERIFICADO]

Fuente: https://www.spaceappschallenge.org/resources/participant-faqs/ (leída por la misma API, página `aWQ6MTIzMTk=`).

- Equipos de 1 a 6 personas; un equipo trabaja un solo reto.
- El envío se hace desde la página del proyecto del equipo. La Project Submission Guide y la Judging & Awards Guide se publican el **13 nov**.
- **Uso de IA (en 2026 llamada "Super Intelligence", SI):** está permitido usar LLM, asistentes conversacionales, generadores de imagen y video, modelos fundacionales y generadores de código. **Cada envío debe incluir una descripción de cómo se usaron estas herramientas** durante el desarrollo.
- Reconocimientos: Honorable Mentions, Global Finalists y Global Winners; los criterios se detallarán en la guía del 13 nov.

### 2b. Correo oficial "Challenge Statements are Live!" (NASA Space Apps GO Team, recibido el 28 oct 2026)

Fuente: correo recibido por el equipo (sin URL pública; texto pegado por un integrante).

- [VERIFICADO] **No empezar a trabajar en el proyecto hasta el 14 nov 2026 a las 9:00 (hora local)**, por equidad. Antes de esa hora sí se permite elegir el reto, investigar el tema y formar el equipo.
  - [SUPOSICION] "Hora local" se refiere a la del evento local en el que esté inscrito el equipo. Para Ecuador continental (UTC-5, sin horario de verano) eso es el 14 nov a las 14:00 UTC. Galápagos está en UTC-6, así que la hora cambiaría si el evento fuera allí. Hay que confirmar en qué evento local está inscrito el equipo.
  - [SUPOSICION] Lo que llevamos (investigación, idea base, reglas del equipo y contrato de datos como propuesta) entra en "investigar y preparar". Escribir código del motor o de la app, diseñar pantallas finales o grabar material del pitch antes de esa hora no entra.
- [VERIFICADO] Los recursos del reto se publican el 13 nov.
- [VERIFICADO] Para optar a premios globales, **todos los integrantes deben estar inscritos en el mismo evento local**. Un equipo de evento local necesita al menos 1 persona; uno del evento universal (virtual), al menos 2. Máximo 6 integrantes.

## 3. Qué cambia respecto a la investigación previa

- [VERIFICADO] El usuario principal es el **astronauta que se autoevalúa**, no el CMO. El CMO y los flight surgeons aparecen como **destino del escalamiento**.
- [VERIFICADO] La orientación (guidance) sobre tratamientos y mejoras forma parte del objetivo, no es un extra.
- [VERIFICADO] Se pide explícitamente una interfaz visual con colores, gráficos e interactividad.
- [SUPOSICION] El enunciado no menciona el retraso de comunicaciones ni el modo offline; solo nombra la "distancia a la Tierra" como peligro. El offline pasa a ser un marco narrativo, no el centro.
- [SUPOSICION] Como el propio enunciado sugiere la figura corporal clicable, muchos equipos la harán: por sí sola no diferencia.
- [HUECO] Datasets oficiales y criterios de juicio 2026 (13 nov).

## Anexo: GitHub Discussions del reto (2026-11-06)

Fuente: https://github.com/nasa/spaceapps/discussions (filtro "Health Monitoring Software for Astronauts"). Las lecturas se hicieron con un resumidor automático de páginas, no son citas literales: verificar el texto exacto antes de citarlo en el pitch.

- **#1787 "Prototype or Real Product?"** (https://github.com/nasa/spaceapps/discussions/1787), respuesta aceptada de Nick-GO-Team (Maintainer, 4 nov 2026):
  - [VERIFICADO] El GO Team no espera una solución terminada al final del hackathon; se quiere ver progreso hacia una solución. Frase clave resumida: "We do not expect you to have a completely finished, fully-developed solution by the end of the hackathon."
  - [VERIFICADO] Un equipo sin datos reales de salud espacial preguntó si vale una API simulada o datos ficticios, y el GO Team confirmó que está bien.
  - [VERIFICADO] Los datos y recursos aparecerán en la pestaña "Resources" del reto cuando empiece el hackathon.
  - **Efecto:** el hardware real no parece obligatorio; la capa `DeviceSource` (D-011) sigue siendo una cobertura, no un requisito.
- **#1772 "Health Monitoring Software Resources availability"** (https://github.com/nasa/spaceapps/discussions/1772): [VERIFICADO con reservas] la respuesta aceptada es de otro participante (no del GO Team) y dice que los recursos estarán el viernes 13-11-2026 y que no se permite trabajo de proyecto antes del hackathon. Coincide con el correo oficial del 28 oct (sección 2b), pero no es una fuente oficial por sí misma.
- #1769 (Navigating Space Apps Connect) y #1768 (Code of Conduct): hilos fijados del GO Team, no leídos.
- [HUECO] No hay hilos con datasets, requisitos de hardware ni criterios de evaluación en esa vista.
