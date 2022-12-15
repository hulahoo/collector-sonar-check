from events_collector.config.log_conf import logger
from events_collector.apps.consumer.base import BaseConsumer


def events_hadler():
    # start consumer
    logger.info("Start main consumer...")
    main_consumer_object = BaseConsumer()
    main_consumer_object.start_process()
