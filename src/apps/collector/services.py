from loguru import logger

from src.apps.collector.selectors import stat_checked_selector
from src.apps.collector.parsers import json_event_matching


def choose_type(name: str):
    methods = {
        "JSON": json_event_matching,
    }
    return methods[name]


def event_matching(*, event: dict, config: dict):
    stat_checked_selector.create()
    try:
        format_handler = choose_type(event.get("format_of_feed", "JSON"))
        # получаем список методов для фида
        format_handler(event=event)
    except Exception as e:
        logger.exception(f"Error occured: {e}")
