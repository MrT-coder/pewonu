# 01 - Fisiologia del vuelo espacial y medicion

Etiquetas: [VERIFICADO] respaldado por fuente citada; [SUPOSICION] inferencia propia (no verificada en fuente); [HUECO] no encontrado.
Metodo: busqueda web y lectura de resumenes; no se leyeron los articulos completos salvo indicacion.

## 0. Marco: 5 peligros del HRP de NASA
- [VERIFICADO] El Human Research Program agrupa los riesgos en cinco peligros: radiacion espacial, aislamiento y confinamiento, distancia de la Tierra, campos de gravedad y ambientes hostiles/cerrados. Riesgos nombrados: sistema inmune alterado, adaptaciones cardiovasculares, cambios oseos, SANS, cambios conductuales y trastornos psiquiatricos, sueno inadecuado, cancer por radiacion. Fuente: https://www.nasa.gov/hrp/risks
- [VERIFICADO] Mas de 30 riesgos para la salud asociados a esos cinco peligros. Fuente (resumen de busqueda sobre pagina NASA): https://www.nasa.gov/hrp/risks

## 1. Radiacion espacial
| Aspecto | Evidencia | Estado |
|---|---|---|
| Cancer, dano al SNC, cambios cognitivos/motores y conductuales | Citados por el HRP | [VERIFICADO] https://www.nasa.gov/hrp/risks |
| Cataratas y enfermedad cardiovascular (por analogia con poblaciones irradiadas en Tierra) | Estudios epidemiologicos | [VERIFICADO] https://www.nasa.gov/hrp/risks |
| Twins Study: ~50 veces mas radiacion que el gemelo en Tierra; genes de reparacion de ADN activados; inversiones cromosomicas | Weill Cornell sobre Science 2019 | [VERIFICADO] https://news.weill.cornell.edu/news/2019/09/heavenly-bodies-nasa%E2%80%99s-famed-twins-study-has-begun-to-yield-results |

Indicadores medibles y sensores:
- Dosis acumulada y tasa de dosis: dosimetros personales/de area. [SUPOSICION] (no se verifico el modelo concreto usado en ISS).
- Biomarcadores: aberraciones cromosomicas, expresion genica, telomeros (sangre; analisis en tierra o laboratorio a bordo). Telomeros y expresion genica: [VERIFICADO] Twins Study (URL arriba).
- Un wearable NO mide radiacion biologicamente; solo registra dosis fisica. [SUPOSICION]
- Idea para el proyecto: correlacionar dosis ambiental (alertas de eventos solares) con tendencias de HRV/sueno. [SUPOSICION]

## 2. Microgravedad
### 2.1 Hueso
- [VERIFICADO] Se citan perdidas de 1-2 % de densidad osea por mes; en tripulantes de ISS 2.2-2.7 % mensual en hueso interior y 1.6-1.7 % en exterior; resistencia de cadera -2.5 % por mes. Fuente: resultados de busqueda que remiten a https://ntrs.nasa.gov/api/citations/20170004597/downloads/20170004597.pdf (no leido en detalle; cifras a confirmar en el original).
- Indicadores: DMO (DXA/QCT, solo en tierra), marcadores de recambio oseo en sangre/orina (NTX, P1NP; [SUPOSICION]), carga mecanica diaria.
- Sensores: acelerometros/IMU para contar impactos y minutos de ejercicio resistivo (proxy de carga osea) [SUPOSICION]. [HUECO] No hay wearable validado que mida DMO en orbita.

### 2.2 Cardiovascular
- [VERIFICADO] 6 de 11 tripulantes mostraron flujo estancado o retrogrado en la vena yugular interna (~dia 50) y 1 desarrollo un trombo oclusivo; LBNP mejoro el flujo en 10 de 17 sesiones. Fuente: https://pmc.ncbi.nlm.nih.gov/articles/PMC6902784/ (Marshall-Goebel 2019, JAMA Netw Open).
- [VERIFICADO] "Risk of Cardiovascular Adaptations" y "Reduced Cardiorespiratory and Musculoskeletal Fitness" figuran en el HRP: https://www.nasa.gov/hrp/risks
- Indicadores: frecuencia cardiaca, HRV, presion arterial, flujo venoso por ultrasonido Doppler, VO2/capacidad aerobica.
- Sensores: ECG/PPG para FC y HRV; ultrasonido (el sistema HRF de ISS es el unico dispositivo de imagen diagnostica) [VERIFICADO] https://ntrs.nasa.gov/api/citations/20110011351/downloads/20110011351.pdf (resultado de busqueda; detalle no leido). Astroskin mide FC, respiracion, SpO2, presion, temperatura, actividad y calcula HRV [VERIFICADO] https://wt-obk.wearable-technologies.com/2018/09/astroskin-smart-shirt-will-monitor-astronauts-vital-signs-in-space/

