from typing import Optional

from events_collector.config.log_conf import logger
from events_collector.models.models import Indicator
from events_collector.commons.enums import TYPE_LIST
from events_collector.apps.collector.services import create_detection
from events_collector.apps.collector.selectors import indicator_selector, stat_matched_selector, stat_checked_selector


def filter_event_format_type(*, event: dict) -> str:
    for key in event:
        if key in TYPE_LIST:
            return key


def create_matched_object(*, indicator_id: int):
    stat_matched_selector.create(indicator_id=indicator_id)


def event_matching(*, event: dict):
    stat_checked_selector.create()
    try:
        format_handler = choose_type(event.get("format_of_feed", "JSON"))
        format_handler(event=event)
    except Exception as e:
        logger.error(f"Error occured: {e}")


def choose_type(name: str):
    methods = {
        "JSON": json_event_matching,
    }
    return methods[name]


def json_event_matching(*, event: dict):
    event_key: str = filter_event_format_type(event=event)
    event_parent_key: dict = event.get(event_key, {})
    event_type: str = event_parent_key.get(event_type, {})

    indicator: Optional[Indicator] = indicator_selector.get_by_type_and_value(
        value=event_type, type=event_key
    )
    if indicator:
        logger.info("Matched found. Create Detection")
        detection = create_detection(
            indicator_context=indicator.context, indicator_id=indicator.id,
            event=event, indicator_weight=indicator.weight
        )
        logger.info(f"Created detection: {detection}")
        create_matched_object(indicator_id=indicator.id)
