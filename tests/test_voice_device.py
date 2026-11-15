from typing import Any

from crew_self_check.astronaut.voice_capture import pick_input_device


def _dev(name: str, inputs: int = 1) -> dict[str, Any]:
    return {"name": name, "max_input_channels": inputs}


DEVICES = [
    _dev("Microsoft Sound Mapper - Input"),
    _dev("Microphone (Steam Streaming Microphone)"),
    _dev("AI Noise-cancelling Input (ASUS Utility)"),
    _dev("Microphone Array (Realtek(R) Audio)"),
    _dev("Speakers (Realtek(R) Audio)", inputs=0),
]


def test_sound_mapper_is_used_when_the_default_is_a_real_microphone() -> None:
    assert pick_input_device(DEVICES, default_index=3) == 0


def test_a_virtual_default_device_is_skipped_for_a_physical_microphone() -> None:
    assert pick_input_device(DEVICES, default_index=1) == 3


def test_virtual_and_noise_filter_inputs_are_never_picked() -> None:
    only_virtual = [_dev("Microphone (Steam Streaming Microphone)"), _dev("System Virtual Line")]
    assert pick_input_device(only_virtual, default_index=0) is None


def test_output_only_devices_are_ignored() -> None:
    assert pick_input_device([_dev("Speakers", inputs=0)], default_index=-1) is None
