"""
Serviço de domínio para ocupação de espaços.

Responsável por:
- Obter espaços
- Obter marcações (bookings) por espaço e semana
- Calcular espaços ocupados no momento
"""
from __future__ import annotations
from datetime import datetime
from urllib.parse import quote
from typing import List, Dict, Any

from config import config
from services.curl_client import get_json
from models.room_model import Room
from models.booking_model import Booking
from utils.timeutils import monday_of_week, iso_date


def _title_spaces(slug_like: str) -> str:
    if not slug_like:
        return "—"
    s = slug_like.replace("-", " ")
    return " ".join(w.capitalize() for w in s.split())


def _format_building(current_slug: str) -> str:
    import re
    if not current_slug:
        return "—"
    if current_slug.lower() == "bloco-i":
        return "Bloco-I"
    m = re.fullmatch(r"(bloco)-([a-z])", current_slug.lower())
    if m:
        return f"{m.group(1).capitalize()}-{m.group(2).upper()}"
    return _title_spaces(current_slug)


def _extract_current_level(slug: str, parent_slug: str | None) -> str:
    if not isinstance(slug, str):
        return slug or ""
    if parent_slug and isinstance(parent_slug, str):
        prefix = f"{parent_slug}-"
        if slug.startswith(prefix):
            return slug[len(prefix):]
    return slug


def _format_end_human(dt) -> str:
    # "01h:00min do dia 25-09-2025"
    return dt.strftime("%Hh:%Mmin do dia %d-%m-%Y")


def fetch_spaces() -> list[Room]:
    data = get_json(f"{config.API_BASE}{config.API_SPACES_ENDPOINT}") or {}
    raw = data.get("data") or []
    spaces: List[Room] = []
    for x in raw:
        r = Room.from_api(x)
        r.query_id = r.id  # Space:...
        spaces.append(r)
    return spaces


def fetch_bookings_for_space(space_id: str, week_start_iso: str) -> list[Booking]:
    esc = quote(space_id, safe="")
    url = f"{config.API_BASE}/api/bookings?spaceId={esc}&weekStart={week_start_iso}"
    data = get_json(url) or {}
    arr = data.get("data") or []
    out: list[Booking] = []
    for obj in arr:
        bk = Booking.from_api(obj)
        if not bk:
            continue
        if bk.ref and bk.ref != space_id:
            continue
        out.append(bk)
    return out


def list_currently_busy(building_filter: str | None = None, now: datetime | None = None) -> list[Dict[str, Any]]:
    """Devolve lista de espaços ocupados no momento atual.

    Cada item contém:
    - spaceId, spaceName
    - instPretty, campusPretty, buildingPretty, areaPretty
    - details, endHuman
    """
    now = now or datetime.now()
    week_start = iso_date(monday_of_week(now))

    spaces = fetch_spaces()
    if building_filter:
        spaces = [r for r in spaces if (r.building or "").lower() == building_filter.lower()]

    busy = []
    for s in spaces:
        inst_slug = (s.institution or "")
        campus_slug = _extract_current_level(s.campus or "", inst_slug)
        bld_slug = _extract_current_level(s.building or "", s.campus or "")
        area_slug = _extract_current_level(s.area or "", s.building or "")

        bookings = fetch_bookings_for_space(s.query_id, week_start)
        for bk in bookings:
            if bk.is_now(now):
                busy.append({
                    "spaceId": s.id,
                    "spaceName": s.name,
                    "instPretty": _title_spaces(inst_slug),
                    "campusPretty": _title_spaces(campus_slug),
                    "buildingPretty": _format_building(bld_slug),
                    "areaPretty": _title_spaces(area_slug),
                    "details": bk.details or (bk.title or "-"),
                    "endHuman": _format_end_human(bk.end),
                    "building": s.building or "—",
                    "spaceNameRaw": s.name,
                })

    busy.sort(key=lambda x: ((x.get("buildingPretty") or "—"), (x.get("spaceName") or "")))
    return busy
