import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answers import Answer
from app.models.questions import Question
from app.models.users import User

pytestmark = pytest.mark.asyncio


async def test_create_question(auth_client: AsyncClient, app: FastAPI):
    payload = {"text": "some text"}
    res = await auth_client.post(app.url_path_for("create_question"), json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["text"] == payload["text"]
    assert "user_id" in data
    assert "created_at" in data


async def test_create_question_auth_required(client: AsyncClient, app: FastAPI):
    res = await client.post(app.url_path_for("create_question"), json={})
    assert res.status_code == 401


async def test_list_questions(
    auth_client: AsyncClient, app: FastAPI, test_user: User, db: AsyncSession
):
    q1 = Question(user_id=test_user.id, text="q1")
    q2 = Question(user_id=test_user.id, text="q2")
    db.add_all([q1, q2])
    await db.commit()

    res = await auth_client.get(app.url_path_for("list_questions"))
    assert res.status_code == 200
    assert len(res.json()) == 2


async def test_get_question(
    auth_client: AsyncClient,
    app: FastAPI,
    test_user: User,
    db: AsyncSession,
    test_question: Question,
):
    res = await auth_client.get(app.url_path_for("get_question", id=test_question.id))
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_question.id
    assert "answers" in data


async def test_delete_question(
    auth_client: AsyncClient,
    app: FastAPI,
    db: AsyncSession,
    test_question: Question,
):
    res = await auth_client.delete(
        app.url_path_for("delete_question", id=test_question.id)
    )
    assert res.status_code == 200
    q = await db.scalar(select(Question).where(Question.id == test_question.id))
    assert q is None
    answers = await db.scalars(
        select(Answer).where(Answer.question_id == test_question.id)
    )
    assert len(answers.all()) == 0
