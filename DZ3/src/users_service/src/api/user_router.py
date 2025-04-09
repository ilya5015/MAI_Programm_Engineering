from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.db import get_async_session
from ..db.schemas import UserCreateRequest, UserResponse
from ..services.user_service import UserService
from ..controller.UserController import UserController
from ..tools.auth import verify_token

router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService(repo=UserController())


@router.post("", response_model=UserResponse, dependencies=[Depends(verify_token)])
async def create_user(payload: UserCreateRequest, session: AsyncSession = Depends(get_async_session),):
    """
    Создаём нового пользователя.
    """
    try:
        user = await user_service.register_user(session=session, login=payload.login, password=payload.password, first_name=payload.first_name,last_name=payload.last_name,)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{login}", response_model=UserResponse, dependencies=[Depends(verify_token)])
async def get_user_by_login(login: str, session: AsyncSession = Depends(get_async_session),):
    """
    Получаем информацию о пользователе по логину.
    """
    user = await user_service.get_user_by_login(session, login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.get("", response_model=List[UserResponse], dependencies=[Depends(verify_token)])
async def search_users(name: Optional[str] = Query(default=None), session: AsyncSession = Depends(get_async_session),):
    """
    Поиск пользователей по имени/фамилии (или только по имени, или только по фамилии).
    """
    users = await user_service.find_users_by_name(session, name)
    return [UserResponse.model_validate(u) for u in users]
