from loguru import logger

from src.models.services import create_feed
from src.apps.collector.parsers import (
    parse_csv, parse_custom_json, parse_free_text,
    parse_misp, parse_stix
)


def choose_type(name: str):
    methods = {
        "json": parse_custom_json,
        "stix": parse_stix,
        "free_text": parse_free_text,
        "misp": parse_misp,
        "csv": parse_csv,
        "txt": parse_free_text
    }
    return methods[name]


def feed_creator(*, feed: dict, config: dict):
    try:
        format_handler = choose_type(feed.get("type", "json"))
        # получаем список методов для фида
        feed = create_feed(data_to_create_with=feed['feed'])
        format_handler(feed, None, config)
    except Exception as e:
        logger.exception(f"Error occured: {e}")
    finally:
        # Statistic.objects.create(data=feed)
        ...
