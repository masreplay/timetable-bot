from .base import CRUDBase
from .crud_asc_version import CRUDAscVersion
from .crud_branch import branch
from .crud_schedule import CRUDSchedule
from .crud_stage import stage
from .crud_subject import CRUDSubject
from .crud_telegram_user import CRUDTelegramUser
from .crud_user import user
from .. import schemas, models
from ..schemas import (RoleCreate, PeriodCreate, JobTitleCreate, DepartmentCreate, BuildingCreate,
                       RoomCreate, RoleUpdate, PeriodUpdate, JobTitleUpdate, DepartmentUpdate, BuildingUpdate,
                       RoomUpdate, FloorCreate, FloorUpdate, CardCreate, CardUpdate, LessonCreate, LessonUpdate,
                       DayCreate, DayUpdate, )

# crud types
RoleCRUD: type = CRUDBase[models.Role, RoleCreate, RoleUpdate, schemas.Role]
PeriodCRUD: type = CRUDBase[models.Period, PeriodCreate, PeriodUpdate, schemas.Period]
JobTitleCRUD: type = CRUDBase[models.JobTitle, JobTitleCreate, JobTitleUpdate, schemas.JobTitle]
DepartmentCRUD: type = CRUDBase[models.Department, DepartmentCreate, DepartmentUpdate, schemas.Department]
BuildingCRUD: type = CRUDBase[models.Building, BuildingCreate, BuildingUpdate, schemas.Building]
RoomCRUD: type = CRUDBase[models.Room, RoomCreate, RoomUpdate, schemas.Room]
FloorCRUD: type = CRUDBase[models.Floor, FloorCreate, FloorUpdate, schemas.Floor]
CardCRUD: type = CRUDBase[models.Card, CardCreate, CardUpdate, schemas.Card]
LessonCRUD: type = CRUDBase[models.Lesson, LessonCreate, LessonUpdate, schemas.Lesson]
DayCRUD: type = CRUDBase[models.Day, DayCreate, DayUpdate, schemas.Day]

role: RoleCRUD = RoleCRUD(models.Role, schemas.Role)
period: PeriodCRUD = PeriodCRUD(models.Period, schemas.Period)
job_title: JobTitleCRUD = JobTitleCRUD(models.JobTitle, schemas.JobTitle)
department: DepartmentCRUD = DepartmentCRUD(models.Department, schemas.Department)
building: BuildingCRUD = BuildingCRUD(models.Building, schemas.Building)
room: RoomCRUD = RoomCRUD(models.Room, schemas.Room)
floor: FloorCRUD = FloorCRUD(models.Floor, schemas.Floor)
card: CardCRUD = CardCRUD(models.Card, schemas.Card)
subject: CRUDSubject = CRUDSubject(models.Subject, schemas.Subject)
lesson: LessonCRUD = LessonCRUD(models.Lesson, schemas.Lesson)
day: DayCRUD = DayCRUD(models.Day, schemas.Day)
schedule: CRUDSchedule = CRUDSchedule()
asc_version: CRUDAscVersion = CRUDAscVersion()
telegram_user: CRUDTelegramUser = CRUDTelegramUser(models.TelegramUser, schemas.TelegramUser)
