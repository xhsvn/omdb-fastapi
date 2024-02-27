from sqlalchemy import select, exists

from src.core.database import DBSession
from src.models.movie import Movie


class MovieRepository:
    """Class for accessing movie table."""

    def __init__(self, session: DBSession):
        self.session = session

    async def list_movies(self, offset: int, limit: int) -> list[Movie]:
        """
        List movies with pagination ond default ordering on title.
        :param offset:
        :param limit:
        :return: List of Movie objects
        """
        res = await self.session.execute(
            select(Movie).offset(offset).limit(limit).order_by(Movie.title)
        )
        return res.scalars().all()

    async def add_movie(self, movie: Movie) -> None:
        """
        Add movie to database.
        :param movie: Movie object to add
        :return: None
        """
        self.session.add(movie)
        await self.session.flush()

    async def get_movie_or_none_by_id(self, movie_id: int) -> Movie | None:
        """
        Get movie by id or return None.
        :param movie_id: id of movie to get
        :return: Movie object or None
        """
        res = await self.session.execute(select(Movie).filter(Movie.id == movie_id))
        return res.scalar_one_or_none()

    async def get_movie_or_none_by_title(self, title: str) -> Movie | None:
        """
        Get movie by title or return None.
        :param title: title of movie to get
        :return: Movie object or None
        """
        res = await self.session.execute(select(Movie).filter(Movie.title == title))
        return res.scalar_one_or_none()

    async def exists_movie_by_title(self, title: str) -> bool:
        """
        Check if movie with given title exists.
        :param title: title of movie to check
        :return: True if movie exists, False otherwise
        """
        res = await self.session.execute(select(exists().where(Movie.title == title)))
        return res.scalar_one()

    async def delete_movie(self, movie: Movie):
        """
        Delete movie.
        :param movie:
        :return: None
        """
        await self.session.delete(movie)
