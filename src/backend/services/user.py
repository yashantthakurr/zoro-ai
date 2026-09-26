
from src.backend.auth import security
from src.backend.exceptions import user as user_exceptions
from src.backend.exceptions.auth import INVALID_CREDENTIALS_EXCEPTIONS
from src.backend.models.user import User
from src.backend.schemas.user import UserUpdate
from sqlalchemy.orm import Session
from typing import List

def fetch_user_by_id(db: Session, id: int) -> User:
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise user_exceptions.CANNOT_FIND_USER_WITH_ID_EXCEPTION
    return user

def fetch_all_users(db: Session) -> List[User]:
    return db.query(User).all()

def update_user_by_id(db: Session, id: int, data: UserUpdate) -> User:
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise user_exceptions.CANNOT_FIND_USER_WITH_ID_EXCEPTION
    if data.email is not None:
        if db.query(User).filter(User.email==data.email, User.id!=id).first():
                raise user_exceptions.EMAIL_ALREADY_TAKEN_EXCEPTION
        user.email=data.email
    if data.username is not None:
        if db.query(User).filter(User.username==data.username, User.id!=id).first():
                raise user_exceptions.USERNAME_ALREADY_TAKEN_EXCEPTION
        user.username=data.username
    if data.new_password is not None:
         user.hashed_password=security.hash_password(data.new_password)
    db.commit()
    db.refresh(user)
    return user

def delete_user_by_id(db: Session, id: int) -> None:
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise user_exceptions.CANNOT_FIND_USER_WITH_ID_EXCEPTION
    db.delete(user)
    db.commit()

def self_update_user(db: Session, user: User, data: UserUpdate) -> User:
    if not security.verify_passowrd(data.current_password, user.hashed_password):
        raise INVALID_CREDENTIALS_EXCEPTIONS
    if data.email is not None:
        if db.query(User).filter(User.email==data.email, User.email!=user.email).first():
            raise user_exceptions.EMAIL_ALREADY_TAKEN_EXCEPTION
        user.email=data.email
    if data.username is not None:
        if db.query(User).filter(User.username==data.username, User.username!=user.username).first():
            raise user_exceptions.USERNAME_ALREADY_TAKEN_EXCEPTION
        user.username=data.username
    if data.new_password is not None:
        user.hashed_password=security.hash_password(data.new_password)
    db.commit()
    db.refresh(user)
    return user

def self_delete_user(db: Session, user: User) -> None:
     db.delete(user)
     db.commit()
