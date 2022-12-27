import json
from abc import ABC, abstractmethod
from typing import List, Union

from kafka.producer import KafkaProducer

from events_collector.config.log_conf import logger
from events_collector.config.config import settings


class AbstractProducer(ABC):
    """
    Абстрактный класс для базового описания продюсера
    """

    @abstractmethod
    def send_message(self):
        raise NotImplementedError

    @abstractmethod
    def start_process(self):
        raise NotImplementedError


class BaseProducer(AbstractProducer):

    __slots__ = ("message_to_send", "topic", "producer")

    def __init__(self, topic: str, message_to_send: dict):
        self.producer = self._start_producer()
        self.message_to_send = message_to_send
        self.topic = topic

    def _send_data(
        self,
        *,
        data: dict,
        topic: Union[List, str],
        producer: KafkaProducer,
    ) -> None:
        """
        Сервис для отправки сгенерированного сообщения в брокер

        :param data: данные для отправки(словарь)
        :type data: `class: Dict[str, Any]`
        :param topic: топик куда данные будут отправлены
        :type topic: `class: Union[List, str]`
        """
        logger.info(f"Sending data to: {topic}")
        producer.send(topic=topic, value=data)
        producer.flush()
        logger.info(f"Data send to: '{topic}' topic")

    def _start_producer(self) -> KafkaProducer:
        """
        Создание продюсера

        :param boostrap_servers: адрес хоста для подключения к Kafka серверу
        :type boostrap_servers: str
        :return: обьект от AIOKafkaProducer
        :rtype: `class: aiokafka.AIOKafkaProducer`
        """
        try:
            logger.info(f"{settings.KAFKA_BOOTSTRAP_SERVER}")
            producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                api_version=(0, 10, 1),
                max_request_size=3718690
            )
        except Exception as e:
            logger.error(f"Error occured when created producer. Error is: {e}")
            return
        else:
            return producer

    def _stop_producer(self):
        self.producer.close()
