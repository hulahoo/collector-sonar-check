from dagster import Field, op, DynamicOutput, DynamicOut

from src.eventscollector.config.log_conf import logger
from src.eventscollector.apps.consumer.base import BaseConsumer


@op(config_schema={"config": Field(dict)})
def events_hadler(context: dict, partition: int):

    # start consumer
    logger.info("Start main consumer...")
    main_consumer_object = BaseConsumer(context=context, partition=partition)
    main_consumer_object.start_process()


@op
def consumer_collector(data):
    return len(data)


@op(config_schema={'partitions': Field(list)}, out=DynamicOut())
def consumer_dispatcher_op(context: dict):
    partitions = context.op_config['partitions']
    for partition in partitions:
        yield DynamicOutput(
            value=partition,
            mapping_key=f'partition_{partition}'
        )
