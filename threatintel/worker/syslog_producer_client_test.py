import logging.handlers

from logging import LogRecord


class SyslogKafkaCustom(logging.handlers.SysLogHandler):

    def handle(self, record: LogRecord) -> bool:
        data = record.getMessage()
        print(data)
        return super(SyslogKafkaCustom, self).handle(record)


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8888

    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger()
    logger.addHandler(SyslogKafkaCustom(address=('localhost', 8888)))

    with open('text.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    logger.info(data)
