from fastapi import Depends
from typing import Annotated
from app.models.users import User
from app.core.fastapi_users_config import fastapi_users as fu

current_user = fu.current_user(active=True)
CurrentUserDep = Annotated[User, Depends(current_user)]
