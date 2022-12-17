from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine

from events_collector.config.log_conf import logger
from events_collector.models.base import SyncPostgresDriver
from events_collector.models.models import StatCheckedObjects, StatMatchedObjects, Detections


def create_migrations() -> None:
    """Create migrations for Database"""
    engine: Engine = SyncPostgresDriver()._engine
    tables_list = [StatMatchedObjects.__tablename__, StatCheckedObjects.__tablename__, Detections.__tablename__]

    if not inspect(engine).has_table("stat_checked_objects"):
        StatCheckedObjects.__table__.create(engine)
        tables_list.remove(StatCheckedObjects.__tablename__)
        logger.info("Table StatCheckedObjects created")

    if not inspect(engine).has_table("stat_matched_objects") and inspect(engine).has_table("indicators"):
        StatMatchedObjects.__table__.create(SyncPostgresDriver().engine)
        tables_list.remove(StatMatchedObjects.__tablename__)
        logger.info("Table StatMatchedObjects created")

    if not inspect(engine).has_table("detections") and inspect(engine).has_table("indicators"):
        tables_list.remove(Detections.__tablename__)
        Detections.__table__.create(SyncPostgresDriver().engine)
        logger.info("Table Detections created")

    logger.info(f"List of unapplied tables: {tables_list}. Waiting for Indicators table to be applied")
    logger.info("Migration applied successfully")
