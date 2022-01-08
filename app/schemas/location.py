from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    lng: Optional[float]
    lat: Optional[float]
