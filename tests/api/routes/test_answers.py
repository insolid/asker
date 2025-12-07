import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answers import Answer
from app.models.questions import Question
from app.models.users import User

pytestmark = pytest.mark.asyncio


async def test_create_answer(
    auth_client: AsyncClient, app: FastAPI, test_user: User, test_question: Question
):
    payload = {"text": "some text"}
    res = await auth_client.post(
        app.url_path_for("create_answer", id=test_question.id), json=payload
    )
    assert res.status_code == 201
    data = res.json()
    assert data["text"] == payload["text"]
    assert data["user_id"] == str(test_user.id)
    assert data["question_id"] == test_question.id
    assert "created_at" in data


async def test_answer_to_non_existent_question_error(
    auth_client: AsyncClient, app: FastAPI
):
    res = await auth_client.post(app.url_path_for("create_answer", id=999), json={})
    assert res.status_code == 404


async def test_get_answer(auth_client: AsyncClient, app: FastAPI, test_answer: Answer):
    res = await auth_client.get(app.url_path_for("get_answer", id=test_answer.id))
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_answer.id


async def test_delete_answer(
    auth_client: AsyncClient,
    app: FastAPI,
    db: AsyncSession,
    test_answer: Answer,
):
    res = await auth_client.delete(app.url_path_for("delete_answer", id=test_answer.id))
    assert res.status_code == 200
    answer = await db.scalar(select(Answer).where(Answer.id == test_answer.id))
    assert answer is None
