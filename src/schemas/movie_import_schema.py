from pydantic import Field

from src.core.schema import BaseModel

class MovieImportCreate(BaseModel):
    title: str = Field(..., title="Title of the movie")

class MovieImport(MovieImportCreate):
    id: int = Field(..., title="Id of the movie import")
    status: str = Field(..., title="Status of the import")