from .crud_teacher import teacher

from .base import CRUDBase
from app.schemas.role import RoleCreate, RoleUpdate, Role

item = CRUDBase[Role, RoleCreate, RoleUpdate](Role)
