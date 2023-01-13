from typing import Union, List

from events_collector.config.log_conf import logger
from events_collector.apps.producer.abstract import BaseProducer


class MessageProducer(BaseProducer):

    def send_message(self, *, message_to_send: str, topic: Union[List, str]):
        logger.info("Sending message...")
        self._send_data(data=message_to_send, topic=topic, producer=self.producer)

    def start_process(self):
        self.send_message(message_to_send=self.message_to_send, topic=self.topic)


def producer_entrypoint(*, message_to_send: str, topic: str):
    producer = MessageProducer(message_to_send=message_to_send, topic=topic)
    logger.info("Producer created...")
    producer.start_process()
