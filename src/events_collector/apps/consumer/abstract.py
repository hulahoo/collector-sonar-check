import json
from abc import ABC, abstractmethod

from kafka import KafkaConsumer

from events_collector.config.log_conf import logger
from events_collector.config.config import settings


class AbstractConsumer(ABC):
    def __init__(
        self
    ) -> None:
        self.consumer = self.create_consumer()

    def create_consumer(self) -> None:
        try:
            config = {
                "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVER,
                "group_id": settings.KAFKA_GROUP_ID,
                "value_deserializer": lambda x: json.loads(x.decode('utf-8')),
                "auto_offset_reset": "earliest",
                "api_version": (0, 10, 1),
            }
            consumer = KafkaConsumer(
                settings.TOPIC_CONSUME_EVENTS,
                **config
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
