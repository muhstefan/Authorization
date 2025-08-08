from fastapi import Depends, Response, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from MyService.api_v1.auth.config import Production
from MyService.api_v1.auth.crud import get_user_by_username
from MyService.api_v1.auth.dependencies import get_user_soft
from MyService.api_v1.auth.security import verify_password, generate_and_set_tokens
from MyService.core.db import get_db
from MyService.templates import templates

router = APIRouter()


@router.get("/login/")
async def login_page(request: Request,
                     user=Depends(get_user_soft)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


@router.post("/login/")
async def login(request: Request,
                response: Response,
                form_data: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(session, form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверный логин или пароль",
                "username": form_data.username
            },
            status_code=400
        )

    generate_and_set_tokens(response, str(user.id), secure=Production)

    redirect_response = RedirectResponse(url="/", status_code=303)
    for header, value in response.headers.items():
        redirect_response.headers[header] = value
    return redirect_response


@router.post("/logout/")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=Production
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=Production
    )
    return response
