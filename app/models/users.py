from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from .base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    questions: Mapped[list["Question"]] = relationship(cascade="all, delete-orphan")
    answers: Mapped[list["Answer"]] = relationship(cascade="all, delete-orphan")
