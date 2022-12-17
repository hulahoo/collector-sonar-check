from abc import abstractmethod, ABC
from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from events_collector.config.config import settings


class Database(ABC):
    def __init__(self) -> None:
        self._engine = self._create_engine()
        self._session_factory = self._init_session_factory()

    @abstractmethod
    def get_db_url(self):
        ...

    @abstractmethod
    def _create_engine(self):
        ...

    @abstractmethod
    def _init_session_factory(self):
        ...

    @contextmanager
    def session(self):
        session: Session = self._session_factory()

        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class SyncPostgresDriver(Database):
    def _create_engine(self):
        return create_engine(
            self.get_db_url(),
            pool_pre_ping=True,
            pool_recycle=3600,
            max_overflow=10,
            pool_size=15,
        )

    def get_db_url(self):
        return f"postgresql://{settings.APP_POSTGRESQL_USER}:{settings.APP_POSTGRESQL_PASSWORD}@" \
                f"{settings.APP_POSTGRESQL_HOST}:{settings.APP_POSTGRESQL_PORT}/{settings.APP_POSTGRESQL_NAME}"

    def _init_session_factory(self):
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


metadata = MetaData(bind=SyncPostgresDriver()._engine)
Base = declarative_base(metadata=metadata)
