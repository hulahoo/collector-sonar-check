import json
from typing import List

from kafka import KafkaProducer

from worker.utils import django_init

django_init()
from django.conf import settings


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


class MultiProducer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=[f'{settings.KAFKA_IP}:9092'],
                                      value_serializer=json_serializer)

    def send_data(self, data: dict):
        try:
            topic = settings.KAFKA_TOPIC
            self.producer.send(topic, data)
        except Exception as e:
            print(e)

    def send_list_of_data(self, data_lst: List[dict]):
        for data in data_lst:
            self.send_data(data)
        self.flush()

    def flush(self, timeout=60 * 5):
        self.producer.flush(timeout=timeout)
