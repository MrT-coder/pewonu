# 10 - Plataforma, modo offline y dispositivos de entrada

Fecha: 2026-11-06. Etiquetas: [VERIFICADO] (con URL) / [SUPOSICION] / [HUECO]. Las fuentes secundarias se indican como tales. Los estándares de datos para almacenar y migrar se añadirán en la sección 7 cuando termine esa investigación.

## 1. Qué computadoras y sistemas operativos usan las naves

- [VERIFICADO, fuentes secundarias] Los portátiles de soporte de la ISS pasaron de Windows (XP, luego 7) a Debian Linux en 2013, por fiabilidad y estabilidad. Hardware citado: ThinkPad y HP ZBook. La versión de Debian varía según la fuente. Fuentes: https://computerweekly.com/blog/Open-Source-Insider/International-Space-Station-adopts-Debian-Linux-drops-Windows-Red-Hat-into-airlock y https://www.techrepublic.com/pictures/photos-from-the-thinkpad-to-the-ipad-the-tech-used-on-the-iss/
- [HUECO] Falta un documento primario de NASA que confirme el parque actual de portátiles y sus versiones.
- [VERIFICADO] Tres iPad se certificaron para la ISS en 2013: https://ntrs.nasa.gov/citations/20130000791
- [VERIFICADO con reservas] Artemis II (abril 2026) llevó tablets Surface Pro con Windows y Outlook: https://www.geekwire.com/2026/ground-control-to-microsoft-artemis-2-astronauts-deal-with-outlook-hiccup-in-deep-space/. Que se eligieran por estar ya certificadas en la ISS viene de una fuente en español sin confirmación en inglés (https://hipertextual.com/ciencia/artemis-ii-ordenadores-surface-pro/).
- [VERIFICADO con reservas] En febrero 2026 NASA permitió smartphones personales en vuelos, para foto y video, no para operaciones: https://macrumors.com/2026/02/06/nasa-allows-iphones-on-space-flights
- [VERIFICADO con reservas] Para iPad, la página de JSC desaconseja apps que impliquen mantenimiento extra y las admite si un experimento las necesita, con cuenta Apple VPP e instalación vía MDM: https://tsc.jsc.nasa.gov/roi-swprocess/ipad_certs.html (solo se leyó el resumen del buscador).
- [HUECO] No hay datos de Gateway ni del plan para Marte sobre computadoras de tripulación. Tampoco sobre navegadores permitidos ni ciberseguridad a bordo.

## 2. Datos, retrasos y transporte

- [VERIFICADO con reservas] Retraso de un sentido a Marte: ~3 min mínimo, ~12,5 de media y ~22 máximo. A la Luna, ~1,3 s. A la ISS por TDRS, ~0,24 s. Fuente: https://ntrs.nasa.gov/api/citations/20160011483/downloads/20160011483.pdf. **Citar "3-22 min"; la cifra "4-24 min" no tiene respaldo.**
- [VERIFICADO con reservas] DTN (Delay/Disruption-Tolerant Networking) usa el Bundle Protocol: cada nodo guarda el paquete y lo reenvía cuando hay enlace (store-and-forward), con custodia opcional. Está estandarizado por IETF y CCSDS y se probó en la ISS desde ~2009. Fuentes: el PDF de NTRS anterior y https://hackaday.com/2026/01/19/tolerating-delay-with-dtn
- [VERIFICADO] Los registros médicos de la ISS se rigen por la Privacy Act de 1974 y las normas de NASA (HIMS). Fuentes: https://pmc.ncbi.nlm.nih.gov/articles/PMC5098747 y https://public-inspection.federalregister.gov/2023-22412.pdf
- [HUECO] Cómo se transmiten los datos médicos desde la nave y su cifrado a bordo.
- **Implicación:** el transporte diferido ya existe en las naves. Nuestra app no lo reconstruye: solo funciona sin red y guarda localmente un paquete listo para enviar.

## 3. Software médico a bordo

