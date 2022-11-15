
from loguru import logger
from django.utils import timezone

from src.models.indicator import Indicator
from src.worker.services import choose_type
from src.intelhandler.models import Statistic
from src.models.feed import Feed


def exist_indicator(indicator, data: dict, config):
    logger.info(f"Incoming indicator: {indicator}")
    indicator: Indicator
    indicator.detected += 1
    indicator.last_detected_date = timezone.now()

    indicator.save()
    data['config'] = config

    Statistic.objects.create(data=data)


def feed_creator(*, feed: dict, config: dict):
    try:
        format_handler = choose_type(feed.get("type", "json"))
        # получаем список методов для фида
        feed = Feed.create_feed(feed['feed'])
        feed.save()
        format_handler(feed, None, config)
    except Exception as e:
        logger.exception(f"Error occured: {e}")
    finally:
        Statistic.objects.create(data=feed)
