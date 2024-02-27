from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.core.model import Base

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()