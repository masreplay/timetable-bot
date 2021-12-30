from .crud_teacher import teacher

from app.schemas.role import RoleCreate, RoleUpdate, Role
from .base import CRUDBase

role = CRUDBase[Role, RoleCreate, RoleUpdate](Role)
