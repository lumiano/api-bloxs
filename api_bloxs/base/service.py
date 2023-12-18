from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Service(ABC):
    """BaseService"""

    @abstractmethod
    def get_by_id(self, id):
        """Get by id"""
        pass

    @abstractmethod
    def get_all(self):
        """Get all"""
        pass

    @abstractmethod
    def create(self, entity):
        """Create"""
        pass

    @abstractmethod
    def update(self, id, entity):
        """Update"""
        pass

    @abstractmethod
    def delete(self, id):
        """Delete"""
        pass
