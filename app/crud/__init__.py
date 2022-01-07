from app.models import Branch
from app.schemas import BranchCreate, BranchUpdate
from .base import CRUDBase
from .crud_stage import stage
from .crud_user import user
from .. import schemas, models
from ..models import Role, Period, JobTitle, Department
from ..schemas import RoleCreate, RoleUpdate, PeriodCreate, PeriodUpdate, JobTitleCreate, JobTitleUpdate, \
    DepartmentCreate, DepartmentUpdate

role = CRUDBase[models.Role, RoleCreate, RoleUpdate, schemas.Role](models.Role, schemas.Role)

period = CRUDBase[models.Period, PeriodCreate, PeriodUpdate, schemas.Period](models.Period, schemas.Period)

job_title = CRUDBase[models.JobTitle, JobTitleCreate, JobTitleUpdate, schemas.JobTitle](models.JobTitle,
                                                                                        schemas.JobTitle)

department = CRUDBase[models.Department, DepartmentCreate, DepartmentUpdate, schemas.Department](models.Department,
                                                                                                 schemas.Department)

branch = CRUDBase[models.Branch, BranchCreate, BranchUpdate, schemas.Branch](models.Branch, schemas.Branch)
