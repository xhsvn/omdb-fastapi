from typing import Annotated

from fastapi import Depends

from src.schemas import user_schema
from src.models.user import User as UserModel
from src.repositories.user_repository import UserRepository
from src.core.exceptions import UsernameTaken
from src.core.security import get_password_hash


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self.user_repository = user_repository

    async def create_user(self, user_create: user_schema.UserCreate) -> UserModel:
        """
        Create a new user with the given username and password.

        :param user: User data
        :return: Created user
        """
        user = await self.user_repository.get_user_or_none_by_username(
            user_create.username
        )

        if user is not None:
            raise UsernameTaken()

        user = UserModel(
            hashed_password=get_password_hash(user_create.password),
            **user_create.model_dump(exclude=["password"]),
        )

        await self.user_repository.add_user(user)
        return user

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        """
        Get user by id.

        :param user_id:
        :return: User object
        """
        return await self.user_repository.get_user_or_none_by_id(user_id)
