from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.schema import ExceptionModel
from src.schemas import auth_schema
from src.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])



@router.post(
    "/doc", response_model=auth_schema.AccessTokenResponse, include_in_schema=False
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends()],
    ) -> auth_schema.AccessTokenResponse:
    """
    Authenticate a user with the given username and password for using the API docs.

    :param form_data: form data with username and password
    :return: access token
    """
    access_token = await auth_service.login(
        username=form_data.username, password=form_data.password
    )
    return auth_schema.AccessTokenResponse(access_token=access_token)


@router.post(
    "",
    response_model=auth_schema.AccessTokenResponse,
    summary="Authenticate user",
    description="Authenticate a user with the given username and password.",
    response_description="The access token",
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel}},
)
async def authenticate_user(
    auth_data: auth_schema.AuthData,
    auth_service: Annotated[AuthService, Depends()]
    ) -> auth_schema.AccessTokenResponse:

    """
    Authenticate a user with the given username and password and return an access token.

    :param auth_data:
    :return: access token
    """
    access_token = await auth_service.login(
        username=auth_data.username, password=auth_data.password
    )
    return auth_schema.AccessTokenResponse(access_token=access_token)