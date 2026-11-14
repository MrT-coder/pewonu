"""C8: FHIR R4 export. Only what the astronaut confirms is exported (D-006, D-010, D-018, D-021)."""

import copy
import json
import os
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from crew_self_check.core.contract import (
    CrewProfile,
    Environment,
    Escalation,
    Indicator,
    IndicatorStatus,
    Measurement,
    Method,
    Reference,
    Sex,
    Source,
    Status,
)
from crew_self_check.core.fhir import (
    CATEGORY_SYSTEM,
    LOCAL_CATEGORY,
    LOCAL_ORIGIN,
    LOINC,
    UCUM,
    ConsentRequired,
    ShareSelection,
    build_bundle,
    bundle_json,
    check_bundle,
    observation_resource,
    patient_resource,
    status_resource,
)

NOW = datetime(2026, 11, 14, 21, 40, tzinfo=UTC)
CONFIRMED = datetime(2026, 11, 14, 21, 45, tzinfo=UTC)
PROFILE = CrewProfile("crew-01", 38, Sex.FEMALE, "simulated-clinical-history")
PATIENT = "urn:uuid:00000000-0000-0000-0000-000000000001"


def reading(
    indicator: Indicator = Indicator.RESTING_HR,
    value: float = 68,
    *,
    unit: str = "bpm",
    method: Method | None = Method.PALPATION,
    source: Source = Source.MANUAL,
    environment: Environment = Environment.SPACECRAFT,
    crew_id: str = "crew-01",
) -> Measurement:
    return Measurement(crew_id, indicator, value, unit, NOW, source, environment, method)


def status(
    indicator: Indicator = Indicator.RESTING_HR,
    state: Status = Status.WATCH,
    *,
    reference: Reference = Reference.PERSONAL,
    baseline_environment: Environment | None = None,
    crew_id: str = "crew-01",
) -> IndicatorStatus:
    return IndicatorStatus(
        crew_id=crew_id,
        indicator=indicator,
        status=state,
        reason="3 consecutive readings above personal range",
        escalation=Escalation.CREW_CMO,
        environment=Environment.PLANET,
        reference=reference,
        baseline_environment=baseline_environment,
    )


def selection(
    measurements: tuple[Measurement, ...] = (),
    statuses: tuple[IndicatorStatus, ...] = (),
    *,
    confirmed: bool = True,
) -> ShareSelection:
    return ShareSelection(
        profile=PROFILE,
        confirmed=confirmed,
        confirmed_at=CONFIRMED,
        measurements=measurements,
        statuses=statuses,
    )


def tags(resource: dict[str, Any]) -> dict[str, str]:
    return {t["system"]: t["code"] for t in resource["meta"]["tag"]}


# --- the pulse follows the HL7 Heart Rate profile ---------------------------------------------


def test_the_pulse_is_a_heart_rate_observation() -> None:
    obs = observation_resource(reading(), PATIENT)
    assert obs["resourceType"] == "Observation"
    assert obs["status"] == "final"
    assert obs["meta"]["profile"] == ["http://hl7.org/fhir/StructureDefinition/heartrate"]
    assert obs["category"] == [
        {"coding": [{"system": CATEGORY_SYSTEM, "code": "vital-signs", "display": "Vital Signs"}]}
    ]
    assert obs["code"]["coding"] == [{"system": LOINC, "code": "8867-4", "display": "Heart rate"}]
    assert obs["valueQuantity"] == {
        "value": 68,
        "unit": "beats/minute",
        "system": UCUM,
        "code": "/min",
    }
    assert obs["effectiveDateTime"] == "2026-11-14T21:40:00Z"
    assert obs["subject"] == {"reference": PATIENT}
    assert obs["method"]["coding"][0] == {
        "system": "urn:crew-self-check:observation-method",
        "code": "palpation",
        "display": "Palpation (counted by hand)",
    }


def test_body_temperature_and_oxygen_saturation_follow_their_hl7_profiles() -> None:
    temp = observation_resource(
        reading(Indicator.BODY_TEMP, 36.6, unit="degC", method=Method.DEVICE), PATIENT
    )
    assert temp["meta"]["profile"] == ["http://hl7.org/fhir/StructureDefinition/bodytemp"]
    assert temp["code"]["coding"][0]["code"] == "8310-5"
    assert temp["valueQuantity"]["code"] == "Cel"
    assert temp["valueQuantity"]["system"] == UCUM
    spo2 = observation_resource(
        reading(Indicator.SPO2, 97, unit="%", method=Method.DEVICE), PATIENT
    )
    assert spo2["meta"]["profile"] == ["http://hl7.org/fhir/StructureDefinition/oxygensat"]
    assert spo2["code"]["coding"][0]["code"] == "2708-6"
    assert spo2["valueQuantity"]["code"] == "%"
    for obs in (temp, spo2):
        assert obs["category"][0]["coding"][0]["code"] == "vital-signs"