### 2.3 Ojo/neuro (SANS)
- [VERIFICADO] Edema de disco optico, aplanamiento del globo, pliegues coroideos, cambio hipermetropico. Causa exacta desconocida; desplazamiento cefalico de fluidos entre factores. Fuente: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10907968/
- Indicadores: OCT, agudeza visual, fondo de ojo. Sensores: [SUPOSICION] camara de fondo de ojo/OCT portatil; no es un wearable continuo. [HUECO] monitoreo continuo de presion intracraneal no verificado.

## 3. Sistema inmune
- [VERIFICADO] Disregulacion inmune y reactivacion de herpesvirus latentes durante 6 meses de vuelo; inmunidad innata elevada, adaptativa alterada; hipersensibilidad persistente en algunas tripulaciones. Fuente: https://frontiersin.org/journals/immunology/articles/10.3389/fimmu.2018.01437/full
- [VERIFICADO] Estresores asociados: microgravedad, radiacion, separacion social, privacion de sueno, alteracion circadiana (misma fuente).
- Indicadores: recuento/fenotipo de leucocitos, citoquinas, carga viral (EBV, CMV, VZV en saliva/orina), erupciones cutaneas.
- Sensores: temperatura cutanea/central como proxy de fiebre; [SUPOSICION] cambios de HRV, frecuencia respiratoria y temperatura nocturna como alerta temprana de infeccion (inferencia, no validada en orbita). Biomarcadores requieren analisis de laboratorio/point-of-care. [HUECO] no se encontro validacion de wearables para detectar reactivacion viral.

## 4. Aislamiento, confinamiento y ambiente cerrado
- [VERIFICADO] Mars-500 (520 dias): menor actividad, tiempo de reposo +50 %, sueno +8 %, ciclos sueno-vigilia alterados, grandes diferencias individuales; un tripulante en ciclo de 25 h y desincronizado. Fuentes: https://whyy.org/articles/psychological-hazards-of-exploration-lessons-from-a-mock-mars-mission/ y https://www.sciencenews.org/article/long-space-missions-may-be-hazardous-your-sleep (articulo PNAS original no leido).
- [VERIFICADO] HRP lista "Behavioral Changes and Psychiatric Disorders", "Inadequate Teamwork" e "Inadequate Sleep and Irregular Schedules": https://www.nasa.gov/hrp/risks
- [VERIFICADO] Twins Study reporto cambio en funcion cognitiva: https://news.weill.cornell.edu/news/2019/09/heavenly-bodies-nasa%E2%80%99s-famed-twins-study-has-begun-to-yield-results

| Dominio | Indicador | Sensor/metodo | Estado |
|---|---|---|---|
| Sueno | duracion, fases, regularidad, desfase circadiano | actigrafia, PPG, mascara con EEG (proyecto ASI/IIT) | Actigrafia/mascara: [VERIFICADO] https://magazine.unibo.it/en/articles/how-astronauts-sleep-in-space ; demas [SUPOSICION] |
| Actividad | pasos, minutos de reposo, ejercicio | acelerometro/IMU | [VERIFICADO] Astroskin (cadencia, pasos); Mars-500 uso actividad como indicador |
| Estres/autonomico | HRV, FC en reposo, respiracion | ECG/PPG, textil inteligente | [VERIFICADO] Astroskin calcula HRV |
| Oxigenacion | SpO2 | oximetria | [VERIFICADO] Astroskin mide SpO2 |
| Temperatura | cutanea/central | termometro textil | [VERIFICADO] Astroskin |
| Cognicion/vigilancia | tiempo de reaccion, memoria, atencion | pruebas cognitivas breves en tablet | [SUPOSICION] (no se verifico la bateria concreta de NASA) |
| Voz/habla | prosodia, ritmo, latencia | microfono + analisis acustico | [HUECO] no se busco evidencia; solo hipotesis |
| Social/clima de equipo | interacciones, proximidad | badges/cuestionarios | [HUECO] no verificado |

## 5. Brechas y cautelas para el proyecto
- [HUECO] Umbrales clinicos de alerta para astronautas en orbita no verificados; usar rangos de referencia terrestres solo como placeholder [SUPOSICION].
- [SUPOSICION] Con n pequeno (3-6 tripulantes), los modelos deben ser individualizados (linea base personal): coherente con "grandes diferencias individuales" de Mars-500.
- [HUECO] Cifras de bone loss y dosis necesitan contraste con articulos primarios antes de citarlas en la presentacion final.
