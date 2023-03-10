import sys
import traceback

from events_collector.config.log_conf import logger
from events_collector.apps.worker.services import EventsHandler
from events_collector.apps.consumer.abstract import AbstractConsumer


class BaseConsumer(AbstractConsumer):

    def start_process(self):
        self.process_handler_service()

    def process_handler_service(self):
        logger.info("Start process services...")  # noqa

        for message in self.consumer:
            event: dict = message.value
            try:
                logger.info(f'Incoming events fromm is: {message.topic}')

                handler = EventsHandler(
                    event=event.get("feed"),
                    source_message=event.pop("source_message")
                )
                handler.check_event_matching()

            except Exception as e:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                logger.error(f"FAILED proccess message from topic: {message.topic}")
                logger.error(f"ERROR traceback: {e}")
                continue
