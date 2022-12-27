import threading

from events_collector.config.log_conf import logger
from events_collector.web.routers.api import execute as flask_app
from events_collector.apps.worker.events_handler import events_hadler


def execute() -> None:
    """
    Function entrypoint to start:
    1. Worker to consume events from kafka
    2. Flask application to serve enpoints
    3. Apply migrations
    """
    flask_thread = threading.Thread(target=flask_app)
    collector_thread = threading.Thread(target=events_hadler)

    logger.info("Start Flask app")
    flask_thread.start()

    logger.info("Start worker")
    collector_thread.start()
