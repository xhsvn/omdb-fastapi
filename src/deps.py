from typing import Annotated

from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.models.user import User
from src.schemas.auth_schema import JWTData
from src.core.exceptions import AuthRequired, InvalidToken, UserNotFound
from src.services.user_service import UserService
from src.settings import get_settings, Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/doc", auto_error=False)


SettingsDep = Annotated[Settings, Depends(get_settings)]


async def get_current_user(
    settings: SettingsDep,
    user_service: Annotated[UserService, Depends()],
    token: str | None = Depends(oauth2_scheme),
) -> User:
    """
    Get the current user from the token
    if the user does not exist, an exception is raised.

    :param token: User data from the token
    :returns: User object with the same id as in the token
    """
    if not token:
        raise AuthRequired()

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    except JWTError:
        raise InvalidToken()

    data = JWTData(**payload)

    user = await user_service.get_user_by_id(data.user_id)
    if not user:
        raise UserNotFound()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
