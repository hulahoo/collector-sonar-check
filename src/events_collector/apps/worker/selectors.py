from decimal import Decimal
from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, desc, and_, update

from events_collector.models.base import SyncPostgresDriver
from events_collector.models.models import Indicator, StatCheckedObjects, StatMatchedObjects, Detections


class BaseProvider:

    model = None

    def update_field(self, filter_data, col, val, *fields):
        with SyncPostgresDriver().session() as db:
            db: Session
            query = update(self.model).where(
                *(
                    getattr(self.model, field) == (
                        filter_data.get(field) if isinstance(filter_data, dict) else getattr(filter_data, field)
                    )
                    for field in fields
                )
            ).values(**{col: val})
            db.execute(query)
            db.commit()


class IndicatorProvider(BaseProvider):

    model = Indicator

    def get_by_value(self, *, value: Optional[str]) -> Optional[Indicator]:
        with SyncPostgresDriver().session() as db:
            query = select(self.model).filter(
                and_(
                    Indicator.value == value,
                    Indicator.is_archived.is_not(True),
                    Indicator.is_false_positive.is_not(True),
                    Indicator.is_sending_to_detections.is_not(False)
                )
            ).order_by(desc(Indicator.created_at))
            indicators = db.execute(query)
            return indicators.scalars().first()


class StatCheckedProvider(BaseProvider):

    model = StatCheckedObjects

    def create(self) -> StatCheckedObjects:
        with SyncPostgresDriver().session() as db:
            checked_object = self.model()
            db.add(checked_object)
            db.flush()
            db.commit()
            return checked_object


class StatMatchedProvider(BaseProvider):

    model = StatMatchedObjects

    def create(self, indicator_id: int) -> StatMatchedObjects:
        with SyncPostgresDriver().session() as db:
            matched_object = self.model(indicator_id=indicator_id)
            db.add(matched_object)
            db.flush()
            db.commit()
            return matched_object


class DetectionsProvider(BaseProvider):

    model = Detections

    def create(
        self,
        source_event: dict,
        source_message: str,
        indicator_weight: Decimal,
        tags_weight: Decimal,
        indicator_id: UUID,
        detection_event: dict
    ) -> Detections:
        with SyncPostgresDriver().session() as db:
            detection = self.model(
                source_event=source_event,
                source_message=source_message,
                indicator_weight=indicator_weight,
                tags_weight=tags_weight,
                detection_message=str(detection_event),
                indicator_id=indicator_id,
                detection_event=detection_event
            )

            db.add(detection)
            db.flush()
            db.commit()
            return detection


detections_selector = DetectionsProvider()
stat_matched_selector = StatMatchedProvider()
stat_checked_selector = StatCheckedProvider()
indicator_selector = IndicatorProvider()
