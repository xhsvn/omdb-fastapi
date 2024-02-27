from typing import Annotated

from fastapi import Depends
from google.cloud import pubsub_v1

from src.deps import SettingsDep


class QueueService:
    def __init__(self, settings: SettingsDep) -> None:
        self.project = settings.google_project_id
        self.topic = settings.pubsub_movies_fetch_topic
        self.publisher_client = pubsub_v1.PublisherClient()
        self.fetch_topic_path = self.publisher_client.topic_path(
            project=self.project,
            topic=self.topic,
        )

    def publish_on_fetch_topic(self, *, message: str = "", **attrs) -> str:
        """
        Publish a single message to a Pub/Sub topic for fetching.
        Return the message ID or raise an exception and fail the message.
        """

        future = self.publisher_client.publish(
            topic=self.fetch_topic_path,
            data=message.encode(),
            **attrs,
        )
        return future.result()


QueueServiceDep = Annotated[QueueService, Depends()]
