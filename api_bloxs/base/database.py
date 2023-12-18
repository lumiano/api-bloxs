import dataclasses
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

from sqlalchemy.orm import Session


@dataclasses.dataclass
class Database(ABC):
    """Database"""

    @abstractmethod
    def session(self) -> AbstractContextManager[Session]:
        """Session"""
        pass
