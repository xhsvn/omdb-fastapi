import enum

from sqlalchemy.orm import Mapped, mapped_column
from src.core.model import Base

class Rating(Base):
    __tablename__ = "ratings"

    source: Mapped[str] = mapped_column()
    value: Mapped[str] = mapped_column()
    movie_id: Mapped[int] = mapped_column()


class Movie(Base):
    __tablename__ = "movies"
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] = mapped_column(nullable=True)
    rated: Mapped[str] = mapped_column(nullable=True)
    released: Mapped[str] = mapped_column(nullable=True)
    runtime: Mapped[str] = mapped_column(nullable=True)
    genre: Mapped[str] = mapped_column(nullable=True)
    director: Mapped[str] = mapped_column(nullable=True)
    writer: Mapped[str] = mapped_column(nullable=True)
    actors: Mapped[str] = mapped_column(nullable=True)
    plot: Mapped[str] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    awards: Mapped[str] = mapped_column(nullable=True)
    poster: Mapped[str] = mapped_column(nullable=True)
    metascore: Mapped[str] = mapped_column(nullable=True)
    imdb_rating: Mapped[str] = mapped_column(nullable=True)
    imdb_votes: Mapped[str] = mapped_column(nullable=True)
    imdb_id: Mapped[str] = mapped_column(nullable=True)
    dvd: Mapped[str] = mapped_column(nullable=True)
    box_office: Mapped[str] = mapped_column(nullable=True)
    production: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    # ratings: 

