from sqlalchemy import select, exists

from src.core.database import DBSession
from src.models.movie_import import MovieImport


class MovieImportRepository:
    """Class for accessing movie table."""

    def __init__(self, session: DBSession):
        self.session = session

    async def add_movie_import(self, movie_import: MovieImport) -> MovieImport:
        """
        Add movie to database.
        :param movie:
        :return: Movie object
        """
        self.session.add(movie_import)
        await self.session.flush()

    async def exists_movie_import_by_title(self, title: str) -> bool:
        """
        Check if movie with given title exists.
        :param title:
        :return: True if movie exists, False otherwise
        """
        res = await self.session.execute(
            select(exists().where(MovieImport.title == title))
        )
        return res.scalar()

    async def get_movie_import_or_none_by_id(
        self, movie_import_id: int
    ) -> MovieImport | None:
        """
        Get movie by id or return None.
        :param movie_id:
        :return: Movie object or None
        """
        res = await self.session.execute(
            select(MovieImport).filter(MovieImport.id == movie_import_id)
        )
        return res.scalar_one_or_none()

    async def get_movie_or_none_by_title(self, title: str) -> MovieImport | None:
        """
        Get movie by title or return None.
        :param title:
        :return: Movie object or None
        """
        res = await self.session.execute(
            select(MovieImport).filter(MovieImport.title == title)
        )
        return res.scalar_one_or_none()

    async def delete_movie(self, movie_import: MovieImport):
        """
        Delete movie.
        :param movie:
        :return: None
        """
        await self.session.delete(movie_import)
