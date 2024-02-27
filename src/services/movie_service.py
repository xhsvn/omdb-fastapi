from typing import Annotated

from fastapi import Depends
from loguru import logger

from src.core.exceptions import MovieNotFound
from src.models.movie import Movie
from src.models.user import User
from src.repositories.movie_repository import MovieRepository


class MovieService:
    def __init__(self, movie_repository: Annotated[MovieRepository, Depends()]):
        self.movie_repository = movie_repository

    async def list_movies(self, offset: int, limit: int) -> list[Movie]:
        """
        return list of movies
        :param offset: offset
        :param limit: number of movies to return
        :return: List of Movie objects
        """
        return await self.movie_repository.list_movies(offset, limit)

    async def delete_movie(self, user: User, movie_id: int) -> None:
        """
        Delete movie with given id if exists else raise exception
        :param movie_id: id of movie to delete
        :return: None
        """
        movie = await self.movie_repository.get_movie_or_none_by_id(movie_id)
        if not movie:
            raise MovieNotFound

        await self.movie_repository.delete_movie(movie)

        logger.info(f"Movie with id {movie_id} deleted by user {user.username}")

    async def get_movie(self, movie_title: str) -> Movie:
        """
        Get movie by title or raise exception if not found
        :param movie_title: title of movie to get
        :return: Movie object
        """
        movie = await self.movie_repository.get_movie_or_none_by_title(movie_title)

        if not movie:
            raise MovieNotFound

        return movie
