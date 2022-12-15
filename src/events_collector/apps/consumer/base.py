import sys
import json
import traceback

from events_collector.apps.collector.services import event_matching
from events_collector.config.log_conf import logger
from events_collector.apps.consumer.abstract import AbstractConsumer


class BaseConsumer(AbstractConsumer):

    def start_process(self):
        self.start_consumer()
        self.process_handler_service()

    def process_handler_service(self):
        logger.info("Start process services...")  # noqa

        for event in self.consumer.poll(timeout_ms=5000):
            message = json.loads(event.value)
            try:
                context_config = self.context.op_config["config"]
                config = dict() if context_config is None else context_config

                logger.info(f"Incoming config is: {config}")
                logger.info(f'Incoming events fromm is: {event.topic}')

                event_matching(event=event)

            except Exception as e:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                logger.error(f"FAILED proccess message from topic: {message.topic}")
                logger.error(f"ERROR traceback: {e}")
                continue
