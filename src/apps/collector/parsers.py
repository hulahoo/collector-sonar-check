import csv
import json
import sys
from uuid import uuid4

import requests
from loguru import logger
from bs4 import BeautifulSoup
from flatdict import FlatterDict
from stix2elevator import elevate
from stix2elevator.options import initialize_options

from src.models.models import Feed, Indicator

initialize_options(options={"spec_version": "2.1"})


def get_url(url) -> str:
    """
    Опрашивает переданный url и возвращает всю страницу в строковом формате.
    """
    try:
        received_data = requests.get(url).text
    except Exception as e:
        logger.exception(f"Возникла ошибка при получении данных: {e}")
    return received_data


def get_or_elevate(feed) -> dict:
    """
    Узнает версию stix и переводит во вторую версию.
    """
    text = get_url(feed.link)
    try:
        return json.loads(text)
    except Exception:
        logger.error("Error loading json. Return text")
        return elevate(text)


def parse_misp_event(urls_for_parsing, feed):
    """
    Парсит MISP евенты со страницы с url'ами.
    """
    indicators = []
    for url in urls_for_parsing:
        indicators.append(convert_misp_to_indicator(json.loads(get_url(url)), feed))
    return indicators


def convert_misp_to_indicator(feed, raw_indicators=None):
    """
    Из MISP события и входящих в него параметров и объектов -
    импортирует список индиктаторов
    """
    indicators = []
    attributes = raw_indicators.get("Event").get("Attribute")
    attribute_in_object = []
    if raw_indicators.get("Event").get("Object"):
        for object in raw_indicators.get("Event").get("Object"):
            attribute_in_object = object.get("Attribute")

    attributes_list = [*attributes, *attribute_in_object]
    try:
        for attribute in attributes_list:
            indicator, created = Indicator.objects.get_or_create(value=attribute.get('value'), defaults={
                "uuid": attribute.get("uuid"),
                "ioc_context_type": attribute.get("type"),
                "supplier_name": feed.vendor,
                "supplier_confidence": feed.confidence,
                "weight": feed.confidence
            })

            try:
                indicator.feeds.add(feed)
                indicators.append(indicator)
            except Exception as e:
                logger.exception(f"Error adding feed to indicator: {e}")
    except TypeError:
        pass
        return indicators


def convert_txt_to_indicator(feed, raw_indicators=None):
    if feed.format_of_feed == "TXT":
        complete_indicators = []
        feed.save()
        for raw_indicator in raw_indicators:
            indicator, created = Indicator.objects.get_or_create(value=raw_indicator,
                                                                 defaults={
                                                                     "uuid": uuid4(),
                                                                     "supplier_name": feed.vendor,
                                                                     "type": feed.type_of_feed,
                                                                     "weight": feed.confidence,
                                                                     "supplier_confidence": feed.confidence
                                                                 })
            indicator.feeds.add(feed)
            complete_indicators.append(indicator)
        return complete_indicators


def parse_custom_json(feed, raw_indicators=None, config: dict = {}):
    try:
        """
        Парсит переданный кастомный json с выбранными из фида полями и отдает список индикаторов.
        """
        limit = config.get('limit', None)

        feed_control(feed, config)
        raw_json = json.loads(get_url(feed.link))
        indicators = []

        if limit:
            lst = list(FlatterDict(raw_json).items())[:limit]
        else:
            lst = list(FlatterDict(raw_json).items())

        for key, value in lst:
            indicator, created = Indicator.objects.get_or_create(value=value, defaults={
                "uuid": uuid4(),
                "supplier_name": feed.vendor,
                "supplier_confidence": feed.confidence,
                "weight": feed.confidence
            })
            indicator.feeds.add(feed)
            indicators.append(indicator)
        return indicators
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


