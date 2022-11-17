import json
from typing import List
from abc import ABC, abstractmethod

from loguru import logger

from src.config.config import settings
from src.apps.consumer.services import start_consumer_services


class AbstractConsumer(ABC):
    def __init__(
        self,
        partition: List[int],
    ) -> None:
        self.consumer = None
        self.val_desirializer = lambda x: json.loads(x.decode('utf-8'))
        self.val_encoder = lambda x: json.dumps(x).encode('utf-8')
        self.partition = partition

    def start_consume(self) -> None:
        if self.consumer is None:
            try:
                self.consumer = start_consumer_services(
                    boostrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
                    partition=self.partition,
                    group_id=settings.KAFKA_GROUP_ID,
                    auto_offset_reset="earliest"
                )
                logger.info(f"Consumer: {self.consumer}")
            except Exception as e:  # noqa
                logger.exception("Error in creating consumer")

    @abstractmethod
    def start_process(self):
        raise NotImplementedError

    def stop_consumer(self):
        self.consumer.stop()
