
from typing import Annotated

from datetime import datetime, timedelta
from fastapi import Depends

from jose import jwt

from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.core.security import verify_password
from src.core.exceptions import InvalidCredentials
from src.deps import SettingsDep

class AuthService:

    def __init__(self,
        user_repository: Annotated[UserRepository, Depends()],
        settings: SettingsDep):
        self.user_repository = user_repository
        self.settings = settings

    async def authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticate a user with the given username and password.
        :param username:
        :param password:
        :return: User object
        """
        user = await self.user_repository.get_user_or_none_by_username(username)

        if not user:
            raise InvalidCredentials()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentials()

        return user


    async def login(self, username: str, password: str) -> str:
        """
        Authenticate a user with the given username and password and return the access token.
        :param username:
        :param password:
        :return: JWT access token
        """
        user = await self.authenticate_user(username, password)
        jwt_data = {
            "sub": str(user.id),
            'exp': datetime.utcnow() + timedelta(minutes=self.settings.jwt_exp)
        }
        access_token = jwt.encode(jwt_data, self.settings.jwt_secret, algorithm=self.settings.jwt_alg)   
        return access_token