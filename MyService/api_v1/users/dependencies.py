from fastapi import Depends, HTTPException, status, Form
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MyService.core.entities.users import UserUpdate, UserCreateDB
from MyService.core.models import db_helper, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def prepare_user_create(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
) -> UserCreateDB:
    password_hash = pwd_context.hash(password)
    return UserCreateDB(username=username, email=email, password_hash=password_hash)


async def prepare_user_update(
        user_id: int,
        user_update: UserUpdate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    update_data = user_update.model_dump(exclude_unset=True)

    # Проверка уникальности username
    if "username" in update_data:
        existing_user = await session.execute(
            select(User).where(User.username == update_data["username"], User.id != user_id)
        )
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой Логин уже есть"
            )

    # Проверка уникальности email
    if "email" in update_data:
        existing_email = await session.execute(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        )
        if existing_email.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой Email уже есть"
            )

    # Хеширование пароля
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    return update_data
