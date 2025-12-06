from typing import Annotated

from fastapi import Depends

from app.core.fastapi_users_config import fastapi_users as fu
from app.models.users import User

current_user = fu.current_user(active=True)
CurrentUserDep = Annotated[User, Depends(current_user)]
