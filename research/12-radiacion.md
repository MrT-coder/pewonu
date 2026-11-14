# 12. Radiación: análisis del artículo de la CSA y qué hacer en el proyecto

Fuente: Agencia Espacial Canadiense (CSA), *Monitoring Radiation for Astronaut Health*, 26 feb 2026. https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp
Leída completa el 2026-11-14. Etiquetas: [VERIFICADO] respaldado por la fuente; [SUPOSICION] inferencia propia; [HUECO] por confirmar. Motivo: la radiación es uno de los cinco peligros del HRP y el proyecto aún no la trata.

## 1. Qué dice el artículo [VERIFICADO]

- La CSA otorgó un contrato de "$5.5 million" a Bubble Technology Industries para seguir desarrollando el **CANS** (*Canadian Active Neutron Spectrometer*), "a compact and autonomous instrument designed to measure neutron radiation exposure in space". Funciona "continuously and autonomously".
- La radiación es "one of the key challenges" para quien sale de la atmósfera. La de neutrones "can cause serious biological damage" y exige medidas de protección especializadas.
- Los neutrones aportan "about 30%" de la radiación total en la ISS.
- Antecedentes canadienses: MOSFET, EVARM, Radi-N y Radi-N2, y los detectores de burbujas que usó David Saint-Jacques en la ISS, predecesores del CANS. La ISS se menciona como banco de pruebas de tecnología.
- Canadá y sus socios avanzan planes para misiones a la Luna "and eventually Mars".
- Los datos "could help develop better measures to reduce risks for astronauts' health". Aplicaciones en la Tierra: terapia contra el cáncer, protección de tripulaciones aéreas, detección de amenazas nucleares y seguridad pública.

## 2. Lo que el artículo NO dice [VERIFICADO: la página no lo trae]

- **Qué magnitud mide** el CANS (dosis, flujo u otra), su método ni sus rangos de energía.
- Si el "30 %" es de dosis o de otra cantidad: **no se puede citar como parte de la dosis**.
- En qué nave o misión volará (Gateway no se menciona).
- Límites o umbrales de exposición, ni efectos concretos más allá de "serious biological damage".
- Alertas en tiempo real, ni si los datos llegan al astronauta.

## 3. Lo que ya teníamos

- La radiación es uno de los cinco peligros del HRP y su riesgo se llama "cánceres inducidos por radiación". [VERIFICADO, [research/11](11-recursos-oficiales.md)]
- Tasas de dosis equivalente por espacio. [VERIFICADO con reservas: el cuaderno de NotebookLM las confirmó contra sus fuentes con cita textual ([notebooklm-verificacion.md](notebooklm-verificacion.md)); el equipo **no abrió** los artículos, así que hay que abrirlos antes de ponerlas en una diapositiva]

| Dónde | Tasa | Fuente según el cuaderno |
|---|---|---|
| Superficie de Marte | 0.64 ± 0.12 mSv/día (rayos cósmicos galácticos) | Hassler et al. 2014, *Science* |
| Superficie de la Luna | 1369 µSv/día (día lunar) | Zhang et al. 2020, *Science Advances* |
| ISS | 0.647 mSv/día | *Eur. Phys. J. Plus* 2026 |
| Tránsito Tierra-Marte | 1.84 mSv/día | *Eur. Phys. J. Plus* 2026 |

  Son medidas de instrumentos y condiciones distintas: no se comparan como si fueran la misma cosa.
- Un *wearable* no mide la radiación de forma biológica; solo registra dosis física con un dosímetro. [SUPOSICION, [research/01](01-fisiologia.md)]
- Dosis acumulada y tasa de dosis se miden con dosímetros personales o de área. [SUPOSICION, no se verificó el modelo usado en la ISS]

## 4. Análisis

