from src.models.models import Feed
from src.models.provider import FeedProvider


def create_feed(*, data_to_create_with: dict) -> Feed:
    return FeedProvider().create(data_to_create=data_to_create_with)
