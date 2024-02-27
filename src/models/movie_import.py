import enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, ForeignKey
from src.core.model import Base


class ImportStatus(enum.Enum):
    FETCHING = "fetching"
    FETCHED = "fetched"
    NOT_FOUND = "not_found"
    ERROR = "error"


class MovieImport(Base):
    __tablename__ = "movie_imports"
    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus), default=ImportStatus.FETCHING, nullable=False
    )
    title: Mapped[str] = mapped_column(unique=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=True)
