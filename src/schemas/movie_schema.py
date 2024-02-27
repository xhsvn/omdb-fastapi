from pydantic import Field, ConfigDict

from pydantic.alias_generators import to_pascal
from src.core.schema import BaseModel

class MovieBase(BaseModel):
    title: str
    year: int
    rated: str
    released: str
    runtime: str
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    language: str
    country: str
    awards: str
    poster: str
    metascore: str
    imdb_rating: str
    imdb_votes: str
    imdb_id: str
    dvd: str
    box_office: str
    production: str
    website: str

class Movie(MovieBase):
    id: int

class MovieOmdb(MovieBase):
    dvd: str = Field(alias="DVD")
    imdb_id: str = Field(alias="imdbID")
    imdb_rating: str = Field(alias="imdbRating")
    imdb_votes: str = Field(alias="imdbVotes")
    
    model_config = ConfigDict(
        alias_generator=to_pascal
    )