def parse_stix(feed, raw_indicators=None, config: dict = {}):
    """
    Парсит переданный json в формате STIX и отдает список индикаторов.
    """

    limit = config.get('limit', None)

    bundle = get_or_elevate(feed)
    objects = bundle.get("objects")
    raw_indicators = []

    if limit:
        objects = list(objects)[:limit]

    for obj in objects:
        if obj.get("type") == "indicator":
            raw_indicators.append(obj)

    indicators = []
    feed_control(feed, config)
    for raw_indicator in raw_indicators:
        indicator, created = Indicator.objects.get_or_create(value=raw_indicator.get("name"),
                                                             defaults={
                                                                 "uuid": raw_indicator.get('id', uuid4()),
                                                                 "first_detected_date": raw_indicator.get("created"),
                                                                 "supplier_name": feed.vendor,
                                                                 "supplier_confidence": feed.confidence,
                                                                 "weight": feed.confidence
                                                             }
                                                             )

        indicator.feeds.add(feed)
        pattern = raw_indicator.get("pattern")
        if "ip" in pattern:
            indicator.ioc_context_ip = pattern
            indicator.type = "IP"
        elif "filesize" in pattern:
            indicator.ioc_context_file_size = pattern
        indicator.save()
        indicators.append(indicator)
    return indicators


def parse_free_text(feed, raw_indicators=None, config: dict = {}):
    """
    Парсит переданный текст и отдает список индикаторов.
    """
    limit = config.get('limit', None)

    raw_indicators = raw_indicators.split("\n")
    try:
        raw_indicators.remove("")
    except Exception as e:
        logger.exception(f"Error is: {e}")
    raw_indicators = [
        ioc.replace("\r", "") for ioc in raw_indicators if not ioc.startswith("#")
    ]

    if limit:
        raw_indicators = raw_indicators[:limit]

    result = convert_txt_to_indicator(feed, raw_indicators)
    return result


def parse_misp(feed, raw_indicators=None, config: dict = {}) -> list:
    """
    Парсит переданный текст со списком url'ок и отдает список индикаторов.
    Применяется когда по ссылке находится список json файлов.
    """
    limit = config.get('limit', None)

    parsed_page = BeautifulSoup(get_url(feed.link), "html.parser")
    urls_for_parsing = []

    links = list(parsed_page.find_all("a"))
    if limit:
        links = links[:limit]

    for link in links:
        if ".json" in link.text:
            urls_for_parsing.append(f"{feed.link}{link.get('href')}")
    misp_events = parse_misp_event(urls_for_parsing, feed)
    return misp_events


def parse_csv(feed, raw_indicators=None, config: dict = {}) -> list:
    """
    Парсит переданный текст с параметрами для csv и отдает список индикаторов.
    """
    limit = config.get('limit', 0)

    raw_indicators = [
        row for row in raw_indicators.split("\n") if not row.startswith("#")
    ]
    indicators = []
    feed_control(feed, config)

    counter = 0

    for row in csv.DictReader(
            raw_indicators,
            delimiter=config.get('delimiter', ","),
            fieldnames=config.get('fieldnames', ""),
            dialect=config.get('dialect', "excel"),
    ):
        indicator, created = Indicator.objects.get_or_create(value=row.get(feed.custom_field), defaults={
            "uuid": uuid4(),
            "supplier_name": feed.vendor,
            "supplier_confidence": feed.confidence,
            "weight": feed.confidence
        })
        indicator.feeds.add(feed)

        counter += 1
        if counter >= limit > 0:
            break

    return indicators


def feed_control(feed, config):
    fields = ['type_of_feed', 'format_of_feed', 'auth_type', 'polling_frequency', 'auth_login', 'auth_password',
              'ayth_querystring', 'separator', 'custom_field', 'sertificate', 'vendor', 'name', 'link', 'confidence',
              'records_quantity', 'update_status', 'ts', 'source_id']

    if config.get('is_instead_full', False):

        feed.save()
    else:
        feed_exist = Feed.objects.filter(name=feed.name).first()
        if feed_exist:
            for field in fields:
                setattr(feed_exist, field, getattr(feed, field))
            feed = feed_exist
        else:
            feed.save()
    return feed
