from app.api.api_v1.endpoints import (users, roles, periods, auth, job_titles, stages, departments, branches, buildings,
                                      rooms, floors, subjects, lessons, cards)
from app.core.utils.utils import APIPermissionsRouter

api_router = APIPermissionsRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
api_router.include_router(job_titles.router, prefix="/job_titles", tags=["job titles"])
api_router.include_permissions_router(departments.router, prefix_permissions="departments", tags=["departments"])
api_router.include_permissions_router(branches.router, prefix_permissions="branches", tags=["branches"])
api_router.include_router(stages.router, prefix="/stages", tags=["stages"])
api_router.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(floors.router, prefix="/floors", tags=["floors"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(cards.router, prefix="/cards", tags=["cards"])
