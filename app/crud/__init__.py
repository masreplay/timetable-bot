from app.models import Branch
from app.models import Department
from app.models import JobTitle, Period, Role
from app.models import Stage
from app.schemas import (BranchCreate, BranchUpdate, DepartmentCreate, DepartmentUpdate, JobTitleCreate, JobTitleUpdate,
                         PeriodUpdate, PeriodCreate, StageCreate, StageUpdate)
from app.schemas.role import RoleCreate, RoleUpdate
from .base import CRUDBase
from .crud_user import user

role = CRUDBase[Role, RoleCreate, RoleUpdate](Role)

period = CRUDBase[Period, PeriodCreate, PeriodUpdate](Period)

job_title = CRUDBase[JobTitle, JobTitleCreate, JobTitleUpdate](JobTitle)

department = CRUDBase[Department, DepartmentCreate, DepartmentUpdate](Department)

branch = CRUDBase[Branch, BranchCreate, BranchUpdate](Branch)

stage = CRUDBase[Stage, StageCreate, StageUpdate](Stage)
