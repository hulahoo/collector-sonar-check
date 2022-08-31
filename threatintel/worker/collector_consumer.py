import json
from uuid import uuid4

from dagster import op, get_dagster_logger, job, Field, DynamicOut, DynamicOutput
from django.utils import timezone
from kafka import KafkaConsumer, TopicPartition


def exist_indicator(indicator, data: dict, config):
    from intelhandler.models import Indicator, Statistic
    indicator: Indicator
    indicator.detected += 1
    indicator.last_detected_date = timezone.now()

    indicator.save()
    data['config'] = config

    Statistic.objects.create(data=data)


def not_exist_indicator(data, config):
    from intelhandler.models import Indicator, Statistic

    value = data.get('indicator')
    Indicator.objects.get_or_create(name=value, defaults={
        "uuid": uuid4(),
        "supplier_name": data.get('supplier_name', value),
        "supplier_confidence": data.get('confidence', value),
        "weight": data.get('confidence', value),
        "detected": 1,
        "first_detected_date": timezone.now(),
        "last_detected_date": timezone.now()
    })

    data['config'] = config
    Statistic.objects.create(data=data)


def event_worker(data: dict):
    from intelhandler.models import Indicator
    indicator = data.get('indicator')
    # todo find by that
    indicator_obj = Indicator.objects.filter(name=indicator).first()
    if indicator_obj is not None:
        exist_indicator(indicator, data, config)
    else:
        not_exist_indicator(indicator, config)


@op(config_schema={'partitions': Field(list)}, out=DynamicOut())
def consumer_dispatcher_op(context):
    partitions = context.op_config['partitions']

    for partition in partitions:
        yield DynamicOutput(
            value=partition,
            mapping_key=f'partition_{partition}'
        )


@op(config_schema={"config": Field(dict)})
def op_consumer(context, partition: int):
    config = context.op_config['config']

    from worker.utils import django_init
    django_init()
    from django.conf import settings
    logger = get_dagster_logger()
    group_id = settings.KAFKA_GROUP_ID
    kafka_ip = settings.KAFKA_IP
    topic = settings.KAFKA_TOPIC

    kafka_consumer = KafkaConsumer(
        bootstrap_servers={f'{kafka_ip}:9092'},
        auto_offset_reset='earliest',
        group_id=group_id,
    )
    topic_partition = TopicPartition(topic, partition)
    topics = [topic_partition]
    kafka_consumer.assign(topics)
    while True:
        for tp, messages in tuple(kafka_consumer.poll(timeout_ms=5000).items()):
            for message in messages:
                data = json.loads(message.value)
                logger.info(f'{data}')
                event_worker(data, config)


@op
def consumer_collector(data):
    return len(data)


@job
def job_consumer():
    results = consumer_dispatcher_op().map(op_consumer)
    consumer_collector(results.collect())
