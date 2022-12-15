import threading

from events_collector.config.log_conf import logger
from events_collector.models.migrations import apply_migrations
from events_collector.web.routers.api import execute as flask_app
from events_collector.apps.collector.events_handler import events_hadler


def execute() -> None:
    """
    Function entrypoint to start:
    1. Worker to consume events from kafka
    2. Flask application to serve enpoints
    3. Apply migrations
    """
    apply_migrations()

    logger.info("Start consumer...")
    flask_thread = threading.Thread(target=flask_app)
    collector_thread = threading.Thread(target=events_hadler)
    flask_thread.start()
    collector_thread.start()
