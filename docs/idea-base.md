# Idea base del proyecto

Estado: **propuesta v1 (2026-10-28)**, pendiente de que el equipo la confirme. Cualquier cambio de alcance se registra en [decisiones.md](decisiones.md).
Base: enunciado oficial ([research/08](../research/08-enunciado-oficial.md)) + investigación previa ([research/04](../research/04-ideas.md), [research/07](../research/07-angulos-de-idea.md)).
Etiquetas: [VERIFICADO] / [SUPOSICION] / [HUECO]. Las puntuaciones son estimaciones propias.

## 1. En una frase

Una herramienta visual con la que el astronauta **se compara consigo mismo**: el color de cada sistema del cuerpo depende de **su propia línea base**, no de un umbral poblacional. Además, le dice qué hacer y cuándo escalar a la tripulación o a Tierra, y **se pone en gris cuando no tiene datos suficientes para opinar**.

Nombre provisional: **Crew Self-Check** (por definir).

## 2. Reanálisis de los conceptos frente al enunciado oficial

| Concepto (research/04) | Relevance antes | Relevance ahora | Papel en la idea base |
|---|---|---|---|
| A Línea base + incertidumbre + abstención | 4 | 4 | **Motor y diferenciador.** Le da significado al código de colores que pide el enunciado |
| B Offline + retraso de comunicaciones | 5 | 3 | Marco del **escalamiento**: el aviso a Tierra llega con retraso, así que se actúa primero a bordo |
| C Tendencias multidominio + OSDR | 4 | 3 | Solo como contexto, si sobra tiempo |
| D Panel + contramedidas | 3 | 5 | **Cáscara visible:** gráficos, colores, orientación y rutina, todos pedidos por el enunciado |
| E Insight Lab (investigadores) | 2 | 1 | Descartado: el usuario del enunciado es el astronauta |
| Tarjeta de decisión del CMO (07, ángulo 2) | — | — | Se convierte en la **tarjeta del sistema** para el astronauta, con el CMO como escalamiento |
| PVT-B de 3 min (07, ángulo 3) | — | — | Opcional: es una "medición que se puede hacer en el espacio" |

[SUPOSICION] Riesgo principal: D y la figura corporal son lo que sugiere el enunciado, así que muchos equipos los harán. Lo que nos diferencia sale de A + B:
1. **Color relativo a la persona**: verde significa "dentro de tu rango", no "dentro del rango de un terrícola promedio".
2. **Gris honesto**: "aún no te conozco lo suficiente; mide N días más". Evita las falsas alarmas y la falsa tranquilidad.
3. **Escalamiento con conciencia del retraso**: autocuidado → CMO a bordo → flight surgeon en Tierra (respuesta en ~X min).
4. **Gamificar la adherencia, no la salud**: la racha premia medir con regularidad, porque más datos dan una línea base mejor. Nunca se premia "estar sano".

## 3. Usuario y escenario

- **Usuario principal:** astronauta sin formación médica, en una misión larga (tránsito a Marte o base lunar).
- **Usuarios secundarios:** CMO de la tripulación y flight surgeon en Tierra, que reciben un resumen cuando se escala.
- **Escenario de demo:** tripulación ficticia de 3 o 4 personas y una misión simulada de N días, acelerada en la interfaz.

## 4. Flujo de la demo (30 s): llegada a Marte (D-007)

Escenario con base documental ([research/09](../research/09-humanos-en-el-espacio.md), sección 3): la tripulación aterriza tras ~6-9 meses en microgravedad y debe arreglarse sola. Es el momento de mayor riesgo sensoriomotor según NASA; el análogo real es la Expedición 6, que pasó ~5 h sin rescate.

