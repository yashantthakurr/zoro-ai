
from src.backend.auth import security
from src.backend.exceptions import auth as auth_exceptions
from src.backend.exceptions import user as user_exceptions
from src.backend.models.user import User
from src.backend.roles.user import UserRole
from src.backend.schemas.user import UserSignup, UserSignin
from sqlalchemy.orm import Session
from typing import Dict

def create_new_user(db: Session, data: UserSignup) -> User:
    if db.query(User).filter(User.email==data.email).first():
        raise user_exceptions.EMAIL_ALREADY_TAKEN_EXCEPTION
    if db.query(User).filter(User.username==data.username).first():
        raise user_exceptions.USERNAME_ALREADY_TAKEN_EXCEPTION
    user = User(
        email=data.email,
        username=data.username,
        hashed_password=security.hash_password(data.password),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, data: UserSignin) -> Dict[str, str]:
    user = db.query(User).filter(User.username==data.username).first()
    if not user or not security.verify_passowrd(data.password, user.hashed_password):
        raise auth_exceptions.INVALID_CREDENTIALS_EXCEPTIONS
    return {
        "access_token": security.generate_access_token(data.username),
        "username": data.username,
        "role": user.role,
        "token_type": "bearer"
    }