- [VERIFICADO] ExMC y EIMO buscan un sistema de apoyo a la decisión clínica (CDSS) para el Crew Medical Officer que funcione con retraso o sin ayuda de Tierra, con arquitectura de datos médicos y requisitos funcionales: https://ntrs.nasa.gov/citations/20220017856, https://ntrs.nasa.gov/citations/20230016189, https://ntrs.nasa.gov/citations/20240011658
- [HUECO] Cuáles de esos sistemas han volado y sus capacidades offline exactas.

## 4. Dispositivos de entrada

| Dispositivo | Qué mide | Interfaz / formato | Evidencia con astronautas |
|---|---|---|---|
| Bio-Monitor / Astroskin (CSA) | ECG/FC, presión, respiración, temp. de piel, SpO2, actividad, sueño | App en tableta; formato [HUECO] | [VERIFICADO] https://www.asc-csa.gc.ca/eng/sciences/astroskin.asp |
| Holter del HRF (ISS) | ECG continuo de 24 a 48 h | Tarjeta de memoria, datos bajados a Tierra | [VERIFICADO, fuente secundaria] https://wikipedia.com/wiki/Holter_(ISS_Facility) |
| Zephyr BioHarness | FC, HRV, ECG, respiración, temp. de piel, postura | [HUECO] ([SUPOSICION] BLE) | [VERIFICADO] vuelo parabólico: https://webarchive.library.unt.edu/web/20130216213034/http://www.nasa.gov/offices/oct/home/tech_life_zephyr.html |
| Anillo Oura | Sueño, "readiness" | Nube del fabricante | [VERIFICADO] demo comercial Ax-4, no NASA: https://issnationallab.org/?p=48894 |
| Double Sensor / Thermo-Mini (DLR/ESA) | Temperatura central | [HUECO] | [VERIFICADO] 11 astronautas: https://sdg.esa.int/index.php/activity/smart-monitoring-human-thermo-regulation-4368 |
| Camiseta BEAT; chaleco ASI | Pulso, presión, respiración en sueño | [HUECO] | [VERIFICADO] https://www.spacedaily.com/reports/Smart_T_shirt_measures_astronauts_vital_signs_999.html, https://www.asi.it/en/?p=16857 |
| Kit médico ISS (manguito, termómetro) | Presión, temperatura | Manual, sin interfaz de datos [SUPOSICION] | [VERIFICADO] https://spaceref.com/?p=128960 |

- [HUECO] No se encontró evidencia de Fitbit, Garmin ni Apple Watch en estudios NASA, ni de un pulsioxímetro independiente en la ISS. EMG, ecografía y OCT no se investigaron.
- [VERIFICADO] BLE Heart Rate Service (GATT) es el estándar abierto para sensores de FC: https://www.bluetooth.com/specifications/specs/heart-rate-service/. Web Bluetooth lo puede leer desde el navegador, pero es un borrador de la comunidad, no un estándar W3C: https://webarchive.library.unt.edu/web/20170119150036mp_/https://webbluetoothcg.github.io/web-bluetooth
- [VERIFICADO] FHIR R4 define un perfil de FC: LOINC 8867-4, categoría vital-signs, unidad /min: https://hl7.org/fhir/R4/heartrate.html
- [SUPOSICION] Adaptador genérico con modelo interno `{tipo, valor, unidad, t, fuente}` y tres entradas: BLE Heart Rate en vivo, importación CSV/JSON y salida opcional a FHIR Observation. Cualquier campo nuevo se acuerda con [contrato-datos.md](../docs/contrato-datos.md).
- [SUPOSICION] Qué cubre un sensor simple: pulso (cardiovascular y autonómico), reloj (actividad y sueño), pulsioxímetro (oxigenación). Una lectura aislada no basta: se compara con la línea base o queda `insufficient_data`.

## 5. Escenario "un astronauta se desmaya"

