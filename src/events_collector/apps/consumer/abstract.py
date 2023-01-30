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
        self.val_desirializer = lambda x: json.loads(x.decode('utf-8'))
        self.val_encoder = lambda x: json.dumps(x).encode('utf-8')

    def create_consumer(self) -> None:
        try:
            config = {
                "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVER,
                "group_id": settings.KAFKA_GROUP_ID,
                "value_deserializer": self.val_desirializer,
                "auto_offset_reset": "earliest",
                "api_version": (0, 10, 1),
            }
            consumer = KafkaConsumer(
                settings.TOPIC_CONSUME_EVENTS,
                **config
            )
            logger.info(f"Consumer: {self.consumer}")
            topics = self.consumer.topics()
            logger.info(f"Registered topics: {topics}")
            return consumer
        except Exception as e:
            logger.error(f"Error in creating consumer: {e}")

    @abstractmethod
    def start_process(self):
        raise NotImplementedError

    def stop_consumer(self):
        self.consumer.stop()