# --- everything else uses documented local codes (D-010) --------------------------------------


@pytest.mark.parametrize(
    ("indicator", "category", "ucum"),
    [
        (Indicator.SYSTOLIC_BP, "exam", "mm[Hg]"),
        (Indicator.DIASTOLIC_BP, "exam", "mm[Hg]"),
        (Indicator.BLOOD_GLUCOSE, "laboratory", "mg/dL"),
        (Indicator.SLEEP_HOURS, "activity", "h"),
        (Indicator.ORTHOSTATIC_HR_DELTA, "exam", "/min"),
    ],
)
def test_the_other_indicators_use_a_local_code_and_no_profile(
    indicator: Indicator, category: str, ucum: str
) -> None:
    obs = observation_resource(reading(indicator, 4, unit="u", method=Method.SURVEY), PATIENT)
    assert "profile" not in obs["meta"]
    assert obs["code"]["coding"] == [
        {
            "system": "urn:crew-self-check:indicator",
            "code": indicator.value,
            "display": obs["code"]["coding"][0]["display"],
        }
    ]
    assert obs["code"]["coding"][0]["display"]
    assert obs["category"][0]["coding"][0]["code"] == category
    assert obs["category"][0]["coding"][0]["system"] == CATEGORY_SYSTEM
    assert obs["valueQuantity"]["code"] == ucum
    assert obs["valueQuantity"]["system"] == UCUM
    assert obs["valueQuantity"]["value"] == 4


@pytest.mark.parametrize("indicator", [Indicator.MOOD, Indicator.VESTIBULAR_SYMPTOMS])
def test_a_score_is_a_whole_number_not_a_quantity_with_an_invented_unit(
    indicator: Indicator,
) -> None:
    obs = observation_resource(reading(indicator, 4, unit="score", method=Method.SURVEY), PATIENT)
    assert obs["valueInteger"] == 4
    assert "valueQuantity" not in obs
    assert obs["category"][0]["coding"][0]["code"] == "survey"
    assert obs["code"]["coding"][0]["system"] == "urn:crew-self-check:indicator"
    with pytest.raises(ValueError, match="whole"):
        observation_resource(reading(indicator, 3.5, method=Method.SURVEY), PATIENT)


def test_the_tandem_walk_is_a_yes_or_no() -> None:
    ok = observation_resource(reading(Indicator.TANDEM_WALK_OK, 1, method=Method.SURVEY), PATIENT)
    failed = observation_resource(
        reading(Indicator.TANDEM_WALK_OK, 0, method=Method.SURVEY), PATIENT
    )
    assert ok["valueBoolean"] is True
    assert failed["valueBoolean"] is False
    assert "valueQuantity" not in ok


def test_a_reading_without_a_method_has_no_method() -> None:
    assert "method" not in observation_resource(reading(method=None), PATIENT)


def test_a_fractional_value_stays_fractional() -> None:
    obs = observation_resource(reading(Indicator.SLEEP_HOURS, 6.5, unit="h", method=None), PATIENT)
    assert obs["valueQuantity"]["value"] == 6.5


def test_every_indicator_can_be_exported() -> None:
    for indicator in Indicator:
        obs = observation_resource(reading(indicator, 1, method=None), PATIENT)
        assert obs["code"]["coding"], indicator


# --- nothing real, and everything labelled ----------------------------------------------------


def test_every_resource_says_where_the_data_comes_from_and_where_it_was_taken() -> None:
    simulated = observation_resource(reading(source=Source.SIMULATED_SCENARIO), PATIENT)
    manual = observation_resource(reading(source=Source.MANUAL), PATIENT)
    assert tags(simulated)[LOCAL_ORIGIN] == "simulated-scenario"
    assert tags(manual)[LOCAL_ORIGIN] == "manual"
    assert tags(manual)["urn:crew-self-check:environment"] == "spacecraft"
    assert tags(patient_resource(PROFILE))[LOCAL_ORIGIN] == "fictitious-crew"


