import uuid

from pydantic import BaseModel


class AnswerCreate(BaseModel):
    text: str


class AnswerRead(AnswerCreate):
    id: int
    user_id: uuid.UUID
    question_id: int
