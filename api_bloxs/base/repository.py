import dataclasses
from abc import ABC, abstractmethod
from typing import Any

from api_bloxs.infra.database import Database


@dataclasses.dataclass
class Repository(ABC):
    """Base repository"""

    database: Database

    @abstractmethod
    def get_by_id(self, id: int) -> Any:
        """Get by id"""
        pass

    @abstractmethod
    def get_all(self) -> Any:
        """Get all"""
        pass

    @abstractmethod
    def create(self, entity: Any) -> Any:
        """Create"""
        pass

    @abstractmethod
    def update(self, id: int, entity: Any) -> Any:
        """Update"""
        pass

    @abstractmethod
    def delete(self, id: int) -> Any:
        """Delete"""
        pass
