
from datetime import datetime
from src.backend.database.base import Base
from sqlalchemy import DateTime, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(24),
        index=True,
        nullable=False,
        unique=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(5),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.current_timestamp(),
        default=func.current_timestamp(),
        nullable=False
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=False),
        server_onupdate=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True
    )
