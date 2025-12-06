import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    answers: Mapped[list["Answer"]] = relationship(cascade="all, delete-orphan")
