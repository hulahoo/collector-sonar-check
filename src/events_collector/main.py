import threading

from events_collector.config.log_conf import logger
from events_collector.models.migrations import apply_migrations
from events_collector.web.routers.api import execute as flask_app
from events_collector.apps.collector.events_handler import events_hadler


def main() -> None:
    """
    Главная функция для запуска определенных сервисов в зависимости от аргумента при вызвове модуля
    """
    apply_migrations()

    logger.info("Start consumer...")
    flask_thread = threading.Thread(target=flask_app)
    collector_thread = threading.Thread(target=events_hadler)
    flask_thread.start()
    collector_thread.start()
