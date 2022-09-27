import json
import sys

from dagster import op, get_dagster_logger, job, Field, DynamicOut, DynamicOutput
from kafka import KafkaConsumer, TopicPartition


def exist_indicator(indicator, data: dict, config):
    from intelhandler.models import Indicator, Statistic
    from django.utils import timezone

    print(indicator, 'indicator')
    indicator: Indicator
    indicator.detected += 1
    indicator.last_detected_date = timezone.now()

    indicator.save()
    data['config'] = config

    Statistic.objects.create(data=data)


def feed_creator(data, config):
    from intelhandler.models import Statistic, Feed
    from worker.services import choose_type

    try:
        try:
            method = choose_type(data.get('type', 'json'))
        except Exception as e:
            method = choose_type('json')
        # получаем список методов для фида
        feed = Feed.create_feed(data['feed'])
        feed.save()
        method(feed, None, config)
    except Exception as e:
        print(e)
        print(str(data)[:30])
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    Statistic.objects.create(data=data)


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
    if config is None:
        config = {}

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
                feed_creator(data, config)


@op
def consumer_collector(data):
    return len(data)


@job
def job_consumer():
    results = consumer_dispatcher_op().map(op_consumer)
    consumer_collector(results.collect())
