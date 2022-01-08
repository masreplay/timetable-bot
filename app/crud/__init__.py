from .base import CRUDBase
from .crud_stage import stage
from .crud_user import user
from .. import schemas, models
from ..schemas import (RoleCreate, PeriodCreate, JobTitleCreate, DepartmentCreate, BranchCreate, BuildingCreate,
                       RoomCreate, RoleUpdate, PeriodUpdate, JobTitleUpdate, DepartmentUpdate, BranchUpdate,
                       BuildingUpdate, RoomUpdate, FloorCreate, FloorUpdate, CardCreate, CardUpdate, )

role = CRUDBase[models.Role, RoleCreate, RoleUpdate, schemas.Role](models.Role, schemas.Role)

period = CRUDBase[models.Period, PeriodCreate, PeriodUpdate, schemas.Period](models.Period, schemas.Period)

job_title = CRUDBase[models.JobTitle, JobTitleCreate, JobTitleUpdate, schemas.JobTitle](models.JobTitle,
                                                                                        schemas.JobTitle)

department = CRUDBase[models.Department, DepartmentCreate, DepartmentUpdate, schemas.Department](models.Department,
                                                                                                 schemas.Department)

branch = CRUDBase[models.Branch, BranchCreate, BranchUpdate, schemas.Branch](models.Branch, schemas.Branch)

building = CRUDBase[models.Building, BuildingCreate, BuildingUpdate, schemas.Building](models.Building,
                                                                                       schemas.Building)

room = CRUDBase[models.Room, RoomCreate, RoomUpdate, schemas.Room](models.Room, schemas.Room)

floor = CRUDBase[models.Floor, FloorCreate, FloorUpdate, schemas.Floor](models.Floor, schemas.Floor)

card = CRUDBase[models.Card, CardCreate, CardUpdate, schemas.Card](models.Card, schemas.Card)
