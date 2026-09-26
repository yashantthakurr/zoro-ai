
from collections.abc import Generator
from src.backend import models
from src.backend.auth import security
from src.backend.constants.config import secrets
from src.backend.database.session import engine, SessionLocal
from src.backend.models.user import User
from src.backend.roles.user import UserRole
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def init_db() -> None:

    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if not db.query(User).filter(User.username==secrets.ADMIN_USERNAME).first():
            user = User(
                email=secrets.ADMIN_EMAIL,
                username=secrets.ADMIN_USERNAME,
                hashed_password=security.hash_password(secrets.ADMIN_PASSWORD),
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
