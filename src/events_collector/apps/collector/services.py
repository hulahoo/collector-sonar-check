from typing import Dict, Optional

from events_collector.config.log_conf import logger
from events_collector.commons.enums import TYPE_LIST
from events_collector.models.models import Detections, Indicator
from events_collector.apps.collector.selectors import (
    stat_checked_selector, detections_selector, indicator_selector, stat_matched_selector
)


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
    event_type: str = event_parent_key.get(event_parent_key, {})

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


def get_event_values(*, event: dict) -> Dict[str, str]:
    filtered_values = dict()
    for parent_key, value in event.get("feed"):
        filtered_values[parent_key] = value[parent_key]
    return filtered_values


def create_detection_format(*, event: dict, indicator_context: dict, indicator_weight: int) -> Detections:
    logger.info(f"Received event: {event}. Creating detection event")
    filtered_pairs = get_event_values(event=event)
    source_ip = filtered_pairs.get("Source_IP")
    source_port = filtered_pairs.get("Source_port")
    dst = filtered_pairs.get("Destination")
    dest_port = filtered_pairs.get("Destination_port")
    username = filtered_pairs.get("User_name")
    url = filtered_pairs.get("URL")
    url_domain = filtered_pairs.get("URL_domain")
    event_name = filtered_pairs.get("Event_name")
    log_source_type = filtered_pairs.get("Log_source_type")
    log_source_identifier = filtered_pairs.get("Log_source_identifier")
    asset_name = filtered_pairs.get("Log_source")
    net_name = filtered_pairs.get("Source_Net_Name")
    source_id = filtered_pairs.get("Source_Id", "default")
    event_code = filtered_pairs.get("Event_code")
    detection_event: str = f"<IP-адрес> <ПО>|KL_Malicious_URL| src:{source_ip}srcPort:{source_port} dst:{dst} dstPort:{dest_port} usrName:{username} URL: {url} URL_Domain: {url_domain} eventName: {event_name} logSourceIdentifier:{log_source_identifier} logSourceType:{log_source_type} srcAssetName: {asset_name} srcNetName:{net_name} Domain:{url_domain} {indicator_weight} {indicator_context} {source_id} %Source_IP feed=KL_Malicious_URL event_code:{event_code}" # noqa
    return detection_event


def create_detection(*, indicator_id: int, event: dict, indicator_context: dict, indicator_weight: int) -> Detections:
    detection_event = create_detection_format(
        event=event, indicator_context=indicator_context, indicator_weight=indicator_weight
    )
    detection = detections_selector.create(
        indicator_id=indicator_id, source_event=event, detection_event=detection_event
    )
    return detection
