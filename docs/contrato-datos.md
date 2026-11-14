# Contrato de datos (motor ↔ app)

Es la costura entre las áreas de trabajo: el **motor** (`engine/`) produce estos objetos y la **app** (`app/`) solo los consume. Mientras el contrato no cambie, cada persona (y su agente) trabaja en paralelo sin pisarse.
**Cambiar este archivo requiere una entrada en [decisiones.md](decisiones.md) y avisar a las otras dos personas.**
Versión: `0.3` (propuesta, 2026-11-14: espacios `environment`, `method`, referencia del estado, perfil de la tripulación y medidas acústicas; D-013 a D-016). La `0.2` agregó los indicadores ortostáticos y vestibulares (D-006 y D-007). Los nombres de campos y valores van en inglés.

## 1. Measurement (entrada)

```json
{
  "crewId": "crew-01",
  "indicator": "resting_hr",
  "value": 62,
  "unit": "bpm",
  "timestamp": "2026-11-14T07:30:00Z",
  "source": "manual",
  "environment": "earth",
  "method": "palpation"
}
```

- `environment`: `earth`, `spacecraft` o `planet` (D-013). Obligatorio.
- `method`: `palpation` (el astronauta cuenta y la app calcula, D-014), `device` o `survey`. Permite al motor ponderar la incertidumbre: una lectura manual es más ruidosa que una de un sensor.

- `indicator`: uno de `resting_hr`, `systolic_bp`, `diastolic_bp`, `blood_glucose`, `body_temp`, `sleep_hours`, `mood`, `spo2`, `orthostatic_hr_delta` (FC de pie menos FC acostado), `vestibular_symptoms` (escala de síntomas), `tandem_walk_ok` (0/1). Se agregan otros con una decisión registrada. Base de los nuevos indicadores: [research/09](../research/09-humanos-en-el-espacio.md).
- `blood_glucose` es de baja frecuencia: entre análisis, su estado normal es `insufficient_data`.
- `source`: `manual`, `sleep-accel`, `official-2026` (los recursos del 13 nov) o `simulated-scenario` (el viaje simulado de la demo, D-013). Los datos simulados se rotulan siempre como tales.
- `mood`: el dato es el resultado de la encuesta clásica de la burbuja (`method: survey`), nunca una inferencia de la voz (D-015, D-019).

## 2. IndicatorStatus (salida del motor, por persona e indicador)

```json
{
  "crewId": "crew-01",
  "indicator": "resting_hr",
  "status": "watch",
  "baseline": { "center": 60, "low": 55, "high": 66, "nDays": 9 },
  "latest": 71,
  "trend": [{ "timestamp": "2026-11-06T07:30:00Z", "value": 59 }],
  "reason": "3 consecutive readings above personal range",
  "escalation": "crew_cmo",
  "environment": "spacecraft",
  "reference": "personal"
}
```

- `reference`: contra qué se comparó el estado (D-013, D-014). `personal` (línea base de este espacio), `transition` (línea base del espacio anterior, `baselineEnvironment` indica cuál) o `population` (tabla poblacional, solo mientras no haya línea base personal). La app rotula siempre la referencia. Con `population` el estado no puede ser `insufficient_data` por falta de línea base, pero sí si faltan lecturas recientes.

- `status`: `ok` (verde), `watch` (ámbar), `act` (rojo) o `insufficient_data` (gris). `insufficient_data` tiene prioridad sobre cualquier otro estado.
- `escalation`: `self_care`, `crew_cmo` o `ground_surgeon`.
- `reason`: texto corto y determinista (plantilla), nunca generado por un LLM.
- `escalation` es una **sugerencia**: la app no envía nada sin la confirmación del astronauta (D-006).

## 3. SystemStatus (lo que pinta la figura corporal)

```json
{
  "crewId": "crew-01",
  "system": "cardiovascular",
  "status": "watch",
  "indicators": ["resting_hr", "systolic_bp", "diastolic_bp"]
}
```

- `system`: `cardiovascular`, `vestibular` (equilibrio y mareo, para el escenario de llegada a Marte, D-007), `sleep_brain`, `mood`, `bone_muscle` o `immune`.
- El estado del sistema es el peor de sus indicadores, salvo que todos sean `insufficient_data`.

## 4. CrewProfile (perfil de la tripulación ficticia)

```json
{
  "crewId": "crew-01",
  "age": 38,
  "sex": "female",
  "baselineSource": "simulated-clinical-history"
}
```

- Sirve para elegir la fila de la tabla poblacional del pulso (D-014). Son datos ficticios y rotulados como tales; nunca datos personales reales (AGENTS.md, sección 7).

## 5. VoiceFeatures (medidas acústicas, experimentales)

```json
{
  "crewId": "crew-01",
  "timestamp": "2026-11-20T19:10:00Z",
  "environment": "spacecraft",
  "features": { "pitchMeanHz": 182.4, "jitter": 0.012, "shimmer": 0.061, "speechRate": 3.8 },
  "moodSurveyScore": 3,
  "experimental": true
}
```

- Solo números. **Sin etiquetas de emoción** y sin audio ni transcripción: el audio de la bitácora se descarta tras extraer las medidas (D-015, D-019).
- No mueve ningún `status`. Se exporta por FHIR (códigos locales) solo si el astronauta decide enviarlo (D-006).
- [HUECO] El conjunto exacto de medidas y su unidad se definen al implementar; este ejemplo es ilustrativo.

## 6. SpacecraftProfile (configuración de la nave)

```json
{
  "id": "iss-analog",
  "label": "ISS (analog)",
  "equipment": [
    { "id": "bp-cuff", "measures": ["systolic_bp", "diastolic_bp"], "mode": "manual" }
  ]
}
```

- Lista qué equipos hay a bordo y qué indicadores habilitan (D-016). El perfil `iss-analog` está rotulado como análogo. [HUECO] La lista real de equipos se verifica con fuente antes de completarla.
