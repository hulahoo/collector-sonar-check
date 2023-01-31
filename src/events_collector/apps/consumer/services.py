import json

from kafka import KafkaConsumer

from events_collector.config.config import settings


def start_consumer_services(
    *,
    boostrap_servers: str,
    **kwargs
) -> KafkaConsumer:
    """
    Сервис для запуска KafkaConsumer

    :param topic: Список или строка топиков в которые нужно отправить данные
    :type topic: `class: Union[str, List[str]]`
    :param boostrap_servers: адрес хоста для подключения к Kafka серверу
    :type boostrap_servers: str
    :return: обьект от AIOKafkaConsumer
    :rtype: `class: aiokafka.AIOKafkaConsumer`
    """
    consumer = KafkaConsumer(
        settings.TOPIC_CONSUME_EVENTS,
        bootstrap_servers=boostrap_servers,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        **kwargs
    )
    return consumer
