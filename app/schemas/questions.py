import uuid
from datetime import datetime

from pydantic import BaseModel

from .answers import AnswerRead


class QuestionCreate(BaseModel):
    text: str


class QuestionReadShort(QuestionCreate):
    id: int
    user_id: uuid.UUID
    created_at: datetime


class QuestionRead(QuestionReadShort):
    answers: list[AnswerRead] = []
