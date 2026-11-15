"""The astronaut app's link to the ground base (A10, G1): HTTP POST of a FHIR Bundle.

Standard library only. The real transport would be DTN (D-008); this is the prototype stand-in
(D-018). The ground base is optional: without it the app keeps working and queues the package.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any, Protocol


class GroundUnreachable(Exception):
    """The ground base did not answer (not running, no network, timeout)."""


class GroundRejected(Exception):
    """The ground base answered and refused the package; ``problems`` says why."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("; ".join(problems))
        self.problems = problems


class GroundLink(Protocol):
    def sync_clock(self, moment: datetime) -> None: ...

    def send(self, bundle: dict[str, Any]) -> datetime:
        """Deliver ``bundle``; returns when the ground will show it (after the delay)."""
        ...


class HttpGroundLink:
    def __init__(self, base_url: str, timeout: float = 2.0) -> None:
        self._base = base_url.rstrip("/")
        self._timeout = timeout

    def _call(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            self._base + path,
            data=json.dumps(payload).encode(),
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                body: dict[str, Any] = json.loads(response.read())
                return body
        except urllib.error.HTTPError as error:
            if error.code == 422:
                detail = json.loads(error.read()).get("detail", {})
                problems = detail.get("problems") if isinstance(detail, dict) else None
                raise GroundRejected(problems or [str(detail)]) from error
            raise GroundUnreachable(f"HTTP {error.code}") from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise GroundUnreachable(str(error)) from error

    def sync_clock(self, moment: datetime) -> None:
        self._call("PUT", "/clock", {"now": moment.isoformat()})

    def send(self, bundle: dict[str, Any]) -> datetime:
        answer = self._call("POST", "/bundles", bundle)
        return datetime.fromisoformat(answer["availableAt"])