- [VERIFICADO] Los CMO suelen no ser médicos y usan la ISS Medical Checklist, con secciones de emergencia: https://ntrs.nasa.gov/api/citations/20110010924/downloads/20110010924.pdf. Existe un estudio de factores humanos sobre esa checklist con un "tripulante caído" simulado: https://ntrs.nasa.gov/citations/20110003477
- [HUECO] No se encontró el texto del procedimiento de síncope ni los criterios de escalamiento a Tierra.
- [VERIFICADO] La intolerancia ortostática tras aterrizar es un riesgo documentado: presíncope en ~20 % de vuelos cortos y >60 % de largos en pruebas de pie sin contramedidas: https://ntrs.nasa.gov/api/citations/20150007319/downloads/20150007319.pdf
- [SUPOSICION] Mientras falte el procedimiento oficial, la pantalla solo muestra FC en vivo con tendencia, preguntas de estado (¿respira?, ¿responde?) y un paso fijo de escalar al CMO y a Tierra. Sin pasos clínicos inventados.

## 6. Recomendación de plataforma

- [SUPOSICION, decisión de diseño] **PWA instalable offline** (service worker y almacenamiento local). Corre en Linux, Windows e iPadOS con un navegador moderno, y se certificaría una sola vez como contenedor web.
- Riesgo: [HUECO] que el navegador a bordo soporte service workers y Web Bluetooth. Plan B documentado, sin construir antes del 14 nov: la misma app web dentro de un contenedor (Electron o Tauri).
- Descartado: app nativa por plataforma, por costo para 3 personas y sin evidencia de que sea requisito.

## 7. Estándares de datos y almacenamiento

Fecha: 2026-11-06. Objetivo: saber en qué forma se guardan y reciben los datos de salud para elegir el almacenamiento local y que luego puedan migrarse o compartirse con Tierra.

