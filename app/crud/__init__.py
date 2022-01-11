from .base import CRUDBase
from .crud_schedule import CRUDSchedule
from .crud_stage import stage
from .crud_user import user
from .. import schemas, models
from ..schemas import (RoleCreate, PeriodCreate, JobTitleCreate, DepartmentCreate, BranchCreate, BuildingCreate,
                       RoomCreate, RoleUpdate, PeriodUpdate, JobTitleUpdate, DepartmentUpdate, BranchUpdate,
                       BuildingUpdate, RoomUpdate, FloorCreate, FloorUpdate, CardCreate, CardUpdate, SubjectCreate,
                       LessonCreate, LessonUpdate, SubjectUpdate, DayCreate, DayUpdate, )

# crud types
RoleCRUD: type = CRUDBase[models.Role, RoleCreate, RoleUpdate, schemas.Role]
PeriodCRUD: type = CRUDBase[models.Period, PeriodCreate, PeriodUpdate, schemas.Period]
JobTitleCRUD: type = CRUDBase[models.JobTitle, JobTitleCreate, JobTitleUpdate, schemas.JobTitle]
DepartmentCRUD: type = CRUDBase[models.Department, DepartmentCreate, DepartmentUpdate, schemas.Department]
BranchCRUD: type = CRUDBase[models.Branch, BranchCreate, BranchUpdate, schemas.Branch]
BuildingCRUD: type = CRUDBase[models.Building, BuildingCreate, BuildingUpdate, schemas.Building]
RoomCRUD: type = CRUDBase[models.Room, RoomCreate, RoomUpdate, schemas.Room]
FloorCRUD: type = CRUDBase[models.Floor, FloorCreate, FloorUpdate, schemas.Floor]
CardCRUD: type = CRUDBase[models.Card, CardCreate, CardUpdate, schemas.Card]
SubjectCRUD: type = CRUDBase[models.Subject, SubjectCreate, SubjectUpdate, schemas.Subject]
LessonCRUD: type = CRUDBase[models.Lesson, LessonCreate, LessonUpdate, schemas.Lesson]
DayCRUD: type = CRUDBase[models.Day, DayCreate, DayUpdate, schemas.Day]

role: RoleCRUD = RoleCRUD(models.Role, schemas.Role)
period: PeriodCRUD = PeriodCRUD(models.Period, schemas.Period)
job_title: JobTitleCRUD = JobTitleCRUD(models.JobTitle, schemas.JobTitle)
department: DepartmentCRUD = DepartmentCRUD(models.Department, schemas.Department)
branch: BranchCRUD = BranchCRUD(models.Branch, schemas.Branch)
building: BuildingCRUD = BuildingCRUD(models.Building, schemas.Building)
room: RoomCRUD = RoomCRUD(models.Room, schemas.Room)
floor: FloorCRUD = FloorCRUD(models.Floor, schemas.Floor)
card: CardCRUD = CardCRUD(models.Card, schemas.Card)
subject: SubjectCRUD = SubjectCRUD(models.Subject, schemas.Subject)
lesson: LessonCRUD = LessonCRUD(models.Lesson, schemas.Lesson)
day: DayCRUD = DayCRUD(models.Day, schemas.Day)
schedule: CRUDSchedule = CRUDSchedule()
