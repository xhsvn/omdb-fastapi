from sqlalchemy import select

from src.core.database import DBSession
from src.models.user import User

class UserRepository:
    """Class for accessing user table."""


    def __init__(self, session: DBSession):
        self.session = session
        
    
    async def add_user(self, user: User) -> User:
        """
        Add user to database.
        :param user:
        :return: User object
        """
        self.session.add(user)
        await self.session.flush()

    
    async def get_user_or_none_by_username(self, username: str) -> User | None:
        """
        Get user by username or return None.
        :param username:
        :return: User object or None
        """
        res = await self.session.execute(select(User).filter(User.username == username))
        return res.scalar_one_or_none()

    async def get_user_or_none_by_id(self, id: str) -> User | None:
        """
        Get user by id or return None.
        :param id:
        :return: User object or None
        """
        res = await self.session.execute(select(User).filter(User.id == id))
        return res.scalar_one_or_none()