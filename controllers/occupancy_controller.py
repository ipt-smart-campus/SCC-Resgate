from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

from services.occupancy_service import list_currently_busy, fetch_spaces
from config import config


# Blueprint de páginas (views)
occupancy_bp = Blueprint("occupancy", __name__)


@occupancy_bp.route("/")
def index():
    building_filter = request.args.get("building")
    now = datetime.now()
    busy = list_currently_busy(building_filter=building_filter, now=now)
    return render_template("occupied.html", items=busy, now=now, building_filter=building_filter)


# Blueprint de API (poderia ser outro módulo/ficheiro)
@occupancy_bp.route("/api/occupied-now")
def api_occupied_now():
    now = datetime.now()
    busy = list_currently_busy(now=now)
    return jsonify(success=True, data=busy, count=len(busy), at=now.isoformat(timespec="seconds"))


@occupancy_bp.route("/api/debug")
def debug_dump():
    now = datetime.now()
    spaces = fetch_spaces()
    return jsonify(
        now=now.isoformat(timespec="seconds"),
        spaces=[{"spaceId": s.query_id, "name": s.name, "building": s.building} for s in spaces],
        api_base=config.API_BASE,
        api_spaces_endpoint=config.API_SPACES_ENDPOINT,
    )
