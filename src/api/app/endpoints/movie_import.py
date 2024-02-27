
from typing import Annotated

from fastapi import APIRouter, Depends, status


from src.core.schema import ExceptionModel
from src.schemas import movie_import_schema
from src.services.movie_import_service import MovieImportService

router = APIRouter(prefix="/imports", tags=["import"])



@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=movie_import_schema.MovieImport,
    summary="Import a new movie using the title.",
    description="Import the movie with the given title from omdbapi if it does not exist.",
    response_description="The import information of the movie",
    responses={status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel}},
)
async def import_movie(
    movie_create: movie_import_schema.MovieImportCreate,
    movies_import_service: Annotated[MovieImportService, Depends()],
    ):
    """
    Check that if the a movie with the given title does not exist and create it.

    :param movie_create: Movie to import
    :return: Created movie import information
    """
    return await movies_import_service.import_movie(movie_create)