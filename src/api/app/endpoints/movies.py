from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_pagination import LimitOffsetParams, paginate

from src.core.pagination import LimitOffsetPage
from src.core.schema import ExceptionModel
from src.deps import CurrentUser
from src.schemas import movie_schema
from src.services.movie_service import MovieService

router = APIRouter(prefix="/movies", tags=["movie"])


@router.get(
    "",
    response_model=LimitOffsetPage[movie_schema.Movie],
    summary="List movies",
    description="List all movies with pagination.",
    response_description="List of movies",
)
async def list_movies(
    movies_service: Annotated[MovieService, Depends()],
    pagination: LimitOffsetParams = Depends(),
):
    """
    List all movies with default ording on title and pagination.

    :param movies_service: MovieService
    :param pagination: LimitOffsetParams
    :return: List of movies
    """

    return paginate(
        await movies_service.list_movies(pagination.offset, pagination.limit),
        pagination,
    )


@router.get(
    "/{movie_title}",
    response_model=movie_schema.Movie,
    summary="Get movie",
    description="Get the movie with the given title.",
    response_description="The movie",
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionModel}},
)
async def get_movie(
    movie_title: str,
    movies_service: Annotated[MovieService, Depends()],
):
    """
    Get the movie with the given title.
    :param movie_title: title of movie to get
    :return: Movie
    """
    return await movies_service.get_movie(movie_title)


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete movie",
    description="Delete the movie with the given id.",
    response_description="The movie was deleted",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
    },
)
async def delete_movie(
    movie_id: int,
    user: CurrentUser,
    movies_service: Annotated[MovieService, Depends()],
):
    """
    Delete the movie with the given id.

    :param movie_id: id of movie to delete
    :return: None
    """
    return await movies_service.delete_movie(user, movie_id)
