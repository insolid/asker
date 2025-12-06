from fastapi import APIRouter

from app.core.fastapi_users_config import fastapi_users as fu
from app.schemas.users import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

router.include_router(fu.get_users_router(UserRead, UserUpdate))
