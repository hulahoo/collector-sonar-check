import json
import pathlib
from abc import ABC, abstractmethod
from configparser import ConfigParser

from kafka import KafkaConsumer

from events_collector.config.log_conf import logger
from events_collector.config.config import settings


class AbstractConsumer(ABC):
    def __init__(self) -> None:
        self.consumer = self.create_consumer()

    def __read_config(self) -> dict:
        config_dir = pathlib.Path(__file__).resolve(strict=True).parent.parent.parent
        path = sorted(pathlib.Path(config_dir).glob(f"{settings.CONFIG_DIRECTORY}{settings.CONFIG_FILE}"))[0]
        with open(path, "r") as config_file:
            config_parser = ConfigParser()
            config_parser.read_file(config_file)
            config = dict(config_parser["consumer"])
            config["bootstrap_servers"] = settings.KAFKA_BOOTSTRAP_SERVER
            config["group_id"] = settings.KAFKA_GROUP_ID
            config["value_deserializer"] = lambda x: json.loads(x.decode('utf-8'))
            return config

    def create_consumer(self) -> KafkaConsumer:
        try:
            consumer = KafkaConsumer(
                settings.TOPIC_CONSUME_EVENTS,
                **self.__read_config()
            )
            logger.info(f"Consumer: {consumer.__dict__}")
            return consumer
        except Exception as e:
            logger.error(f"Error in creating consumer: {e}")

    @abstractmethod
    def start_process(self):
        raise NotImplementedError

    def stop_consumer(self):
        self.consumer.stop()
