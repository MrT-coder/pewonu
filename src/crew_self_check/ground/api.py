"""HTTP face of the ground base: receive bundles (G1), delay (G2) and the view (G3)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import AwareDatetime, BaseModel, Field, StrictInt

from crew_self_check.core.inbox import ReceivedBundle
from crew_self_check.ground import pages
from crew_self_check.ground.i18n import language_from
from crew_self_check.ground.ingest import InvalidBundle
from crew_self_check.ground.service import MAX_DELAY_MINUTES, GroundService
from crew_self_check.ground.view_model import build_crew_view, crew_ids


class DelayBody(BaseModel):
    delayMinutes: StrictInt = Field(ge=0, le=MAX_DELAY_MINUTES)


class ClockBody(BaseModel):
    now: AwareDatetime


def _meta(item: ReceivedBundle) -> dict[str, Any]:
    return {
        "id": item.bundle_id,
        "crewId": item.crew_id,
        "sentAt": item.sent_at.isoformat(),
        "receivedAt": item.received_at.isoformat(),
        "availableAt": item.available_at.isoformat(),
        "readings": item.readings,
        "states": item.states,
    }


def _clock(service: GroundService) -> dict[str, Any]:
    return {"now": service.now().isoformat(), "simulated": service.clock_is_simulated}


def create_app(service: GroundService) -> FastAPI:
    app = FastAPI(title="Crew Self-Check ground base", version="0.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "system": "ground"}

    @app.post("/bundles", status_code=202)
    async def post_bundle(request: Request) -> JSONResponse:
        try:
            body = await request.json()
        except ValueError:
            body = None
        if not isinstance(body, dict):
            raise HTTPException(
                422,
                {"message": "invalid FHIR bundle", "problems": ["body: expected a JSON object"]},
            )
        try:
            item = service.receive(body)
        except InvalidBundle as error:
            raise HTTPException(
                422, {"message": "invalid FHIR bundle", "problems": error.problems}
            ) from error
        return JSONResponse(
            status_code=202,
            content={**_meta(item), "delayMinutes": service.delay_minutes},
        )

    @app.get("/bundles")
    def list_bundles(crew: str | None = None) -> list[dict[str, Any]]:
        return [_meta(i) for i in service.visible_now(crew)]

    @app.get("/bundles/{bundle_id}")
    def get_bundle(bundle_id: str) -> dict[str, Any]:
        item = service.get_visible(bundle_id, service.now())
        if item is None:
            raise HTTPException(404, "no such bundle has arrived")
        return item.bundle

    @app.get("/config")
    def get_config() -> dict[str, int]:
        return {"delayMinutes": service.delay_minutes}

    @app.put("/config")
    def put_config(body: DelayBody) -> dict[str, int]:
        service.set_delay(body.delayMinutes)
        return {"delayMinutes": service.delay_minutes}

    @app.get("/clock")
    def get_clock() -> dict[str, Any]:
        return _clock(service)

    @app.put("/clock")
    def put_clock(body: ClockBody) -> dict[str, Any]:
        moment: datetime = body.now
        service.set_clock(moment)
        return _clock(service)

    @app.delete("/clock")
    def delete_clock() -> dict[str, Any]:
        service.clear_clock()
        return _clock(service)

    @app.get("/", response_class=HTMLResponse)
    def home(lang: str | None = None) -> str:
        language = language_from(lang)
        arrived = service.visible_now()
        crews = []
        for crew_id in crew_ids(arrived):
            view = build_crew_view(crew_id, arrived)
            if view is not None:
                crews.append((crew_id, view.bundles, view.last_arrival))
        return pages.home_page(
            language, tuple(crews), service.delay_minutes, service.now(), service.clock_is_simulated
        )

    @app.get("/crew/{crew_id}", response_class=HTMLResponse)
    def crew(crew_id: str, lang: str | None = None) -> Response:
        view = build_crew_view(crew_id, service.visible_now(crew_id))
        language = language_from(lang)
        if view is None:
            return HTMLResponse(pages.not_found_page(language), status_code=404)
        return HTMLResponse(pages.crew_page(language, view))

    return app
