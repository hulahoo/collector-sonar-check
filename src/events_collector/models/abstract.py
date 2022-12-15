import sqlalchemy

from events_collector.models.base import Base


class IDBase(Base):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True)


class TimestampBase(Base):
    __abstract__ = True

    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.now(), index=True, nullable=False
    )
