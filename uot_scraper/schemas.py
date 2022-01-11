from pydantic import Field, BaseModel


class Teacher(BaseModel):
    id: str
    ar_name: str | None
    en_name: str
    image: str
    stages_id: list[str] = Field([])
    email: str | None
    uot_url: str
    role_id: str | None

    @property
    def first_name(self):
        return self.ar_name.split()[0]

    @property
    def second_name(self):
        return self.ar_name.split()[1]


class Role(BaseModel):
    id: str
    en_name: str
    ar_name: str | None = Field(None)
