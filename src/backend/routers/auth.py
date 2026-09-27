
from fastapi import APIRouter, Depends, Request, status
from src.backend.constants.naming import AUTH_API_PREFIX
from src.backend.dependencies.database import get_db
from src.backend.dependencies.rate_limit import limiter
from src.backend.models.user import User
from src.backend.schemas.access_token import AccessToken
from src.backend.schemas.user import UserSignup, UserResponse, UserSignin
from src.backend.services import auth as auth_service
from sqlalchemy.orm import Session
from typing import Annotated, Dict

router = APIRouter(
    prefix=AUTH_API_PREFIX,
    tags=["Authentication Routes"]
)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def user_sign_up(request: Request, data: UserSignup, db: Annotated[Session, Depends(get_db)]) -> User:
    return auth_service.create_new_user(db, data)

@router.post("/signin", response_model=AccessToken, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def user_sign_in(request: Request, data: UserSignin, db: Annotated[Session, Depends(get_db)]) -> Dict[str, str]:
    return auth_service.authenticate_user(db, data)
