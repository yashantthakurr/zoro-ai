
from src.backend.dependencies.database import get_db
from fastapi import APIRouter, Depends, status
from src.backend.schemas.user import UserResponse, UserUpdate
from typing import Annotated
from sqlalchemy.orm import Session
from src.backend.models.user import User
from src.backend.services import user as user_service
from src.backend.constants.naming import USERS_API_PREFIX
from typing import List
from src.backend.dependencies.auth import get_current_user
from src.backend.roles.user import UserRole
from src.backend.exceptions.auth import NOT_AUTHORIZED_FOR_ADMIN_ENDPOINTS_EXCEPTION

router = APIRouter(
    prefix=USERS_API_PREFIX,
    tags=["Users Routes"]
)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_myself(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user


@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_myself(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)], data: UserUpdate) -> User:
    return user_service.self_update_user(db, user, data)


@router.delete("/me", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def get_me(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]) -> None:
    return user_service.self_delete_user(db, user)


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]) -> List[User]:
    if current_user.role != UserRole.ADMIN:
        raise NOT_AUTHORIZED_FOR_ADMIN_ENDPOINTS_EXCEPTION
    return user_service.fetch_all_users(db)


@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise NOT_AUTHORIZED_FOR_ADMIN_ENDPOINTS_EXCEPTION
    return user_service.fetch_user_by_id(db, id)


@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user_by_id(id: int, data: UserUpdate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise NOT_AUTHORIZED_FOR_ADMIN_ENDPOINTS_EXCEPTION
    return user_service.update_user_by_id(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]) -> None:
    if current_user.role != UserRole.ADMIN:
        raise NOT_AUTHORIZED_FOR_ADMIN_ENDPOINTS_EXCEPTION
    return user_service.delete_user_by_id(db, id)