1. **Recordatorio de rutina (día R+0):** "Chequeo de llegada: prueba de pie (FC y presión acostado → de pie), síntomas vestibulares, marcha en tándem y visión".
2. **Figura corporal:** los sistemas se colorean según la línea base del propio tripulante **antes del vuelo**. Cardiovascular pasa a ámbar (taquicardia al pararse) y vestibular a rojo (náusea y mareo).
3. **Clic en un sistema → tarjeta:** qué mide, por qué cambia al aterrizar (cita NASA), la tendencia con su banda y qué hacer en formato checklist: descansar, hidratarse, **no hacer EVA ni conducir el rover**.
4. **Caso gris:** la glucosa es un análisis ocasional; sin datos recientes se muestra gris y no "normal".
5. **Escalamiento privado:** el astronauta decide compartir un resumen con el CMO; el resumen a Tierra sale de forma asíncrona ("llega en ~12 min").
6. **Evolución R+0 → R+3:** la tendencia muestra la recuperación de los primeros días.

## 4b. Principios de diseño que salen de la evidencia

- **Privado por defecto (D-006):** los datos crudos solo los ve el astronauta; compartir con el CMO o con Tierra es su decisión. La app aclara que los datos no se usan para decidir si sigue apto para la misión. Motivo: el miedo a la descalificación es la causa documentada del subreporte (*Safe Passage*, IOM 2001).
- **El escalamiento sugiere, no notifica automáticamente.**
- **Modo entorno:** cambia qué se pregunta y qué se prioriza (tránsito, Luna, Marte, rover), no los umbrales clínicos.
- **Checklist, no diagnóstico:** el CMO no es médico (~25 h de entrenamiento).
- **Glucosa de baja frecuencia:** en la ISS no se mide a diario.

## 5. Alcance (MoSCoW, equipo de 3, 48 h)

- **Must**
  - Entrada manual de indicadores y carga de series de ejemplo (Sleep-Accel ya descargado; tripulación ficticia).
  - Motor de línea base por persona e indicador: mediana con banda robusta y desviación sostenida; estado `insufficient_data` (gris).
  - Figura corporal clicable con el color de cada sistema.
  - Tarjeta del sistema: tendencia con banda, explicación simple, orientación y cita.
  - Recordatorios de rutina en el escenario simulado.
  - Pantalla "Limits": datos análogos y nada validado en órbita.
- **Should:** escalamiento con simulador de retraso; racha de adherencia.
- **Could:** PVT-B; contexto ambiental (DONKI/SWPC); varios entornos (nave, base).
- **Won't:** diagnóstico, umbrales clínicos inventados, LLM en la ruta crítica de alertas, hardware y datos personales reales.

## 6. Datos

- Hasta el 13 nov: Sleep-Accel (FC y sueño), entradas simuladas de la tripulación ficticia y contenido del HRP (riesgos y contramedidas) para las tarjetas. OSDR es opcional.
- El 13 nov: incorporar los recursos oficiales del reto mediante el adaptador del [contrato de datos](contrato-datos.md), sin tocar la interfaz.
- [VERIFICADO, guía 2022] Hay que usar al menos algunos datos abiertos de NASA o de agencias socias. [HUECO] Confirmarlo en la guía 2026.

## 7. Estimación frente a los criterios (1-5, [SUPOSICION])

Impact 4 · Creativity 3-4 (por el color relativo y el gris) · Validity 4 · Relevance 5 · Presentation 4. Total estimado: 20-21 de 25. Escala real 2026: [HUECO] hasta el 13 nov.

## 8. Preguntas abiertas para el equipo

- Stack y persistencia: se deciden el 13 nov con los datasets oficiales (criterios en [decisiones.md](decisiones.md), D-003).
- Elegir el nombre definitivo.
- Decidir qué 4 o 5 sistemas del cuerpo entran en el Must.
- Ideas por analizar (2026-10-28): **voz** (STT para ingresar datos y TTS para leer guías e instrucciones) y **análisis de imágenes**, que el equipo considera obligatorio. Pendiente de análisis: viabilidad offline, privacidad (D-006) y cómo evitar el diagnóstico automático.
