from fastapi import APIRouter

from MyService.pages.home import router as home_page_router
from MyService.pages.login import router as login_pages_router
from MyService.pages.registration import router as registration_page_router

router = APIRouter(tags=["Pages"])

router.include_router(login_pages_router, prefix="/pages")  # или другой префикс, если нужно
router.include_router(home_page_router, prefix="/pages")  # или другой префикс, если нужно
router.include_router(registration_page_router, prefix="/pages")  # или другой префикс, если нужно
