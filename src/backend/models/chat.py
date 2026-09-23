
from datetime import datetime
from src.backend.database.base import Base
from sqlalchemy import DateTime, func, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    session_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.current_timestamp(),
        default=func.current_timestamp(),
        nullable=False
    )
