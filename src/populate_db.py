from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.services.omdb_service import OmdbService
from src.settings import get_settings
from src.models.movie import Movie
from src.repositories.movie_repository import MovieRepository
from src.schemas.movie_schema import MovieOmdb

from loguru import logger


movie_ids = [
    "tt0111161",
    "tt0068646",
    "tt0071562",
    "tt0110912",
    "tt0060196",
    "tt0468569",
    "tt0050083",
    "tt0108052",
    "tt0167260",
    "tt0137523",
    "tt0080684",
    "tt0120737",
    "tt0073486",
    "tt1375666",
    "tt0099685",
    "tt0076759",
    "tt0047478",
    "tt0109830",
    "tt0133093",
    "tt0167261",
    "tt0317248",
    "tt0114369",
    "tt0102926",
    "tt0064116",
    "tt0034583",
    "tt0114814",
    "tt0082971",
    "tt0047396",
    "tt0038650",
    "tt0054215",
    "tt0110413",
    "tt0043014",
    "tt0120586",
    "tt0078788",
    "tt0103064",
    "tt0120815",
    "tt0209144",
    "tt0021749",
    "tt0057012",
    "tt0078748",
    "tt0027977",
    "tt0245429",
    "tt0053125",
    "tt0088763",
    "tt0118799",
    "tt0081505",
    "tt0253474",
    "tt0033467",
    "tt0407887",
    "tt0022100",
    "tt0050825",
    "tt0052357",
    "tt1853728",
    "tt0036775",
    "tt1345836",
    "tt0090605",
    "tt0075314",
    "tt0169547",
    "tt0120689",
    "tt0172495",
    "tt1675434",
    "tt0910970",
    "tt0405094",
    "tt0435761",
    "tt0032553",
    "tt0482571",
    "tt0066921",
    "tt0056172",
    "tt0211915",
    "tt0056592",
    "tt0105236",
    "tt0082096",
    "tt0110357",
    "tt0095765",
    "tt0086190",
]


async def populate():
    logger.info("Populating the database with movies")

    settings = get_settings()

    engine = create_async_engine(settings.database_url, echo=settings.postgres_echo)

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    session = session_factory()

    movie_repository = MovieRepository(session)

    async with session.begin():
        if await movie_repository.is_populated():
            logger.info("Database already populated")
            return
    omdb_service = OmdbService(settings)
    movies = []

    for movie_id in movie_ids:
        res = await omdb_service.get_movie_by_id(movie_id)
        movie = Movie(**MovieOmdb(**res).model_dump())
        movies.append(movie)

    async with session.begin():
        session.add_all(movies)

    await session.close()

    logger.info("Database populated")


if __name__ == "__main__":
    import asyncio

    asyncio.run(populate())