def test_the_patient_is_a_fictitious_crew_member_with_no_real_identity() -> None:
    patient = patient_resource(PROFILE)
    assert patient["resourceType"] == "Patient"
    assert patient["gender"] == "female"
    assert patient["identifier"] == [{"system": "urn:crew-self-check:crew-id", "value": "crew-01"}]
    assert "name" not in patient
    assert "birthDate" not in patient


# --- the state is exported with a local code, a reason and the reference ----------------------


def test_a_status_is_an_observation_with_its_reason_and_reference() -> None:
    obs = status_resource(status(), PATIENT, CONFIRMED)
    assert obs["resourceType"] == "Observation"
    assert obs["status"] == "final"
    assert obs["category"][0]["coding"][0] == {
        "system": LOCAL_CATEGORY,
        "code": "derived-status",
        "display": "Status derived by the app",
    }
    assert obs["code"]["coding"][0]["code"] == "indicator-status"
    assert obs["valueCodeableConcept"]["coding"][0] == {
        "system": "urn:crew-self-check:indicator-status",
        "code": "watch",
        "display": "Amber: outside the range it was compared with",
    }
    assert obs["note"] == [{"text": "3 consecutive readings above personal range"}]
    assert obs["effectiveDateTime"] == "2026-11-14T21:45:00Z"
    parts = {c["code"]["coding"][0]["code"]: c["valueCodeableConcept"]["coding"][0]["code"]
             for c in obs["component"]}  # fmt: skip
    assert parts == {
        "indicator": "resting_hr",
        "reference": "personal",
        "escalation-suggestion": "crew_cmo",
    }
    assert tags(obs)["urn:crew-self-check:environment"] == "planet"


@pytest.mark.parametrize(
    ("state", "code"),
    [(Status.OK, "ok"), (Status.WATCH, "watch"), (Status.ACT, "act"),
     (Status.INSUFFICIENT_DATA, "insufficient_data")],
)  # fmt: skip
def test_the_four_states_have_a_code_and_a_meaning(state: Status, code: str) -> None:
    coding = status_resource(status(state=state), PATIENT, CONFIRMED)["valueCodeableConcept"][
        "coding"
    ][0]
    assert coding["code"] == code
    assert coding["display"]


def test_a_transition_status_says_which_baseline_it_used() -> None:
    obs = status_resource(
        status(reference=Reference.TRANSITION, baseline_environment=Environment.EARTH),
        PATIENT,
        CONFIRMED,
    )
    parts = {c["code"]["coding"][0]["code"]: c["valueCodeableConcept"]["coding"][0]["code"]
             for c in obs["component"]}  # fmt: skip
    assert parts["reference"] == "transition"
    assert parts["baseline-environment"] == "earth"


# --- nothing leaves without the astronaut's confirmation (D-006) ------------------------------


def test_without_a_confirmation_a_selection_cannot_exist() -> None:
    with pytest.raises(ConsentRequired):
        selection((reading(),), confirmed=False)


@pytest.mark.parametrize("not_confirmed", [None, 0, "yes", 1])
def test_only_an_explicit_true_counts_as_a_confirmation(not_confirmed: object) -> None:
    with pytest.raises(ConsentRequired):
        ShareSelection(
            profile=PROFILE,
            confirmed=not_confirmed,  # type: ignore[arg-type]
            confirmed_at=CONFIRMED,
            measurements=(reading(),),
            statuses=(),
        )


def test_an_empty_selection_is_refused() -> None:
    with pytest.raises(ValueError, match="nothing"):
        selection()


def test_data_of_another_person_cannot_be_smuggled_in() -> None:
    with pytest.raises(ValueError, match="crew-02"):
        selection((reading(crew_id="crew-02"),))
    with pytest.raises(ValueError, match="crew-02"):
        selection(statuses=(status(crew_id="crew-02"),))


def test_the_confirmation_needs_a_timezone() -> None:
    with pytest.raises(ValueError, match="timezone"):
        ShareSelection(
            profile=PROFILE,
            confirmed=True,
            confirmed_at=datetime(2026, 11, 14, 21, 45),
            measurements=(reading(),),
            statuses=(),
        )


# --- the bundle -------------------------------------------------------------------------------


def sample_bundle() -> dict[str, Any]:
    return build_bundle(
        selection(
            (
                reading(),
                reading(Indicator.MOOD, 4, unit="score", method=Method.SURVEY),
                reading(Indicator.BODY_TEMP, 36.6, unit="degC", method=Method.DEVICE),
            ),
            (status(), status(Indicator.MOOD, Status.OK)),
        )
    )


