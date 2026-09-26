
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.backend.constants.config import secrets
from src.backend.dependencies.database import get_db
from src.backend.exceptions.auth import INVALID_OR_EXPIRED_TOKEN_EXCEPTION
from src.backend.models.user import User
from sqlalchemy.orm import Session
from typing import Annotated

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/signin")

def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Depends(oauth2scheme)) -> User:
    try:
        payload = jwt.decode(token, secrets.SECRET_KEY, algorithms=[secrets.ALGORITHM])
        username = payload.get("subject")
        if username is None:
            raise INVALID_OR_EXPIRED_TOKEN_EXCEPTION
    except JWTError:
        raise INVALID_OR_EXPIRED_TOKEN_EXCEPTION
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise INVALID_OR_EXPIRED_TOKEN_EXCEPTION
    return user
