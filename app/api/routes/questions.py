from fastapi import APIRouter, HTTPException, Depends
from app.schemas.questions import QuestionRead, QuestionCreate, QuestionReadShort
from app.core.db import SessionDep
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.questions import Question
from ..deps.auth import CurrentUserDep
from ..deps.questions import QuestionByIDFromUrl
from typing import Annotated

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionReadShort])
async def list_questions(db: SessionDep):
    return await db.scalars(select(Question))


@router.get("/{id}", response_model=QuestionRead)
async def retrieve_question(
    question: Annotated[Question, Depends(QuestionByIDFromUrl(Question.answers))],
):
    return question


@router.post("/", response_model=QuestionReadShort)
async def create_question(
    db: SessionDep, question_data: QuestionCreate, cur_user: CurrentUserDep
):
    question = Question(user_id=cur_user.id, **question_data.model_dump())
    db.add(question)
    await db.commit()
    return question


@router.delete("/{id}", response_model=QuestionReadShort)
async def delete_question(
    cur_user: CurrentUserDep,
    question: Annotated[Question, Depends(QuestionByIDFromUrl())],
    db: SessionDep,
):
    if question.user_id != cur_user.id:
        raise HTTPException(404, "Item not found")
    await db.delete(question)
    await db.commit()
    return question
