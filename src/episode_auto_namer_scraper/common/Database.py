"""Database module."""

import logging
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, DeclarativeBase, scoped_session, sessionmaker

logger = logging.getLogger(__name__)

meta = MetaData()


class Base(DeclarativeBase):
    metadata = meta
    __table_args__ = {'mariadb_engine': 'Aria'}


class Database:
    def __init__(self, db_uri: str) -> None:
        try:
            if db_uri is None:
                raise Exception("No Database URI provided!")
            else:
                engine = create_engine(db_uri)
                self._session_factory = scoped_session(sessionmaker(bind=engine))
                Base.query = self._session_factory.query_property()
                Base.metadata.create_all(engine)
        except Exception as e:
            logger.exception(str(e))

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
