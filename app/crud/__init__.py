from .crud_user import user

from app.schemas.role import RoleCreate, RoleUpdate, Role
from .base import CRUDBase

role = CRUDBase[Role, RoleCreate, RoleUpdate](Role)
