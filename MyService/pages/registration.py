from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from MyService.api_v1.auth.dependencies import get_user_soft
from MyService.api_v1.users import crud
from MyService.api_v1.users.dependencies import prepare_user_create
from MyService.core.db import get_db
from MyService.core.entities.users import UserCreateDB
from MyService.templates import templates

router = APIRouter()


@router.get("/registration/")
async def registration_page(request: Request,
                            user=Depends(get_user_soft)):
    # Отдаем HTML с формой регистрации через шаблон
    return templates.TemplateResponse("registration.html", {"request": request, "user": user})


@router.post("/registration/")
async def create_user_with_redirect(
        request: Request,
        user_data: UserCreateDB = Depends(prepare_user_create),
        session: AsyncSession = Depends(get_db),
):
    try:
        user = await crud.create_user(session=session, user_data=user_data)
    except IntegrityError:
        # В случае дублирования возвращаем форму с ошибкой
        error = "Пользователь с таким именем или email уже существует."
        return templates.TemplateResponse(
            "registration.html",
            {
                "request": request,
                "error": error
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # Если успешна регистрация — редирект на главную
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