### 7.1 Qué usa NASA
- [VERIFICADO] LSAH/LSDA no publican un esquema fijo: el solicitante y LSAH "finalizan el conjunto de datos y el formato" en cada solicitud. Fuente: https://ntrs.nasa.gov/api/citations/20170009502/downloads/20170009502.pdf
- [VERIFICADO con reservas] El mismo taller de 2017 describe un EMR a bordo basado en OpenEMR con modificaciones leves, en desarrollo, con integración prevista de biosensores (según el resumen del buscador; no se leyó el PDF completo).
- [VERIFICADO con reservas] Un documento NTRS sobre el Mission Medical Information System (MMIS) dice que sus conectores usarían estándares de TI en salud como HL7. No se confirmó cuál PDF exacto lo dice (candidato: NTRS 20080010663); abrirlo antes de citarlo.
- [VERIFICADO] Los resúmenes de ExMC (https://ntrs.nasa.gov/citations/20230016189 y https://ntrs.nasa.gov/citations/20220017856) **no nombran** FHIR, openEHR, OMOP ni IEEE 11073. Citan NASA-STD-3001 y, el segundo, HRP-48032 "ExMC CDSS Architecture Recommendation". [HUECO] Falta leer los PDF completos.
- [VERIFICADO] ISA-Tab (OSDR) es la serialización tabular del modelo ISA, con validador: https://isa-tools.org/format/specification.html. [SUPOSICION] Sirve para estudios de laboratorio, no para telemetría de salud.
- [HUECO] No hay esquema público del EMR de la ISS ni de los exportes de LSAH. Las listas "Summarized/Detailed Description of Medical Tests" de nlsp.nasa.gov/data-request-guidelines no se han abierto todavía.

### 7.2 Transporte
- [VERIFICADO] En Bundle Protocol v7 (RFC 9171) la carga útil es una unidad de datos de aplicación: https://www.rfc-editor.org/rfc/rfc9171.html. [SUPOSICION] Por eso un registro médico, por ejemplo un FHIR Bundle, viaja como carga opaca sin que el transporte conozca su formato.
- [HUECO] El perfil CCSDS 734.20 devolvió 404; XTCE y SFDU no se investigaron. No hay evidencia de DTN en la ISS en esta búsqueda.

### 7.3 Estándares de salud candidatos
- [VERIFICADO] Perfil Vital Signs de FHIR R4 (https://hl7.org/fhir/R4/observation-vitalsigns.html): FC = LOINC 8867-4, `/min`; SpO2 = LOINC 2708-6, `%`; presión = panel 85354-9 con sistólica 8480-6 y diastólica 8462-4, en `mm[Hg]`.
- [VERIFICADO] FHIR ND-JSON: un recurso por línea, un tipo por archivo, MIME `application/fhir+ndjson`: https://hl7.org/fhir/R4/nd-json.html
- [SUPOSICION] openEHR, OMOP, IEEE 11073, EDF/WFDB, Open mHealth, HealthKit y Health Connect no se verificaron en esta sesión; el esfuerzo de cualquiera de ellos excede las 48 h.
- [SUPOSICION] Estados por sistema, líneas base y escalamientos no tienen perfil FHIR verificado: usar `Observation` con códigos locales o una extensión, documentado como decisión propia.
- [HUECO] No hay evidencia de que NASA use FHIR. En el pitch decir "compatible con FHIR y transportable como carga útil de DTN", nunca "NASA usa FHIR".

### 7.4 Almacenamiento en el navegador
- [VERIFICADO] Cuotas: Chrome hasta el 60 % del disco por origen, Firefox 2 GB por grupo, Safari ~1 GB (medido por el autor). Los datos son "best effort" salvo que se pida almacenamiento persistente; las PWA instaladas están exentas del tope de 7 días de Safari. Fuente: https://web.dev/articles/storage-for-the-web
- [VERIFICADO] Llamar a `navigator.storage.persist()` al guardar datos críticos: https://web.dev/articles/persistent-storage
- [VERIFICADO] SQLite WASM con `opfs-sahpool`: requiere worker, no soporta varias pestañas por defecto, y si falla la inicialización borra su almacenamiento salvo `preserveOnInitFailure`: https://sqlite.org/wasm/doc/trunk/persistence.md
- [SUPOSICION] Los patrones local-first (registro de eventos de solo anexado, ids idempotentes, sincronización por lotes) no se verificaron con fuente.

### 7.5 Recomendación (decisión de diseño, no verificación)
1. **IndexedDB como registro de eventos de solo anexado**; cada evento con UUID generado en el cliente, que sirve de id idempotente para el envío por lotes.
2. **Sin SQLite WASM**: añade una dependencia (AGENTS.md exige decisión registrada) y riesgos operativos verificados, sin ganancia de interoperabilidad, porque ningún estándar de intercambio verificado exige SQL.
3. **Intercambio: FHIR R4 Bundle JSON y NDJSON** generados desde el registro al exportar. El contrato interno puede seguir siendo el nuestro; FHIR es la capa de salida.
4. Llamar a `persist()` en el primer guardado y rotular los datos como simulados o análogos.

## 8. Conexión con dispositivos desde la PWA

Fecha: 2026-11-06. Fuentes principales: MDN, caniuse, Chrome for Developers. No se leyeron las especificaciones W3C/WICG directamente ni hay documentación primaria de Apple sobre Web Bluetooth en iOS.

### 8.1 Contexto seguro
- [VERIFICADO] Son contextos seguros `https://`, `wss:`, `file:`, `localhost`, `127.0.0.0/8` y `::1`. Una IP de LAN por `http://` (192.168.x.x) no lo es. Los service workers solo se registran en contextos seguros: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts
- [VERIFICADO] Web Bluetooth, Web Serial, WebUSB y el File System API (incluye OPFS) exigen contexto seguro: https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API, https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API, https://developer.mozilla.org/en-US/docs/Web/API/WebUSB_API
- [SUPOSICION] WebHID también lo exige (MDN no lo dice en la página consultada).
- [SUPOSICION] En una LAN con `http://192.168.x.x` no se registra el service worker y `navigator.bluetooth` o `navigator.serial` no se exponen.
- Opciones: servir desde `http://localhost` [VERIFICADO], certificado local de una CA propia instalada en cada equipo [SUPOSICION, no se verificó la herramienta] o `file://` [SUPOSICION: no se probó que un service worker se registre desde ahí].

### 8.2 Soporte por plataforma (caniuse)
| API | Chrome / Edge (Win, Linux, macOS) | Firefox | Safari macOS | Safari iOS/iPadOS |
|---|---|---|---|---|
| Web Bluetooth | Chrome 56+, Edge 79+ | No | No | No |
| Web Serial | Chrome/Edge 89+ | Sí desde 151 | No | No |
| WebUSB | Chrome 61+, Edge 79+ | No | No | No |
| WebHID | Chrome/Edge 89+ | No | No | No |

- [VERIFICADO] WebKit tiene posición "oppose" sobre Web Bluetooth, WebHID, Web Serial y WebUSB: https://github.com/WebKit/standards-positions/issues?q=web+bluetooth
- [HUECO] Web Bluetooth en Linux: la página del WebBluetoothCG dice "partially implemented and not supported" y pide una bandera, pero puede estar desactualizada: https://github.com/WebBluetoothCG/web-bluetooth/blob/main/implementation-status.md. **Probar en un Debian real.**
- [VERIFICADO] Bluefy es un navegador de App Store que expone Web Bluetooth en iPhone y iPad: https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055
- [SUPOSICION] Otras vías para iOS: app nativa envoltorio (Capacitor) o puente local. Bluefy puede no estar permitido por el MDM de un equipo certificado.

### 8.3 Web Bluetooth
- [VERIFICADO] `requestDevice()` exige un gesto del usuario. `getDevices()` lista los dispositivos ya autorizados sin diálogo, pero hay que llamar a `gatt.connect()`; MDN lo marca experimental: https://developer.mozilla.org/en-US/docs/Web/API/Bluetooth/getDevices
- [HUECO] No se confirmó si `getDevices()` y `watchAdvertisements()` están activos por defecto en el Chrome actual. Un reporte de 2020 indica que `advertisementreceived` no se dispara en Linux ni macOS.
- [VERIFICADO] La lista de bloqueo GATT no incluye Heart Rate (0x180D), Pulse Oximeter (0x1822), Health Thermometer (0x1809), Blood Pressure (0x1810) ni Battery (0x180F): https://github.com/WebBluetoothCG/registries/blob/master/gatt_blocklist.txt
- La API no está disponible en Web Workers [VERIFICADO].

### 8.4 Wi-Fi y red local
- [VERIFICADO] Chrome añade Local Network Access: un sitio público que consulta una IP privada o `localhost` necesita permiso del usuario (prompt desde Chrome 142). Las peticiones con permiso quedan exentas de contenido mixto si el destino es una IP privada literal, un dominio `.local` o `fetch()` con `targetAddressSpace: "local"`: https://developer.chrome.com/blog/local-network-access
- [VERIFICADO con reservas] WebSocket, WebTransport y WebRTC no estaban cubiertos en la versión inicial.
- [SUPOSICION] Si la PWA se sirve desde el mismo equipo (`http://localhost`) y un puente local expone WebSocket o HTTP, se evita el problema y no depende de internet. El puente también cubre iOS y Firefox.

### 8.5 Cable y archivos
- [VERIFICADO] Web Serial: `requestPort()` exige gesto, `getPorts()` devuelve los puertos ya autorizados sin diálogo: https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API
- [SUPOSICION] `<input type="file">` funciona en todos los navegadores, incluido iOS; `showOpenFilePicker` solo en Chromium. Los pulsioxímetros USB suelen exponerse como puerto serie o HID: revisar el modelo concreto.

### 8.6 Arquitectura propuesta (decisión de diseño, no verificación)
Capa `DeviceSource` con interfaz común (`start()`, `stop()`, flujo de lecturas `{tipo, valor, unidad, t, fuente}` y `capabilities()`) e implementaciones intercambiables, de mayor a menor probabilidad de que la demo funcione sin hardware:

| Fuente | Sin hardware real | Plataformas |
|---|---|---|
| Emulador desde dataset | Sí | Todas |
| Importación de archivo | Sí | Todas |
| WebSocket local (puente) | Sí, con servidor simulado | Todas |
| BLE en vivo | Sí, con un periférico simulado (p. ej. nRF Connect [SUPOSICION]) | Chromium; iOS vía Bluefy |
| Serial en vivo | Sí, con puertos virtuales | Chromium y Firefox 151+ |

- Detectar con `'bluetooth' in navigator` e `isSecureContext` y degradar a la siguiente fuente.
- Rotular como simulados los datos del emulador (AGENTS.md, sección 5). El requisito de hardware real del reto sigue en [HUECO].
