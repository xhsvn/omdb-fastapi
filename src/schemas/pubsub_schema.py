from base64 import b64decode
from typing import Any

from pydantic import Base64Str
from pydantic import BaseModel, Field


class MovieFetchGooglePubSubMessageAttributes(BaseModel):
    movie_title: str
    movie_import_id: int


class MovieFetchGooglePubSubMessage(BaseModel):
    data: Base64Str
    message_id: str = Field(str, alias="messageId")
    attributes: MovieFetchGooglePubSubMessageAttributes

    def decode(self) -> str:
        return b64decode(self.data).decode("utf8")

class MovieFetchGooglePubSubPushRequest(BaseModel):
    message: MovieFetchGooglePubSubMessage
