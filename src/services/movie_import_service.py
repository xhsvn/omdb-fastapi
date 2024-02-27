from typing import Annotated

from fastapi import Depends, BackgroundTasks


from src.core.exceptions import MovieAlreadyExists, MovieAlreadySubmitted
from src.models.movie_import import MovieImport
from src.repositories.movie_import_repository import MovieImportRepository
from src.repositories.movie_repository import MovieRepository
from src.schemas.movie_import_schema import MovieImportCreate
from src.services.queue_service import QueueServiceDep
from src.utils.logging import call_logger


class MovieImportService:
    def __init__(
        self,
        movie_import_repository: Annotated[MovieImportRepository, Depends()],
        movie_repository: Annotated[MovieRepository, Depends()],
        background_tasks: BackgroundTasks,
        queue_service: QueueServiceDep,
    ):
        self.movie_import_repository = movie_import_repository
        self.movie_repository = movie_repository
        self.background_tasks = background_tasks
        self.queue_service = queue_service

    @call_logger
    async def bg_fetch_movie_data(self, movie: MovieImport):
        """
        Background task to fetch movie data from omdbapi and update the movie with the fetched data.
        :param movie:
        :return:
        """
        self.queue_service.publish_on_fetch_topic(
            message=movie.title, movie_import_id=str(movie.id), movie_title=movie.title
        )

    async def import_movie(self, movie_import_create: MovieImportCreate) -> MovieImport:
        """
        Throw an error if a movie or movie import with the given title already exists
        if not, create a movie import
        and then make a call to the worker to fetch the movie data from omdbapi

        :param movie_import_create: Movie info to import
        :return: Movie import
        """

        if await self.movie_repository.exists_movie_by_title(movie_import_create.title):
            raise MovieAlreadyExists()

        if await self.movie_import_repository.exists_movie_import_by_title(
            movie_import_create.title
        ):
            raise MovieAlreadySubmitted()

        movie_import = MovieImport(title=movie_import_create.title)
        await self.movie_import_repository.add_movie_import(movie_import)
        await self.bg_fetch_movie_data(movie_import)
        # self.background_tasks.add_task(self.bg_fetch_movie_data, movie=movie)
        return movie_import
