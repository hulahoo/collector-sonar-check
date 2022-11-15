from abc import abstractmethod, ABC
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session


Base = declarative_base()


class Database(ABC):
    def __init__(self) -> None:
        self._engine = self._create_engine()
        self._session_factory = self._init_session_factory()

    @abstractmethod
    def _get_db_url(self):
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
        return create_async_engine(
            self._get_db_url(),
            pool_pre_ping=True,
            pool_recycle=3600,
            max_overflow=10,
            pool_size=15,
        )

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
