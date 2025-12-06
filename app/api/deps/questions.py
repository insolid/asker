from app.core.db import SessionDep
from app.models.questions import Question
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException


class QuestionByIDFromUrl:
    def __init__(self, *select_in_load):
        self.select_in_load = select_in_load

    async def __call__(
        self,
        db: SessionDep,
        id: int,
    ) -> Question:
        vj = await db.scalar(
            select(Question)
            .where(Question.id == id)
            .options(*[selectinload(field) for field in self.select_in_load])
        )
        if not vj:
            raise HTTPException(404, "Item not found")
        return vj
