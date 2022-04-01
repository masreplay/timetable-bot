from pydantic import BaseModel

from app.schemas import User, Role


class UserRole(BaseModel):
    user: User
    role: Role