1. **La radiación es una exposición física, no una señal del cuerpo.** Nuestro motor compara a la persona consigo misma, pero aquí no hay un "normal personal": la dosis se acumula y depende del lugar. [SUPOSICION]
2. **Sí encaja con nuestro eje de espacios.** La tabla de arriba muestra que la tasa cambia mucho entre la ISS, el tránsito y la superficie. Una serie de tasa de dosis **por espacio** sería natural en nuestro modelo. [SUPOSICION]
3. **No podemos ponerle un color.** El artículo no publica límites, y `AGENTS.md` (sección 6) prohíbe inventar umbrales. Un verde, ámbar o rojo de radiación sería un umbral inventado. Los límites los fijan las agencias.
4. **No podemos medirla.** El CANS es un instrumento dedicado; nuestra app no tiene sensor de radiación. Lo que sí podría hacer es **recibir** lecturas de un dosímetro a bordo: el puerto `DeviceSource` (D-011) es el lugar para eso.
5. **Callar sobre la radiación es un hueco visible.** El HRP la lista primero y el ganador de 2025 en "Best Use of Science" trató radiación ([research/05](05-ganadores.md)). Mejor decir con claridad qué no medimos y por qué. [SUPOSICION]
6. **Cuidados:** no sugerir una relación causal entre radiación y fisiología sin base ([research/07](07-angulos-de-idea.md), ángulo 6); no citar el 30 % como dosis; no comparar tasas de instrumentos distintos como equivalentes; no sugerir seguridad ni peligro.

## 5. Opciones

| | Qué es | Costo | Riesgo | Contrato |
|---|---|---|---|---|
| **A. Tarjeta de contexto** (recomendada) | En la vista del cuerpo, una tarjeta "Radiación: no la medimos aquí" fuera de los seis sistemas. Explica por qué importa (HRP), qué mide un instrumento como el CANS (CSA) y que se necesita un dosímetro. | Bajo: reutiliza la tarjeta del sistema | Ninguno: no hay datos ni umbrales | No cambia |
| **B. Dosímetro simulado** (Could, D-016) | Un adaptador `DeviceSource` que entrega una tasa de dosis simulada por espacio, rotulada como simulada. Se muestra el valor y la tendencia, **sin color**. | Medio | Que parezca una medición real o un estado | Nuevo indicador `radiation_dose_rate` y unidad: requiere decisión y subir a `0.4` |
| C. Contexto de clima espacial | Alinear eventos solares con las tendencias (ángulo 6) | Alto | Sugerir causalidad sin base | Nuevo origen de datos |
| D. Integrar un CANS real | | No viable: no hay hardware ni datos | n/a | n/a |

## 6. Recomendación

1. **Hacer A ahora**, junto a la figura corporal: una tarjeta informativa, con cita del HRP y de la CSA, la frase de límites y el aviso de que no se calcula ningún estado. Añadirla a la pantalla "Límites" y a las diapositivas.
2. **B solo si sobra tiempo** después de la figura, el envío y la base en Tierra. Muestra que la arquitectura recibe un dosímetro sin tocar el motor.
3. **No hacer C ni D.**
4. Frase para el envío: *"Radiation is a major hazard and Crew Self-Check does not measure it: that needs a dedicated dosimeter. Our device port is designed to take such readings, and we show no radiation status because no validated limits are ours to invent."*

Propuesta para el equipo (no está registrada como decisión): **D-025**, radiación como contexto informativo (opción A), sin estado ni umbrales; la opción B queda como Could.

## 7. Qué cambiaría en la documentación si se acepta

- [tareas.md](../docs/tareas.md): una tarea **A14** (Should) para la tarjeta de contexto, y **C9** (Could) para el dosímetro simulado.
- [idea-base.md](../docs/idea-base.md): la pregunta abierta sobre radiación pasa a decisión.
- [submission-pack.md](../docs/submission-pack.md): una línea en la diapositiva 6 y en los límites.

## 8. Huecos

- [HUECO] Qué magnitud mide el CANS y si su dato llega al astronauta.
- [HUECO] Abrir los cuatro artículos de la tabla de tasas antes de usarlas.
- [HUECO] Qué dosímetros personales usan realmente las tripulaciones (no se verificó).
- [HUECO] Límites de exposición de las agencias: no se leyeron y **no son nuestros** para fijar.
