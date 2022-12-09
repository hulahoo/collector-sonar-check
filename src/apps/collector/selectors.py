from typing import Optional

from sqlalchemy import select, desc, and_

from src.models.models import Indicator, StatCheckedObjects, StatMatchedObjects
from src.models.base import SyncPostgresDriver


class IndicatorProvider:
    def get_by_type_and_value(self, *, type: str, value: Optional[str]) -> Optional[Indicator]:
        with SyncPostgresDriver().session() as db:
            query = select(Indicator).filter(
                and_(
                    Indicator.type == type,
                    Indicator.value == value
                )
            ).order_by(desc(Indicator.created_at))
            indicators = db.execute(query)
            return indicators.scalars().first()


class StatCheckedProvider:
    def create(self) -> StatCheckedObjects:
        with SyncPostgresDriver().session() as db:
            checked_object = StatCheckedObjects()

            db.add(checked_object)
            db.flush()
            db.commit()


class StatMatchedProvider:
    def create(self, indicator_id: int) -> StatMatchedObjects:
        with SyncPostgresDriver().session() as db:
            matched_object = StatMatchedObjects(indicator_id=indicator_id)

            db.add(matched_object)
            db.flush()
            db.commit()


stat_matched_selector = StatMatchedProvider()
stat_checked_selector = StatCheckedProvider()
indicator_selector = IndicatorProvider()
