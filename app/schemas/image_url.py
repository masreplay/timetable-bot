from pydantic import BaseModel


class ImageUrl(BaseModel):
    name: str | None = None
    url: str
