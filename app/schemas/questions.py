import uuid

from pydantic import BaseModel

from .answers import AnswerRead


class QuestionCreate(BaseModel):
    text: str


class QuestionRead(QuestionCreate):
    id: int
    user_id: uuid.UUID
    answers: list[AnswerRead] = []
