from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import (
    Column, Integer, String, BigInteger,
    DateTime, Boolean, DECIMAL, text
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
    ioc_weight = Column(DECIMAL)
    feeds_weight = Column(DECIMAL)
    time_weight = Column(DECIMAL)
    tags_weight = Column(DECIMAL)
    is_archived = Column(Boolean, default=False)
    false_detected_counter = Column(Integer)
    positive_detected_counter = Column(Integer)
    total_detected_counter = Column(Integer)
    first_detected_at = Column(DateTime)
    last_detected_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(DateTime)

    def __str__(self):
        return f"{self.value}"


class StatCheckedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_checked_objects"


class StatMatchedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_matched_objects"

    indicator_id = Column(UUID(as_uuid=True))


class Detections(IDBase, TimestampBase):
    __tablename__ = "detections"

    source_event = Column(JSONB, default=None, nullable=True)
    indicator_id = Column(UUID(as_uuid=True))
    detection_event = Column(JSONB, default=None, nullable=True)


class DetectionTagRelationships(IDBase, TimestampBase):
    __tablename__ = "detection_tag_relationships"

    detection_id = Column(BigInteger)
    tag_id = Column(BigInteger)
