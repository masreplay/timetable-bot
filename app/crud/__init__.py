from app.models import Branch
from app.models import Department
from app.models import JobTitle, Period, Role
from app.schemas import (BranchCreate, BranchUpdate, DepartmentCreate, DepartmentUpdate, JobTitleCreate, JobTitleUpdate,
                         PeriodUpdate, PeriodCreate, )
from app.schemas.role import RoleCreate, RoleUpdate
from .base import CRUDBase
from .crud_stage import stage
from .crud_user import user
from .. import schemas

role = CRUDBase[Role, RoleCreate, RoleUpdate, schemas.Role](Role, schemas.Role)

period = CRUDBase[Period, PeriodCreate, PeriodUpdate, schemas.Period](Period, schemas.Period)

job_title = CRUDBase[JobTitle, JobTitleCreate, JobTitleUpdate, schemas.Period](Period, schemas.Period)

department = CRUDBase[Department, DepartmentCreate, DepartmentUpdate, schemas.Department](Department,
                                                                                          schemas.Department)

branch = CRUDBase[Branch, BranchCreate, BranchUpdate, schemas.Branch](Branch, schemas.Branch)
