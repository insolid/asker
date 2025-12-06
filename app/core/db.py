from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
from collections.abc import AsyncGenerator
from fastapi import Depends
from .config import settings

engine = create_async_engine(str(settings.postgres_dsn))

local_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
