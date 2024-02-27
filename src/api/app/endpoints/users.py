from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.core.schema import ExceptionModel
from src.schemas import user_schema
from src.services.user_service import UserService
from src.deps import CurrentUser

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.User,
    summary="Create a new user",
    description="Create a new user with the given username and password.",
    response_description="The created user",
    responses={status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel}},
)
async def register_user(
    user_create: user_schema.UserCreate, services: Annotated[UserService, Depends()]
):
    """
    Create a new user with the given username and password.

    :param user_create:
    :return: Created user
    """
    return await services.create_user(user_create)


@router.get(
    "/me",
    response_model=user_schema.User,
    summary="Get current user",
    description="Get the current user.",
    response_description="The current user",
    )
async def get_user(user: CurrentUser):
    """
    Get the current user.
    :param user:

    :return: Current user
    """
    return user
