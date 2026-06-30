import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ChatSession(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    customer_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("customers.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), default="active")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    satisfaction_rating: Mapped[int | None] = mapped_column(Integer)

    customer = relationship("Customer", back_populates="sessions")
    messages = relationship("Message", back_populates="session")
    actions = relationship("Action", back_populates="session")
