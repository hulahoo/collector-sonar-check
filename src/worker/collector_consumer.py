
from loguru import logger

from src.worker.services import choose_type
from src.intelhandler.models import Statistic
from src.models.services import create_feed


def feed_creator(*, feed: dict, config: dict):
    try:
        format_handler = choose_type(feed.get("type", "json"))
        # получаем список методов для фида
        feed = create_feed(data_to_create_with=feed['feed'])
        format_handler(feed, None, config)
    except Exception as e:
        logger.exception(f"Error occured: {e}")
    finally:
        Statistic.objects.create(data=feed)
