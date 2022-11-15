import sys
import json
import traceback

from dagster import get_dagster_logger

from src.worker.collector_consumer import feed_creator
from src.apps.consumer.abstract import AbstractConsumer


class BaseConsumer(AbstractConsumer):

    def __init__(self, context: dict):
        self.context = context
        super().__init__(self)

    def start_process(self):
        self.start_consume()
        self.process_handler_service()

    def process_handler_service(self):
        logger.info("Start process services...")  # noqa

        for event in tuple(self.consumer.poll(timeout_ms=5000).items()):
            message = json.loads(event.value)
            try:
                logger = get_dagster_logger()
                context_config = self.context.op_config["config"]
                config = dict() if context_config is None else context_config
                logger.info(f"Incoming config is: {config}")
                logger.info(f'Incoming events is: {event}')
                feed_creator(feed=event, config=config)
            except Exception as e:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                logger.error(f"FAILED proccess message from topic: {message.topic}")
                logger.error(f"ERROR traceback: {e}")
                continue
