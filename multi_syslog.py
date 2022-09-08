import logging
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - [%(threadName)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)
logger = logging.getLogger(__name__)


def worker():
    for i in range(5):
        logger.info(f"журнальное сообщение {i} из рабочего потока")


thread = threading.Thread(target=worker)
thread.start()

for i in range(5):
    logger.info(f"журнальное сообщение {i} из главного потока")

thread.join()
