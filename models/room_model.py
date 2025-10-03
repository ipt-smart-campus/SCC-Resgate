from dataclasses import dataclass

@dataclass
class Room:
    id: str
    name: str
    building: str | None = None
    campus: str | None = None
    area: str | None = None
    institution: str | None = None
    description: str | None = None
    fullPath: str | None = None
    query_id: str | None = None

    @staticmethod
    def from_api(obj: dict) -> "Room":
        return Room(
            id=obj.get("id") or obj.get("entityId") or obj.get("name"),
            name=obj.get("name") or obj.get("displayName") or obj.get("id"),
            building=obj.get("building"),
            campus=obj.get("campus"),
            area=obj.get("area"),
            institution=obj.get("institution"),
            description=obj.get("description"),
            fullPath=obj.get("fullPath"),
        )
