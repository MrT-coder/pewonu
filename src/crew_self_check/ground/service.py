"""The ground service: take in valid bundles and show them only after the communication delay.

Rules (D-018): the ground sees only what the astronaut chose to send, and only once the simulated
delay has passed. It never asks the astronaut for anything. The clock is injectable: the demo
drives it with the simulated journey, standalone it follows the wall clock.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any

from crew_self_check.core.inbox import BundleInbox, ReceivedBundle
from crew_self_check.ground.ingest import inspect_bundle

DEFAULT_DELAY_MINUTES = 12  # [SUPOSICION] inside the 3-22 min range of D-018
MAX_DELAY_MINUTES = 60


class GroundService:
    def __init__(self, inbox: BundleInbox, clock: Callable[[], datetime] | None = None) -> None:
        self._inbox = inbox
        self._base_clock = clock or (lambda: datetime.now(UTC))
        self._override: datetime | None = None
        self.delay_minutes = DEFAULT_DELAY_MINUTES

    # --- clock -----------------------------------------------------------------------------

    def now(self) -> datetime:
        return self._override if self._override is not None else self._base_clock()

    def set_clock(self, moment: datetime) -> None:
        if moment.tzinfo is None:
            raise ValueError("the clock needs a time zone")
        self._override = moment

    def clear_clock(self) -> None:
        self._override = None

    @property
    def clock_is_simulated(self) -> bool:
        return self._override is not None

    # --- configuration ---------------------------------------------------------------------

    def set_delay(self, minutes: int) -> None:
        if not 0 <= minutes <= MAX_DELAY_MINUTES:
            raise ValueError(f"the delay must be between 0 and {MAX_DELAY_MINUTES} minutes")
        self.delay_minutes = minutes

    # --- receiving and reading ---------------------------------------------------------------

    def receive(self, bundle: dict[str, Any]) -> ReceivedBundle:
        """Keep a valid bundle (``InvalidBundle`` otherwise). The same bundle twice is kept once."""
        parts = inspect_bundle(bundle)
        existing = self._inbox.get(parts.bundle_id)
        if existing is not None:
            return existing
        received_at = self.now()
        item = ReceivedBundle(
            bundle_id=parts.bundle_id,
            crew_id=parts.crew_id,
            sent_at=parts.sent_at,
            received_at=received_at,
            available_at=received_at + timedelta(minutes=self.delay_minutes),
            bundle=bundle,
            readings=parts.readings,
            states=parts.states,
        )
        self._inbox.add(item)
        return item

    def visible(self, as_of: datetime, crew_id: str | None = None) -> tuple[ReceivedBundle, ...]:
        """What has already arrived at ``as_of``, oldest arrival first."""
        arrived = [
            i
            for i in self._inbox.all()
            if i.available_at <= as_of and (crew_id is None or i.crew_id == crew_id)
        ]
        return tuple(sorted(arrived, key=lambda i: i.available_at))

    def visible_now(self, crew_id: str | None = None) -> tuple[ReceivedBundle, ...]:
        return self.visible(self.now(), crew_id)

    def get_visible(self, bundle_id: str, as_of: datetime) -> ReceivedBundle | None:
        item = self._inbox.get(bundle_id)
        return item if item is not None and item.available_at <= as_of else None
