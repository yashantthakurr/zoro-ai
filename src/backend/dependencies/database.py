
from collections.abc import Generator
from src.backend.database.session import SessionLocal
from sqlalchemy.orm import Session
from src.backend.roles.user import UserRole
from src.backend.models.user import User
from src.backend.auth import security


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username=="yashantthakurr").first():
            user = User(
                email="yashant.thakur2007@gmail.com",
                username="yashantthakurr",
                hashed_password=security.hash_password("12345678"),
                role=UserRole.ADMIN
            )
            db.add(user)
            db.commit()
            db.refresh(user)
    except Exception:
        db.rollback()
        print("Cannot connect to the database.")
    finally:
        db.close()
