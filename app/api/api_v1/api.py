from app.api.api_v1.endpoints import (users, roles, periods, auth, job_titles, stages, departments, branches, buildings,
                                      rooms, floors, subjects, lessons, cards, days, schedule, asc_version,
                                      telegram_user)
from app.api.api_v1.tags import Tags
from app.core.utils.utils import APIPermissionsRouter
from openapi_formatter.openapi import generate_formatted_openapi
from fastapi.responses import FileResponse

api_router = APIPermissionsRouter()

api_router.include_router(schedule.router, prefix="/schedule", tags=[Tags.schedules])
api_router.include_router(stages.router, prefix="/stages", tags=[Tags.stages])
api_router.include_router(asc_version.router, prefix="/asc", tags=[Tags.asc])
api_router.include_router(auth.router, prefix="/auth", tags=[Tags.auth])
api_router.include_router(periods.router, prefix="/periods", tags=[Tags.periods])
api_router.include_router(job_titles.router, prefix="/job_titles", tags=[Tags.job_titles])
api_router.include_permissions_router(departments.router, prefix="/departments", tags=[Tags.departments])
api_router.include_router(branches.router, prefix="/branches", tags=[Tags.branches])
api_router.include_router(buildings.router, prefix="/buildings", tags=[Tags.buildings])
api_router.include_router(rooms.router, prefix="/rooms", tags=[Tags.rooms])
api_router.include_router(floors.router, prefix="/floors", tags=[Tags.floors])
api_router.include_router(subjects.router, prefix="/subjects", tags=[Tags.subjects])
api_router.include_router(lessons.router, prefix="/lessons", tags=[Tags.lessons])
api_router.include_router(cards.router, prefix="/cards", tags=[Tags.cards])
api_router.include_permissions_router(days.router, prefix="/days", tags=[Tags.days])
api_router.include_router(users.router, prefix="/users", tags=[Tags.users])
api_router.include_permissions_router(roles.router, prefix="/roles", tags=[Tags.roles])
api_router.include_router(telegram_user.router, prefix="/telegram", tags=[Tags.telegram])


@api_router.get("/openapi2.json")
def get_openapi():
    generate_formatted_openapi()
    return FileResponse("openapi_formatter/openapi.json")