def test_the_bundle_holds_the_patient_and_only_what_was_selected() -> None:
    bundle = sample_bundle()
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert bundle["timestamp"] == "2026-11-14T21:45:00Z"
    kinds = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert kinds == ["Patient"] + ["Observation"] * 5
    assert all(e["fullUrl"].startswith("urn:uuid:") for e in bundle["entry"])


def test_every_reference_points_to_the_patient_in_the_same_bundle() -> None:
    bundle = sample_bundle()
    patient_url = bundle["entry"][0]["fullUrl"]
    for entry in bundle["entry"][1:]:
        assert entry["resource"]["subject"]["reference"] == patient_url


def test_the_same_selection_gives_the_same_bundle_so_a_resend_is_idempotent() -> None:
    assert sample_bundle() == sample_bundle()
    first = {e["fullUrl"] for e in sample_bundle()["entry"]}
    changed = build_bundle(selection((reading(value=69),)))
    assert first.isdisjoint({changed["entry"][1]["fullUrl"]})


def test_the_ids_are_unique() -> None:
    urls = [e["fullUrl"] for e in sample_bundle()["entry"]]
    assert len(urls) == len(set(urls))
    ids = [e["resource"]["id"] for e in sample_bundle()["entry"]]
    assert len(ids) == len(set(ids))
    assert all(url == f"urn:uuid:{rid}" for url, rid in zip(urls, ids, strict=True))


def test_the_bundle_is_plain_json_and_survives_a_round_trip() -> None:
    bundle = sample_bundle()
    text = bundle_json(bundle)
    assert json.loads(text) == bundle
    assert "\r" not in text


def test_a_bundle_never_contains_a_voice_recording_or_a_name() -> None:
    text = bundle_json(sample_bundle()).lower()
    for forbidden in ("audio", "transcript", "emotion", '"name"', "birthdate"):
        assert forbidden not in text


# --- our own structure check (the official validator is the second opinion) --------------------


def test_a_good_bundle_has_no_structure_problems() -> None:
    assert check_bundle(sample_bundle()) == []


def test_the_check_finds_a_reference_that_does_not_resolve() -> None:
    bundle = sample_bundle()
    bundle["entry"][1]["resource"]["subject"]["reference"] = "urn:uuid:nobody"
    assert any("reference" in problem for problem in check_bundle(bundle))


def test_the_check_finds_a_profile_value_that_was_changed() -> None:
    bundle = sample_bundle()
    pulse = bundle["entry"][1]["resource"]
    pulse["valueQuantity"]["code"] = "bpm"
    assert any("/min" in problem for problem in check_bundle(bundle))
    bundle = sample_bundle()
    bundle["entry"][1]["resource"]["code"]["coding"][0]["code"] = "0000-0"
    assert any("8867-4" in problem for problem in check_bundle(bundle))


def test_the_check_finds_missing_required_parts() -> None:
    for missing in ("status", "code", "subject", "effectiveDateTime"):
        bundle = sample_bundle()
        del bundle["entry"][1]["resource"][missing]
        assert any(missing in problem for problem in check_bundle(bundle)), missing
    bundle = sample_bundle()
    bundle["entry"][1]["resource"]["valueQuantity"] = None
    del bundle["entry"][1]["resource"]["valueQuantity"]
    assert any("value" in problem for problem in check_bundle(bundle))


def test_the_check_finds_duplicate_urls_and_a_wrong_bundle_type() -> None:
    bundle = sample_bundle()
    bundle["entry"][2]["fullUrl"] = bundle["entry"][1]["fullUrl"]
    assert any("duplicate" in problem for problem in check_bundle(bundle))
    other = copy.deepcopy(sample_bundle())
    other["type"] = "searchset"
    assert any("type" in problem for problem in check_bundle(other))


# --- the official HL7 validator, when it is available (D-022) ---------------------------------


@pytest.mark.skipif(
    not os.environ.get("HL7_VALIDATOR_JAR") or shutil.which("java") is None,
    reason="set HL7_VALIDATOR_JAR to the path of validator_cli.jar (and have Java) to run it",
)
def test_the_official_hl7_validator_finds_no_errors() -> None:
    jar = Path(os.environ["HL7_VALIDATOR_JAR"])
    assert jar.is_file()
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "bundle.json"
        path.write_text(bundle_json(sample_bundle()), encoding="utf-8")
        run = subprocess.run(
            ["java", "-jar", str(jar), str(path), "-version", "4.0.1", "-tx", "n/a"],
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    output = run.stdout + run.stderr
    assert "0 errors" in output, output[-3000:]
