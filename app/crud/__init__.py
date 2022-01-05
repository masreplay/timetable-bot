from app.schemas.roleschema import RoleCreate, RoleUpdate, RoleSchema
from .base import CRUDBase
from .crud_user import user
from ..schemas.period import Period, PeriodUpdate, PeriodCreate

role = CRUDBase[RoleSchema, RoleCreate, RoleUpdate](RoleSchema)
period = CRUDBase[Period, PeriodCreate, PeriodUpdate](Period)
classes = CRUDBase[Period, PeriodCreate, PeriodUpdate](Period)
