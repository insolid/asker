import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.config import settings
from app.core.db import SessionDep
from app.models.users import User

SECRET = "SECRET"


async def get_user_db(session: SessionDep):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    pass


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.jwt_secret_key,
        lifetime_seconds=settings.jwt_expire_minutes * 60,
    )


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy
)
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
