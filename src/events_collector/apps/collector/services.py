from typing import Dict, Optional, Callable, Union

from events_collector.config.log_conf import logger
from events_collector.commons.enums import TYPE_LIST
from events_collector.models.models import Detections, Indicator
from events_collector.apps.collector.selectors import (
    stat_checked_selector, detections_selector, indicator_selector, stat_matched_selector
)


class FormatsHandler:

    def json_event_matching(self, *, event: dict):
        event_key: str = self.filter_event_format_type(event=event)
        logger.info(f"Event key; {event_key}")

        event_parent_key: dict = event.get(event_key, None)
        logger.info(f"Event parent key; {event_parent_key}")

        event_type: str = event_parent_key.get(event_key, None)
        logger.info(f"Event type: {event_type}")

        indicator: Optional[Indicator] = indicator_selector.get_by_type_and_value(
            type=event_key,
            value=event_type,
        )
        logger.info(f"Indicator found {indicator}")
        if indicator:
            logger.info("Matched found. Create Detection")

            detection = self.create_detection(
                event=event,
                indicator_id=indicator.id,
                indicator_weight=indicator.weight,
                indicator_context=indicator.context,
            )
            logger.info(f"Created detection: {detection}")
            self.create_matched_object(indicator_id=indicator.id)
        else:
            logger.info("No matched found.")

    def create_detection(
        self,
        *,
        event: dict,
        indicator_id: int,
        indicator_weight: int,
        indicator_context: dict,
    ) -> Detections:
        detection_event = self.create_detection_format(
            event=event,
            indicator_weight=indicator_weight,
            indicator_context=indicator_context,
        )
        detection = detections_selector.create(
            source_event=event,
            indicator_id=indicator_id,
            detection_event=detection_event
        )
        return detection

    def create_detection_format(
        self,
        *,
        event: dict,
        indicator_weight: int,
        indicator_context: dict,
    ) -> Dict[str, Union[str, dict]]:
        detection = dict()
        logger.info(f"Received event: {event}. Creating detection event")
        filtered_pairs = self.get_event_values(event=event)
        detection["src"] = filtered_pairs.get("Source_IP")
        detection["src_port"] = filtered_pairs.get("Source_port")
        detection["dst"] = filtered_pairs.get("Destination")
        detection["dstPort"] = filtered_pairs.get("Destination_port")
        detection["username"] = filtered_pairs.get("User_name")
        detection["url"] = filtered_pairs.get("URL")
        detection["url_domain"] = filtered_pairs.get("URL_domain")
        detection["event_name"] = filtered_pairs.get("Event_name")
        detection["log_source_identifier"] = filtered_pairs.get("Log_source_identifier")
        detection["log_source_type"] = filtered_pairs.get("Log_source_type")
        detection["src_asset_name"] = filtered_pairs.get("Log_source")
        detection["src_net_name"] = filtered_pairs.get("Source_Net_Name")
        detection["domain"] = filtered_pairs.get("URL_domain")
        detection["context"] = dict()
        detection["context"]["ioc_weight"] = indicator_weight
        detection["context"]["ioc_context"] = indicator_context
        detection["context"]["source_id"] = filtered_pairs.get("Source_Id", "default")
        detection["event_code"] = filtered_pairs.get("Event_code")
        return detection

    @staticmethod
    def create_matched_object(*, indicator_id: int):
        stat_matched_selector.create(indicator_id=indicator_id)

    @staticmethod
    def filter_event_format_type(*, event: dict) -> str:
        logger.info(f"Event to filter: {event}")
        keys = event.keys()
        for key in keys:
            if key in TYPE_LIST:
                logger.info(f"Key found: {key}")
                return key

    @staticmethod
    def get_event_values(*, event: dict) -> Dict[str, str]:
        filtered_values = dict()
        for parent_key, value in event.get("feed"):
            filtered_values[parent_key] = value[parent_key]
        return filtered_values


class EventsHandler:
    def __init__(self, event: dict):
        self.event = event
        self.format_handler = FormatsHandler()

    def choose_format(self, *, event_type: str) -> Optional[Callable]:
        formats = {
            "JSON": self.format_handler.json_event_matching,
        }
        return formats.get(event_type)

    def check_event_matching(self):
        stat_checked_selector.create()
        try:
            format_handler = self.choose_format(
                event_type=self.event.get("format_of_feed", "JSON")
            )
            if format_handler is None:
                logger.error("No appropriate format found")
                return
            else:
                logger.info(f"Found handler: {format_handler.__name__}")
                format_handler(event=self.event)
        except Exception as e:
            logger.error(f"Error occured: {e}")

    def __call__(self):
        self.event_matching()
