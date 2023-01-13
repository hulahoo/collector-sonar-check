from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import (
    Column, String, BigInteger, Text,
    DateTime, Boolean, DECIMAL, text, UniqueConstraint
)

from events_collector.models.abstract import IDBase, TimestampBase


class Indicator(TimestampBase):
    __tablename__ = "indicators"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    ioc_type = Column(String(32))
    value = Column(String(1024))
    context = Column(JSONB)
    is_sending_to_detections = Column(Boolean, default=True)
    is_false_positive = Column(Boolean, default=False)
    weight = Column(DECIMAL)
    feeds_weight = Column(DECIMAL)
    time_weight = Column(DECIMAL)
    tags_weight = Column(DECIMAL)
    is_archived = Column(Boolean, default=False)
    false_detected_counter = Column(BigInteger)
    positive_detected_counter = Column(BigInteger)
    total_detected_counter = Column(BigInteger)
    first_detected_at = Column(DateTime)
    last_detected_at = Column(DateTime)
    created_by = Column(BigInteger)
    updated_at = Column(DateTime)

    UniqueConstraint(value, ioc_type, name='indicators_unique_value_type')

    def __str__(self):
        return f"{self.value}"


class StatCheckedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_checked_objects"

    indicator_id = Column(UUID(as_uuid=True), nullable=True)


class StatMatchedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_matched_objects"

    indicator_id = Column(UUID(as_uuid=True))


class Detections(IDBase, TimestampBase):
    __tablename__ = "detections"

    source_event = Column(JSONB)
    source_message = Column(Text)
    indicator_id = Column(UUID(as_uuid=True))
    detection_event = Column(JSONB)
    detection_message = Column(Text)
    tags_weight = Column(DECIMAL)
    indicator_weight = Column(DECIMAL)


class DetectionTagRelationships(IDBase, TimestampBase):
    __tablename__ = "detection_tag_relationships"

    detection_id = Column(BigInteger)
    tag_id = Column(BigInteger)
