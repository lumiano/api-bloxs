from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session


class BaseRepository:
    """Base repository class for all repositories."""

    def __init__(self, session: Session, model):
        self.session = session

        self.model = model

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, id):
        return self.session.query(self.model).filter_by(id=id).first()

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, obj):
        self.session.commit()
        return obj

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()
        return obj
