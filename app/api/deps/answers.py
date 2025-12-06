from fastapi import HTTPException
from sqlalchemy import select

from app.core.db import SessionDep
from app.models.answers import Answer


async def get_answer_by_id_from_url(
    db: SessionDep,
    id: int,
) -> Answer:
    answer = await db.scalar(select(Answer).where(Answer.id == id))
    if not answer:
        raise HTTPException(404, "Answer not found")
    return answer
