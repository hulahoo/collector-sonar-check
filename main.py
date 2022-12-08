from loguru import logger
from dagster import job

from src.config import conf
from src.apps.collector.events_handler import events_hadler, consumer_dispatcher_op, consumer_collector

logger.remove()
logger.configure(**conf)


@job
def main() -> None:
    """
    Главная функция для запуска определенных сервисов в зависимости от аргумента при вызвове модуля
    """
    results = consumer_dispatcher_op().map(events_hadler)
    consumer_collector(results.collect())
