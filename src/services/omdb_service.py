from typing import Annotated
import aiohttp


from fastapi import Depends

from src.deps import SettingsDep


class OmdbService:
    def __init__(self, settings: SettingsDep):
        self.api_key = settings.omdb_api_key

    async def get_movie_by_title(self, title: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
            ) as response:
                return await response.json()

    async def get_movie_by_id(self, movie_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://www.omdbapi.com/?i={movie_id}&apikey={self.api_key}"
            ) as response:
                return await response.json()


OmdbServiceDep = Annotated[OmdbService, Depends()]
