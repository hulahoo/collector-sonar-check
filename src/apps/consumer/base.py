import sys
import json
import traceback
from typing import List

from dagster import get_dagster_logger

from src.apps.collector.services import event_matching
from src.apps.consumer.abstract import AbstractConsumer


class BaseConsumer(AbstractConsumer):

    def __init__(self, context: dict, partition: List[int]):
        self.context = context
        self.partition = partition
        super().__init__(self)

    def start_process(self):
        self.start_consumer()
        self.process_handler_service()

    def process_handler_service(self):
        logger = get_dagster_logger()
        logger.info("Start process services...")  # noqa

        for event in tuple(self.consumer.poll(timeout_ms=5000).items()):
            message = json.loads(event.value)
            try:
                context_config = self.context.op_config["config"]
                config = dict() if context_config is None else context_config

                logger.info(f"Incoming config is: {config}")
                logger.info(f'Incoming events is: {event}')

                event_matching(event=event, config=config)

            except Exception as e:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                logger.error(f"FAILED proccess message from topic: {message.topic}")
                logger.error(f"ERROR traceback: {e}")
                continue
