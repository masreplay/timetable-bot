from pydantic import BaseModel


class Location(BaseModel):
    lng: float | None
    lat: float | None
