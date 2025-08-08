from fastapi import APIRouter

from MyService.api_v1.admin.views import router as admin_router
from MyService.api_v1.auth.views import router as auth_router
from MyService.api_v1.users.views import router as users_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=admin_router, prefix="/admin")
