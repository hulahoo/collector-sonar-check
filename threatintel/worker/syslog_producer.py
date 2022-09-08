import json
import logging
import socket
import time
from logging import StreamHandler, LogRecord

from intelhandler.models import LogStatistic
from worker.kafka_producer import MultiProducer

SPLIT_WORD = '|threat|'


def record_to_json(record: LogRecord):
    message = f'{record.asctime} | {record.getMessage()}'
    pattern = {"indicator": "name_indicator", "config": "", "supplier_name": "", "confidence": ""}
    if SPLIT_WORD in message:
        message = message.split(SPLIT_WORD, maxsplit=1)[1].strip()
        message_dct: dict = json.loads(message)
        return message_dct
    return None


class SyslogKafkaCustom(StreamHandler):
    def __init__(self, test_mode=False, *args, **kwargs):
        if test_mode:
            self.messages = []
        self.test_mode = test_mode

        try:
            self.kafka_producer = MultiProducer()
        except:
            pass
        super(SyslogKafkaCustom, self).__init__(*args, **kwargs)

    def handle(self, record: LogRecord) -> bool:
        if self.test_mode:
            self.messages.append(record.getMessage())

        result = record_to_json(record)
        if result is not None:
            try:
                LogStatistic.objects.create(data=result)
                self.kafka_producer.send_data(result)
                self.kafka_producer.flush()
            except Exception as e:
                print(e)

        return super(SyslogKafkaCustom, self).handle(record)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger()
    logger.addHandler(SyslogKafkaCustom())
    while True:
        logger.info(
            SPLIT_WORD + ' {"indicator": "test", "config": {"c":"1"}, "supplier_name": "s_n", "confidence": "c_n","weight":10}'
        )
        time.sleep(10)
