from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, FileResponse
from starlette.requests import Request


from MyService.api_v1.auth.config import Production
from MyService.api_v1.auth.dependencies import get_user_soft
from MyService.templates import templates

router = APIRouter()


@router.get("/login/")
async def login_page(request: Request,
                     user=Depends(get_user_soft)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


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
