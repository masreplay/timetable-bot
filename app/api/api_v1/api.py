from app.api.api_v1.endpoints import (users, roles, periods, auth, job_title, stages, departments, branches)
from app.core.utils.utils import APIPermissionsRouter

api_router = APIPermissionsRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
api_router.include_router(job_title.router, prefix="/job_titles", tags=["job titles"])
api_router.include_permissions_router(departments.router, prefix_permissions="departments", tags=["departments"])
api_router.include_permissions_router(branches.router, prefix_permissions="branches", tags=["branches"])
api_router.include_router(stages.router, prefix="/stages", tags=["stages"])
