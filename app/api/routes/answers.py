from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.core.db import SessionDep
from app.models.answers import Answer
from app.models.questions import Question
from app.schemas.answers import AnswerCreate, AnswerRead

from ..deps.answers import get_answer_by_id_from_url
from ..deps.auth import CurrentUserDep
from ..deps.questions import QuestionByIDFromUrl

router = APIRouter(prefix="", tags=["answers"])


@router.get("/answers/{id}", response_model=AnswerRead)
async def get_answer(answer: Annotated[Answer, Depends(get_answer_by_id_from_url)]):
    return answer


@router.delete("/answers/{id}", response_model=AnswerRead)
async def delete_answer(
    answer: Annotated[Answer, Depends(get_answer_by_id_from_url)],
    db: SessionDep,
    cur_user: CurrentUserDep,
):
    if not answer.user_id == cur_user.id:
        raise HTTPException(404, "Answer not found")
    await db.delete(answer)
    await db.commit()
    return answer


@router.post("/questions/{id}/answers", response_model=AnswerRead)
async def create_answer(
    question: Annotated[Question, Depends(QuestionByIDFromUrl())],
    db: SessionDep,
    cur_user: CurrentUserDep,
    answer_data: AnswerCreate,
):
    answer = Answer(
        user_id=cur_user.id,
        question_id=question.id,
        **answer_data.model_dump(),
    )
    db.add(answer)
    await db.commit()
    return answer
