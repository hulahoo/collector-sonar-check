from src.models.models import Feed
from src.models.base import SyncPostgresDriver


class FeedProvider:
    def create(self, *, data_to_create: dict) -> Feed:
        with SyncPostgresDriver().session() as db:
            feed = Feed(**data_to_create)

            db.add(feed)
            db.flush()
            db.commit()
            db.refresh(feed)
            return feed

    def delete(self, filter_fields: dict):