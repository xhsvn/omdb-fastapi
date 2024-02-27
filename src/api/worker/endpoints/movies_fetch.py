from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.services.movie_fetch_service import MovieFetchService
from src.schemas.pubsub_schema import MovieFetchGooglePubSubPushRequest

router = APIRouter(prefix="/movies", tags=["auth"])


@router.post("/fetch")
async def fetch(
    request: MovieFetchGooglePubSubPushRequest,
    fetch_service: Annotated[MovieFetchService, Depends()],
    ):
    """
    Fetch movie data from omdbapi and update the movie with the fetched data.
    :param request: message from google pubsub
    :param fetch_service:
    :return:

    """
    await fetch_service.fetch_movie_data(
        movie_import_id=request.message.attributes.movie_import_id,
        movie_title=request.message.attributes.movie_title
        )


@router.post("/fetch/dlq")
async def fetch_dlq(
    request: MovieFetchGooglePubSubPushRequest,
    fetch_service: Annotated[MovieFetchService, Depends()],
    ):
    """
    process dead letter queue
    :param request: message from google pubsub
    :param fetch_service:
    :return:

    """

    await fetch_service.process_dead_letter(
        movie_import_id=request.message.attributes.movie_import_id,
        movie_title=request.message.attributes.movie_title
        )