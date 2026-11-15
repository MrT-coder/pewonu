"""T2: the numbers of a voice note travel to the ground as FHIR, never audio or words (D-028)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.ground_client import GroundUnreachable
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.voice_capture import SyntheticVoiceRecorder
from crew_self_check.core.contract import CrewProfile, Environment, Sex, VoiceFeatures
from crew_self_check.core.fhir import ConsentRequired, ShareSelection, build_bundle, check_bundle
from crew_self_check.core.voice_baseline import VoiceComparison, VoiceLevel, compare
from crew_self_check.ground.ingest import inspect_bundle

PROFILE = CrewProfile("crew-03", 33, Sex.MALE, "simulated-clinical-history")
WHEN = datetime(2026, 11, 22, 12, 0, tzinfo=UTC)
FEATURES = {
    "durationSeconds": 41.0,
    "pitchMeanHz": 117.0,
    "pitchVariation": 1.4,
    "speechRate": 3.0,
    "pauseRatio": 0.4,
    "loudnessDb": -28.0,
}


def _note(crew: str = "crew-03") -> VoiceFeatures:
    return VoiceFeatures(crew, WHEN, Environment.SPACECRAFT, FEATURES, 2)


def _comparison() -> VoiceComparison:
    usual = {
        "durationSeconds": 45.0,
        "pitchMeanHz": 118.0,
        "pitchVariation": 2.4,
        "speechRate": 4.5,
        "pauseRatio": 0.22,
        "loudnessDb": -23.0,
    }
    earlier = [
        VoiceFeatures(
            "crew-03", datetime(2026, 11, 10 + i, 12, tzinfo=UTC), Environment.EARTH, usual, 4
        )
        for i in range(6)
    ]
    return compare(earlier, _note())


def _selection(note: VoiceFeatures | None = None, confirmed: bool = True) -> ShareSelection:
    return ShareSelection(
        profile=PROFILE,
        confirmed=confirmed,
        confirmed_at=WHEN,
        measurements=(),
        statuses=(),
        voice=((note or _note(), _comparison()),),
    )


def _voice_observation(bundle: dict[str, Any]) -> dict[str, Any]:
    return next(
        e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation"
    )


def test_a_voice_only_bundle_is_valid_and_has_the_patient_and_one_observation() -> None:
    bundle = build_bundle(_selection())
    assert check_bundle(bundle) == []
    assert [e["resource"]["resourceType"] for e in bundle["entry"]] == ["Patient", "Observation"]


def test_it_carries_the_numbers_the_comparison_and_the_experimental_flag() -> None:
    observation = _voice_observation(build_bundle(_selection()))
    assert observation["valueCodeableConcept"]["coding"][0]["code"] == VoiceLevel.DIFFERENT.value
    codes = {c["code"]["coding"][0]["code"]: c for c in observation["component"] if "code" in c}
    assert codes["speechRate"]["valueQuantity"]["value"] == 3.0
    assert codes["speechRate-direction"]["valueCodeableConcept"]["coding"][0]["code"] == "down"
    assert codes["pauseRatio-direction"]["valueCodeableConcept"]["coding"][0]["code"] == "up"
    tags = [t["code"] for t in observation["meta"]["tag"]]
    assert "experimental-voice" in tags


def test_there_is_no_audio_no_text_and_no_emotion_label_in_the_bundle() -> None:
    text = str(build_bundle(_selection())).lower()
    for forbidden in (
        "valuestring",
        "valueattachment",
        "transcript",
        "audio",
        "emotion",
        "sad",
        "anx",
    ):
        assert forbidden not in text, forbidden


def test_it_cannot_leave_without_consent_and_cannot_be_someone_elses() -> None:
    with pytest.raises(ConsentRequired):
        _selection(confirmed=False)
    with pytest.raises(ValueError, match="only the data of the person"):
        _selection(note=_note("crew-01"))
    with pytest.raises(ValueError, match="nothing to share"):
        ShareSelection(PROFILE, True, WHEN, (), (), ())


def test_the_ground_accepts_it_and_does_not_count_it_as_a_reading_or_a_state() -> None:
    parts = inspect_bundle(build_bundle(_selection()))
    assert parts.crew_id == "crew-03"
    assert parts.readings == 0
    assert parts.states == 0


# --- the app state shares it ------------------------------------------------------------------


class FakeLink:
    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []
        self.down = False

    def sync_clock(self, moment: datetime) -> None:
        if self.down:
            raise GroundUnreachable("down")

    def send(self, bundle: dict[str, Any]) -> datetime:
        if self.down:
            raise GroundUnreachable("down")
        self.sent.append(bundle)
        return datetime(2030, 1, 1, tzinfo=UTC)


def _state(link: FakeLink | None) -> AppState:
    state = AppState(
        simulated_directory(), ground_link=link, voice_recorder=SyntheticVoiceRecorder()
    )
    state.login("AST-0003")
    state.set_day(next(d.index for d in state.scenario.days if d.label == "T+8"))
    state.open_voice()
    state.start_voice()
    return state


def test_a_saved_note_goes_to_the_ground_by_itself_and_says_so() -> None:
    link = FakeLink()
    state = _state(link)
    result = state.stop_voice()
    assert result.saved and result.shared
    assert len(link.sent) == 1
    assert [e["resource"]["resourceType"] for e in link.sent[0]["entry"]] == [
        "Patient",
        "Observation",
    ]
    (item,) = state.outbox
    assert item.voices == 1
    assert item.readings == 0


def test_without_a_ground_link_nothing_is_sent_and_it_says_so() -> None:
    state = _state(None)
    result = state.stop_voice()
    assert result.saved
    assert not result.shared
    assert state.outbox == []


def test_if_the_ground_is_down_the_note_is_kept_and_sent_later() -> None:
    link = FakeLink()
    link.down = True
    state = _state(link)
    result = state.stop_voice()
    assert result.saved and not result.shared
    assert len(state.unsent_to_ground()) == 1
    link.down = False
    state.advance()
    assert len(link.sent) == 1


def test_a_note_with_poor_quality_is_never_sent() -> None:
    link = FakeLink()
    state = AppState(
        simulated_directory(),
        ground_link=link,
        voice_recorder=SyntheticVoiceRecorder(seconds=2.0),
    )
    state.login("AST-0003")
    state.open_voice()
    state.start_voice()
    result = state.stop_voice()
    assert not result.saved and not result.shared
    assert link.sent == []
