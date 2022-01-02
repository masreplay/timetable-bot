from .crud_user import user

from app.schemas.role import RoleCreate, RoleUpdate, Role
from .base import CRUDBase
from ..schemas.period import Period, PeriodUpdate, PeriodCreate

role = CRUDBase[Role, RoleCreate, RoleUpdate](Role)
period = CRUDBase[Period, PeriodCreate, PeriodUpdate](Period)
classes = CRUDBase[Period, PeriodCreate, PeriodUpdate](Period)
