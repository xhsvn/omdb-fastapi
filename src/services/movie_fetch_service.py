from typing import Annotated

from fastapi import Depends

from src.core.database import DBSession
from src.models.movie_import import ImportStatus
from src.models.movie import Movie
from src.repositories.movie_repository import MovieRepository
from src.repositories.movie_import_repository import MovieImportRepository
from src.services.omdb_service import OmdbServiceDep
from src.schemas.movie_schema import MovieOmdb

from loguru import logger


class MovieFetchService:
    def __init__(
        self,
        movie_repository: Annotated[MovieRepository, Depends()],
        movie_import_repository: Annotated[MovieImportRepository, Depends()],
        session: DBSession,
        omdb_service: OmdbServiceDep,
    ):
        self.movie_import_repository = movie_import_repository
        self.movie_repository = movie_repository
        self.omdb_service = omdb_service
        self.session = session

    async def fetch_movie_data(self, movie_title: str, movie_import_id: str):
        """
        Fetch movie data from omdbapi and update the movie with the fetched data.
        check if movie already fetched
        :param movie_title:
        :param movie_id:
        :return:
        """
        logger.info(f"Fetching movie data for movie {movie_title}")

        async with self.session.begin():
            movie_import = (
                await self.movie_import_repository.get_movie_import_or_none_by_id(
                    movie_import_id
                )
            )

            if not movie_import or movie_import.status != ImportStatus.FETCHING:
                logger.info(f"Movie {movie_title} already fetched")
                return

            movie = await self.movie_repository.get_movie_or_none_by_title(movie_title)
            if movie:
                logger.info(f"Movie {movie_title} already imported")
                movie_import.movie_id = movie.id
                movie_import.status = ImportStatus.FETCHED
                await self.movie_import_repository.add_movie_import(movie_import)
                return

        result = await self.omdb_service.get_movie_by_title(movie_title)

        if result.get("Response") == "False":
            movie_import.status = ImportStatus.NOT_FOUND
            await self.movie_import_repository.add_movie_import(movie_import)
            return
        else:
            body = MovieOmdb(**result).model_dump()
            movie = Movie(**body)
            await self.movie_repository.add_movie(movie)

            movie_import.movie_id = movie.id
            movie_import.status = ImportStatus.FETCHED
            await self.movie_import_repository.add_movie_import(movie_import)
            return

    async def process_dead_letter(self, movie_title: str, movie_import_id: str):
        """
        Process dead letter queue for now just set the status to error and log

        :param movie_title:
        :param movie_id:
        :return:
        """
        logger.info(f"Processing dead letter for movie {movie_title}")

        movie_import = (
            await self.movie_import_repository.get_movie_import_or_none_by_id(
                movie_import_id
            )
        )

        if not movie_import:
            logger.info(f"Movie {movie_title} not found")
            return

        movie_import.status = ImportStatus.ERROR
        await self.movie_import_repository.add_movie_import(movie_import)
        return movie_import
