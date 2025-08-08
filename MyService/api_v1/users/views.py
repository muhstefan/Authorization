from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from MyService.api_v1.auth import get_user_strict
from MyService.core.db import get_db
from MyService.core.entities.users import UserCreateDB, UserPublic
from . import crud
from .dependencies import prepare_user_create, prepare_user_update

router = APIRouter(tags=["Users"])


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreateDB = Depends(prepare_user_create),
        session: AsyncSession = Depends(get_db)
):
    user = await crud.create_user(session=session, user_data=user_data)
    return UserPublic.model_validate(user)


@router.get("/me/", response_model=UserPublic)
async def get_current_user(
        current_user: "User" = Depends(get_user_strict),  # Проверка, что пользователь login in
):
    return current_user


@router.put("/{user_id}/", response_model=UserPublic)
async def update_user(
        user_id: int,
        update_data: dict = Depends(prepare_user_update),
        session: AsyncSession = Depends(get_db),

):
    updated_user = await crud.update_user(session=session, user_id=user_id, update_data=update_data)
    return UserPublic.model_validate(updated_user)


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_db)
) -> None:
    await crud.delete_user(session=session, user_id=user_id)


@router.get("/all/")
async def get_users(session: AsyncSession = Depends(get_db)):
    return await crud.get_users(session=session)
