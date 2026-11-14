# 02 - Estado del arte: monitoreo de salud de astronautas

Etiquetas: [VERIFICADO] respaldado por fuente citada; [SUPOSICION] inferencia propia; [HUECO] no encontrado.
Metodo: busqueda web y lectura de resumenes/paginas; muchos PDF de NTRS aparecieron solo como resultados de busqueda y no se leyeron completos.

## 1. Human Research Program (HRP) y Human Research Roadmap
- [VERIFICADO] HRP organiza el riesgo en 5 peligros (radiacion, aislamiento/confinamiento, distancia de la Tierra, gravedad, ambientes hostiles/cerrados) y publica una lista de riesgos: https://www.nasa.gov/hrp/risks
- [VERIFICADO] Elemento Exploration Medical Capability (ExMC): aborda el riesgo "Inability to Adequately Recognize or Treat an Ill or Injured Crewmember"; usa la Exploration Medical Condition List para identificar condiciones y brechas (gaps); datos en el Human Research Roadmap y la Human Research Wiki. Fuente (resultado de busqueda): https://ntrs.nasa.gov/citations/20100028273
- [HUECO] No se abrio el Human Research Roadmap en linea (humanresearchroadmap.nasa.gov) ni se obtuvo la lista actual de gaps; verificar manualmente.

## 2. Monitoreo actual en la ISS
- [VERIFICADO] Crew Health Care System (CHeCS): Health Maintenance System (HMS), Countermeasures System y Environmental Maintenance System. HMS da soporte vital, atencion medica y monitoreo de salud. Fuente: https://ntrs.nasa.gov/api/citations/20110011351/downloads/20110011351.pdf (via resultado de busqueda).
- [VERIFICADO] Equipos: muestreo de sangre/orina, ECG, tensiometro y ecografo; el ecografo HRF es el unico dispositivo de imagen diagnostica manifestado. Misma fuente.
- [VERIFICADO] Crew Medical Officer (CMO): astronauta a cargo de operaciones medicas; dos CMO por tripulacion de 3 en ISS, normalmente no medicos. Fuente: resultados de busqueda sobre https://ntrs.nasa.gov/api/citations/20110011351/downloads/20110011351.pdf y NTRS relacionados (cifra exacta a contrastar).
- [VERIFICADO] Bio-Monitor/Astroskin (CSA): camiseta e cinta con FC, respiracion, SpO2, presion, temperatura, actividad, HRV y calidad de sueno; desplegado en ISS en dic. 2018 por D. Saint-Jacques y validado por L. Parmitano (ESA). Fuente: https://wt-obk.wearable-technologies.com/2018/09/astroskin-smart-shirt-will-monitor-astronauts-vital-signs-in-space/
- [VERIFICADO] ASI/IIT: proyecto de monitoreo continuo del sueno con mascara (FC, respiracion, temperatura, movimiento, EEG) y algoritmos de IA. Fuente: https://magazine.unibo.it/en/articles/how-astronauts-sleep-in-space
- [VERIFICADO] JAXA publica su sistema de operaciones medicas/atencion de salud: https://humans-in-space.jaxa.jp/en/biz-lab/med-in-space/healthcare/medops/system (contenido no leido).
- [HUECO] No se verifico en detalle el esquema de vigilancia medica de ESA ni el de Roscosmos; solo hay menciones indirectas (Parmitano, Mars-500 con IMBP/ESA).

## 3. Analogos en tierra
- [VERIFICADO] CHAPEA: primera mision de 3 planificadas; 4 voluntarios, 378 dias en un habitat impreso en 3D de ~158 m2 (1,700 ft2) en JSC, del 25 jun 2023 al 7 jul 2024; incluye caminatas simuladas, operaciones roboticas, ejercicio y cultivo; roles incluyen oficial medico. Fuentes: https://www.space.com/chapea-yearlong-mars-analog-mission-begins y https://www.nasa.gov/?p=439942
- [HUECO] No se encontraron resultados publicados de salud de CHAPEA 1 en esta busqueda.
- [VERIFICADO] Mars-500 (IMBP/ESA/Roscosmos): 520 dias, 6 voluntarios; hallazgos de sueno y actividad (ver 01-fisiologia.md). Fuente: https://whyy.org/articles/psychological-hazards-of-exploration-lessons-from-a-mock-mars-mission/
- [VERIFICADO] NASA Twins Study (2015-16) como referencia multi-omica de un ano: https://news.weill.cornell.edu/news/2019/09/heavenly-bodies-nasa%E2%80%99s-famed-twins-study-has-begun-to-yield-results

## 4. Autonomia medica y Earth-Independent Medical Operations (EIMO)
- [VERIFICADO] EIMO Concept of Operations (Parker, Krihak, Laing, Bardina, Parmar, Anderson): transferir progresivamente el cuidado de controladores en Tierra a sistemas a bordo, ante retrasos de comunicacion e imposibilidad de evacuacion; el sistema medico integra datos de sensores portables, diagnostico en punto de atencion y control ambiental, con bases de referencia; apoya al CMO con herramientas de entrenamiento. Fuente: https://ntrs.nasa.gov/citations/20250000009
- [VERIFICADO] Limites de recursos: sin reabastecimiento, masa, energia, volumen y datos restringidos (resumen de busqueda del mismo documento).
- [VERIFICADO] Brecha de HRP: entrenamiento optimo del CMO segun su formacion clinica (gap 3.01). Fuente: https://ntrs.nasa.gov/citations/20100028273 (resultado de busqueda; confirmar numeracion vigente).

## 5. Retraso de comunicaciones a Marte
- [VERIFICADO con reservas] Retraso unidireccional de ~3 a 22 min segun geometria orbital (otras fuentes dicen 3-21 o hasta ~20). Fuentes: https://ntrs.nasa.gov/citations/20250000009 (via resumen de busqueda) y https://reference-global.com/download/article/10.2478/asam-2024-0001.pdf. Conviene citar el rango, no un valor unico.
- [SUPOSICION] Consecuencia de diseno: alertas locales (edge) sin depender del enlace; sincronizacion diferida con tierra. Coherente con EIMO pero no es requisito oficial.

## 6. IA de apoyo medico
- [VERIFICADO] NASA y Google trabajan en CMO-DA (Crew Medical Officer Digital Assistant), asistente de IA para guiar diagnostico y manejo paso a paso. Fuente (blog, no primaria): https://www.innovaspace.org/blog/google-nasas-digital-assistant-a-space-doctor-for-mars. [HUECO] No se localizo comunicado primario de NASA/Google.

## 7. Implicaciones para el hackathon
- [SUPOSICION] Nicho: capa de analitica local de bajo consumo que fusione wearables (HRV, sueno, actividad, SpO2, temperatura) con linea base individual y avise al CMO, con modo offline y trazabilidad.
- [SUPOSICION] Diferenciador frente a Astroskin/CHeCS: tendencias multi-dominio (inmune/cardio/conductual) y apoyo a decision, no solo captura.
- [HUECO] Falta verificar: requisitos de privacidad medica de NASA (p. ej. politica de datos de astronautas), datasets abiertos utilizables (NASA OSDR/Lifetime Surveillance of Astronaut Health) y formatos; investigar antes de disenar.
