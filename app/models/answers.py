import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )
