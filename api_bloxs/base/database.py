import dataclasses
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

from sqlalchemy.orm import Session as SQLAlchemySession


@dataclasses.dataclass
class Database(ABC):
    """Database"""

    @abstractmethod
    def context(self) -> AbstractContextManager[SQLAlchemySession]:
        """Session"""
        pass
