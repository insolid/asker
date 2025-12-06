from fastapi import FastAPI
from app.api.routes import auth, users, questions

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questions.router)