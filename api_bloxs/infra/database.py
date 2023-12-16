from contextlib import AbstractContextManager, contextmanager
from typing import Any

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session

from api_bloxs.base.model import Base


class MySQLDatabase:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)

        self._session = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            ),
        )

    def create_database(self) -> Any:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> AbstractContextManager[Session]:
        session = self._session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
