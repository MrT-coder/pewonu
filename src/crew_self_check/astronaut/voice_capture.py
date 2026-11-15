"""Where a voice note comes from: the microphone, or a labelled synthetic sample (T2, D-028).

The audio lives in memory only, from ``start`` to ``stop``: the caller analyses it and throws it
away. The app runs on the crew's own computer (D-017), so the server captures the microphone itself
and the audio never reaches the browser or the network. ``sounddevice`` is imported lazily so the
rest of the app works without it (and without a microphone).
"""

from __future__ import annotations

import array
import math
import os
import random
import threading
from typing import Any, Protocol

VOICE_RATE = 16000
MAX_SECONDS = 300  # a note stops by itself after five minutes

# Open questions only (never yes/no): the point is to let the person talk (D-019).
VOICE_PROMPTS = tuple(f"voice.prompt.{i}" for i in range(1, 9))


class VoiceRecorder(Protocol):
    synthetic: bool  # True when the sound is generated, not captured

    def available(self) -> bool: ...

    def start(self) -> None: ...

    def level(self) -> float:
        """How loud it is right now, from 0 to 1 (for the meter on screen)."""
        ...

    def stop(self) -> tuple[array.array[int], int]:
        """Stop, hand over the samples and the sample rate, and forget them."""
        ...


_NOT_A_MICROPHONE = ("steam", "virtual", "stereo mix", "noise-cancelling")


def _is_physical(name: str) -> bool:
    lowered = name.lower()
    return not any(marker in lowered for marker in _NOT_A_MICROPHONE)


def pick_input_device(devices: list[dict[str, Any]], default_index: int) -> int | None:
    """Choose the recording device by index, or ``None`` to let the library decide.

    The Windows Sound Mapper follows the system default, which on many laptops is a virtual input
    (game streaming, noise filters) that records silence. When the default is one of those, the
    first physical microphone is used instead.
    """
    inputs = [(i, str(d["name"])) for i, d in enumerate(devices) if d["max_input_channels"] > 0]
    default_name = next((name for i, name in inputs if i == default_index), "")
    if _is_physical(default_name):
        for index, name in inputs:
            if name.startswith("Microsoft Sound Mapper"):
                return index  # follows the system's default recording device on Windows
    for index, name in inputs:
        if _is_physical(name) and not name.startswith("Microsoft Sound Mapper"):
            return index
    return None


def _default_input(sd: Any) -> int:
    try:
        return int(sd.default.device[0])
    except Exception:
        return -1


class MicRecorder:
    synthetic = False

    def __init__(self, device: int | str | None = None, rate: int = VOICE_RATE) -> None:
        self._rate = rate
        self._device = device if device is not None else _device_from_env()
        self._chunks: list[bytes] = []
        self._level = 0.0
        self._stream: Any = None
        self._lock = threading.Lock()
        self._size = 0

    def available(self) -> bool:
        try:
            import sounddevice as sd

            sd.check_input_settings(device=self._resolved(sd), channels=1, samplerate=self._rate)
        except Exception:  # no library, no device or no permission: the caller falls back
            return False
        return True

    def _resolved(self, sd: Any) -> int | str | None:
        if self._device is not None:
            return self._device
        return pick_input_device(list(sd.query_devices()), _default_input(sd))

    def start(self) -> None:
        import sounddevice as sd

        self._chunks, self._size, self._level = [], 0, 0.0

        def callback(data: Any, frames: int, time: Any, status: Any) -> None:
            raw = bytes(data)
            samples = array.array("h")
            samples.frombytes(raw)
            peak = max((abs(s) for s in samples), default=0)
            with self._lock:
                self._level = min(1.0, peak / 12000)
                if self._size < MAX_SECONDS * self._rate * 2:
                    self._chunks.append(raw)
                    self._size += len(raw)

        self._stream = sd.RawInputStream(
            samplerate=self._rate,
            channels=1,
            dtype="int16",
            device=self._resolved(sd),
            callback=callback,
        )
        self._stream.start()

    def level(self) -> float:
        with self._lock:
            return self._level

    def stop(self) -> tuple[array.array[int], int]:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        with self._lock:
            raw, self._chunks, self._size, self._level = b"".join(self._chunks), [], 0, 0.0
        samples = array.array("h")
        samples.frombytes(raw)
        return samples, self._rate


def _device_from_env() -> int | str | None:
    wanted = os.environ.get("CREW_SELF_CHECK_MIC", "").strip()
    if not wanted:
        return None
    return int(wanted) if wanted.isdigit() else wanted


class SyntheticVoiceRecorder:
    """A generated, speech-like sample for demos without a microphone. Labelled as synthetic."""

    synthetic = True

    KINDS = ("usual", "slower")

    def __init__(self, seconds: float = 14.0, seed: int = 3, kind: str = "usual") -> None:
        if kind not in self.KINDS:
            raise ValueError(f"kind must be one of {self.KINDS}")
        self._seconds = seconds
        self._seed = seed
        self.kind = kind

    def available(self) -> bool:
        return True

    def start(self) -> None:
        return None

    def level(self) -> float:
        return 0.5

    def stop(self) -> tuple[array.array[int], int]:
        rate = 8000
        rng = random.Random(self._seed)
        # usual: brisk, short pauses, lively pitch; slower: slow, long pauses, flatter, softer
        rhythm, cycle, pause, glide, amplitude = (
            (4.4, 5.0, 0.4, 1.8, 7000) if self.kind == "usual" else (2.4, 3.0, 1.3, 0.4, 4800)
        )
        samples = array.array("h")
        phase = 0.0
        for n in range(int(self._seconds * rate)):
            t = n / rate
            envelope = math.sin(math.pi * rhythm * t) ** 2
            if t % cycle > cycle - pause:  # a pause now and then
                envelope = 0.0
            pitch = 125.0 * 2 ** ((glide * math.sin(2 * math.pi * 0.4 * t)) / 12)
            phase += 2 * math.pi * pitch / rate
            voiced = sum(math.sin(h * phase) / h for h in range(1, 5))
            value = amplitude * envelope * voiced + rng.gauss(0, 25)
            samples.append(int(max(-32768, min(32767, value))))
        return samples, rate


def default_recorder() -> VoiceRecorder | None:
    """The microphone if there is one, else ``None`` (the screen offers the sample).

    ``CREW_SELF_CHECK_VOICE=synthetic`` forces the labelled sample (demos without a mic).
    """
    if os.environ.get("CREW_SELF_CHECK_VOICE", "").lower() == "synthetic":
        return SyntheticVoiceRecorder()
    mic = MicRecorder()
    return mic if mic.available() else None
