import json

from kafka import KafkaConsumer, TopicPartition

from src.eventscollector.config.config import settings


def start_consumer_services(
    *,
    boostrap_servers: str,
    partition: int,
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
    topic_partition = TopicPartition(settings.TOPIC_CONSUME_EVENTS, partition)
    topics = [topic_partition]
    consumer = KafkaConsumer(
        bootstrap_servers=boostrap_servers,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        **kwargs
    )
    consumer.assign(topics)
    return consumer
