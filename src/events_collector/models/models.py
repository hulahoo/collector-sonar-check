from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    Column, Integer, String, func, Text,
    DateTime, Boolean, Enum, CheckConstraint,  BigInteger
)

from events_collector.commons.enums import TypesEnum
from events_collector.models.abstract import IDBase, TimestampBase


class Indicator(IDBase, TimestampBase):
    """
    Модель индикатора.
    """
    __tablename__ = "indicators"

    type = Column(
        Enum(TypesEnum), default=TypesEnum.IP, nullable=False, name="types"
    )
    value = Column(
        String(256)
    )
    # Контекст
    context = Column(
        JSONB, default=None, nullable=True
    )

    # отпаравка в detections
    is_sending_to_detections = Column(Boolean, default=True)
    is_false_positive = Column(Boolean, default=False)

    weight = Column(
        Integer, CheckConstraint("weight > 0 AND age < 100"), default=0
    )
    is_archived = Column(Boolean, default=False, index=True)

    # счетчики
    false_detected_counter = Column(
        Integer, CheckConstraint("false_detected > 0"), default=0
    )
    positive_detected_counter = Column(
        Integer, CheckConstraint("positive_detected > 0"), default=0
    )
    total_detected_counter = Column(
        Integer, CheckConstraint("detected > 0"), default=0
    )

    # дата регистрации
    first_detected_date = Column(DateTime, nullable=True)
    last_detected_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=func.now(), nullable=False)
    matched_objects = relationship("StatMatchedObjects", backref=backref("indicator"))
    detections = relationship("Detections", backref=backref("indicator"))

    def __str__(self):
        return f"{self.value}"


class StatCheckedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_checked_objects"


class StatMatchedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_matched_objects"

    indicator_id = Column(BigInteger)


class Detections(IDBase, TimestampBase):
    __tablename__ = "detections"

    source_event = Column(JSONB, default=None, nullable=True)
    indicator_id = Column(BigInteger)
    detection_event = Column(Text, default=None, nullable=True)
