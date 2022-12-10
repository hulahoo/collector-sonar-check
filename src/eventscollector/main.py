from dagster import job

from src.eventscollector.config.log_conf import logger
from src.eventscollector.apps.collector.events_handler import events_hadler, consumer_dispatcher_op, consumer_collector


@job
def main() -> None:
    """
    Главная функция для запуска определенных сервисов в зависимости от аргумента при вызвове модуля
    """
    logger.info("Start consumer...")
    results = consumer_dispatcher_op().map(events_hadler)
    consumer_collector(results.collect())
