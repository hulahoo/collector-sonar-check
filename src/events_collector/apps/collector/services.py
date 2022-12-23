import json
from typing import Dict, Optional, Callable, Union

from events_collector.config.log_conf import logger
from events_collector.commons.enums import TYPE_LIST, TypesEnum
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

        indicator: Optional[Indicator] = indicator_selector.get_by_type_and_value(value=event_type)
        logger.info(f"Indicator found {indicator}")
        if indicator:
            self.create_matched_object(indicator_id=indicator.id)
            logger.info("Matched found. Increase matched count")

            detection = self.create_detection(
                event=event,
                event_key=event_key,
                indicator_id=indicator.id,
                indicator_weight=indicator.weight,
                indicator_context=indicator.context,
            )
            logger.info(f"Created detection: {detection}")
        else:
            logger.info("No matched found.")

    def create_detection(
        self,
        *,
        event: dict,
        event_key: str,
        indicator_id: int,
        indicator_weight: int,
        indicator_context: dict,
    ) -> Detections:
        detection_event = self.create_detection_format(
            event=event,
            event_key=event_key,
            indicator_weight=indicator_weight,
            indicator_context=indicator_context,
        )
        source_event_json = json.dumps(event, ensure_ascii=False, default=str)
        logger.info(f"Parsed source event: {source_event_json}")

        detection_event_json = json.dumps(detection_event, ensure_ascii=False, default=str)
        logger.info(f"Parsed detection event: {detection_event_json}")
        detection = detections_selector.create(
            source_event=source_event_json,
            indicator_id=indicator_id,
            detection_event=detection_event_json
        )
        return detection

    def create_detection_format(
        self,
        *,
        event: dict,
        event_key: str,
        indicator_weight: int,
        indicator_context: dict,
    ) -> Dict[str, Union[str, dict]]:
        detection = dict()
        logger.info(f"Received event: {event}. Creating detection event")
        filtered_pairs = self.get_event_values(event=event)
        logger.info(f"filtered: {filtered_pairs}")
        detection["src"] = filtered_pairs.get("src")
        detection["src_port"] = filtered_pairs.get("srcPort")
        detection["dst"] = filtered_pairs.get("dst")
        detection["dstPort"] = filtered_pairs.get("dstPort")
        detection["username"] = filtered_pairs.get("username")
        detection["event_name"] = filtered_pairs.get("eventName")
        detection["log_source_identifier"] = filtered_pairs.get("logSourceIdentifier")
        detection["log_source_type"] = filtered_pairs.get("logSourceType")
        detection["src_net_name"] = filtered_pairs.get("srcNetName")
        detection["context"] = dict()
        detection["context"]["ioc_weight"] = indicator_weight
        detection["context"]["ioc_context"] = indicator_context
        detection["context"]["source_id"] = filtered_pairs.get("Source_Id", "default")
        detection["event_code"] = filtered_pairs.get("event_code")

        if event_key == TypesEnum.URL.value:
            detection["domain"] = filtered_pairs.get("URL_domain")
            detection["url_domain"] = filtered_pairs.get("URL_domain")
            detection["url"] = filtered_pairs.get("URL")
        if event_key == TypesEnum.IP.value:
            detection["ip"] = filtered_pairs.get("IP")
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
        for _, value in event.items():
            try:
                filtered_values.update(value)
            except Exception as e:
                logger.info(f"Filtering finished: {e}")
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
