from dataclasses import dataclass
from datetime import datetime

@dataclass
class Booking:
    start: datetime
    end: datetime
    title: str | None = None
    ref: str | None = None
    details: str | None = None   # 👈 NOVO

    @staticmethod
    def _parse_dt_iso_local(s: str) -> datetime | None:
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            return None

    @staticmethod
    def _parse_pair(day: str, hour: str) -> datetime | None:
        try:
            return datetime.strptime(f"{day} {hour}", "%Y-%m-%d %H:%M")
        except Exception:
            return None

    @staticmethod
    def from_api(obj: dict) -> "Booking | None":
        s = e = None
        if obj.get("startDateTime") and obj.get("endDateTime"):
            s = Booking._parse_dt_iso_local(obj["startDateTime"])
            e = Booking._parse_dt_iso_local(obj["endDateTime"])
        else:
            dS, hS = obj.get("dayStartOccupancy"), obj.get("hourStartOccupancy")
            dE, hE = obj.get("dayEndOccupancy"), obj.get("hourEndOccupancy")
            if dS and hS and dE and hE:
                s = Booking._parse_pair(dS, hS)
                e = Booking._parse_pair(dE, hE)
        if not (s and e):
            return None

        title = obj.get("titleOccupancy") or obj.get("title")
        ref = obj.get("refSpac") or obj.get("refSpace") or obj.get("spaceId")
        details = (
            obj.get("detailsOccupancy")
            or obj.get("details")
            or title  # fallback: usa o título como detalhes
        )
        return Booking(start=s, end=e, title=title, ref=ref, details=details)

    def is_now(self, now) -> bool:
        return self.start <= now < self.end
