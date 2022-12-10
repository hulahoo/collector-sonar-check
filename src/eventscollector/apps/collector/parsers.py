from typing import Optional


from src.eventscollector.config.log_conf import logger
from src.eventscollector.models.models import Indicator
from src.eventscollector.apps.collector.selectors import indicator_selector, stat_matched_selector
from src.eventscollector.commons.enums import TYPE_LIST


# def create_detection(*, event: dict) -> Detections: # think about format and data to take from


def filter_event_format_type(*, event: dict) -> str:
    for key in event:
        if key in TYPE_LIST:
            return key


def create_matched_object(*, indicator_id: int):
    stat_matched_selector.create(indicator_id=indicator_id)


def json_event_matching(*, event: dict):
    event_type = filter_event_format_type(event=event)
    event_value = event.get(event_type, "").get(event_type, "")

    indicator: Optional[Indicator] = indicator_selector.get_by_type_and_value(
        value=event_value, type=event_type
    )
    if indicator:
        logger.info("Matched found. Create Detection")
        # detection = create_detection()
        create_matched_object(indicator_id=indicator.id)
