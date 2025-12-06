from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.db import SessionDep
from app.models.questions import Question


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
            raise HTTPException(404, "Question not found")
        return vj
