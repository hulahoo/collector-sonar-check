from kafka import KafkaConsumer

from events_collector.config.config import settings


def start_consumer_services(**kwargs) -> KafkaConsumer:
    """
    Сервис для запуска KafkaConsumer
    """
    consumer = KafkaConsumer(
        settings.TOPIC_CONSUME_EVENTS,
        **kwargs
    )
    return consumer
