from app.schemas.role import RoleCreate, RoleUpdate
from .base import CRUDBase
from .crud_user import user
from ..models import JobTitle, Period, Role
from ..schemas import JobTitleCreate, JobTitleUpdate
from ..schemas import PeriodUpdate, PeriodCreate

role = CRUDBase[Role, RoleCreate, RoleUpdate](Role)
period = CRUDBase[Period, PeriodCreate, PeriodUpdate](Period)

job_title = CRUDBase[JobTitle, JobTitleCreate, JobTitleUpdate](JobTitle)
