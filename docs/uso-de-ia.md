# Registro de uso de IA

**Requisito oficial 2026:** cada envío debe describir cómo se usaron las herramientas de IA (que en 2026 la organización llama "Super Intelligence") durante el desarrollo. Fuente: https://www.spaceappschallenge.org/resources/participant-faqs/ (ver [research/08](../research/08-enunciado-oficial.md)).

Cada persona agrega una fila cuando la IA aporta algo que llega al repositorio o al pitch. Antes del envío, la persona de producto resume esta tabla en inglés para la página del proyecto.

| Fecha | Persona | Herramienta | Para qué | Qué revisó o cambió el humano |
|---|---|---|---|---|
| 2026-10-28 | Josue Morales | Claude Code | Lectura del enunciado oficial, reanálisis de ideas y estructura del repositorio | Pendiente de revisión del equipo |
| 2026-10-28 | Josue Morales | Claude Code (4 subagentes de investigación) | Búsqueda de literatura sobre humanos en el espacio ([research/09](../research/09-humanos-en-el-espacio.md)) | Pendiente: contrastar las fuentes con artículos descargados (NotebookLM) |
| 2026-10-28 | Josue Morales | NotebookLM (Gemini Notebook) | Recopilación de 189 fuentes e informes de Deep Research sobre salud de astronautas | Pendiente: los 8 informes generados se tratan como [SUPOSICION] hasta verificarlos contra papers |
| 2026-10-30 | Josue Morales | Claude Code (Playwright, skill pdf-to-markdown) | Extracción del inventario de fuentes del cuaderno de NotebookLM, descarga de PDF de acceso abierto y conversión a Markdown ([research/fuentes-notebooklm.md](../research/fuentes-notebooklm.md)) | El humano inició sesión en Google manualmente y eligió la estrategia del corpus. Pendiente: revisar el índice; 17 fuentes de NCBI estaban guardadas en NotebookLM como captcha |
| 2026-11-14 | Josue Morales | Claude Code | C1: tipos del contrato 0.3 en `core/contract.py` y sus tests (test primero) | Pendiente: revisar las suposiciones marcadas en el código (`Sex`, `method` opcional, `experimental` siempre verdadero) |
| 2026-11-14 | Josue Morales | Claude Code (validador oficial de HL7) | C8: exportación a FHIR R4 en `core/fhir.py` (test primero): Observation, Bundle, puerta de consentimiento y revisión de la estructura; verificación de LOINC y UCUM de temperatura y saturación contra los perfiles de HL7 | Pendiente: revisar los códigos locales y qué se comparte |
