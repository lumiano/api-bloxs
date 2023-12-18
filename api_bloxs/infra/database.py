import dataclasses
from contextlib import AbstractContextManager, contextmanager

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session

from api_bloxs.base.database import Database
from api_bloxs.infra.trace import Trace


@dataclasses.dataclass
class MySQLDatabase(Database):
    """MySQL Database"""

    def __init__(self, db_url: str, trace: Trace) -> None:
        self.engine = create_engine(db_url)
        self.trace = trace

        self._session = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            ),
        )

    @contextmanager
    def session(
        self,
    ) -> AbstractContextManager[Session]:
        session = self._session()
        try:
            yield session
            self.trace.logger.info("Commiting session")
        except Exception as e:
            self.trace.logger.error("Error on session rollback")
            session.rollback()

            self.trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")
            raise
        finally:
            self.trace.logger.info("Closing session")
            session.close()
