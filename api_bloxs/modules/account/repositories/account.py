from contextlib import AbstractContextManager
from typing import Callable

from requests import Session

from api_bloxs.modules.account.model.account import Account


class BaseRepository:
    def __init__(self, session, model):
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


class AccountRepository(BaseRepository):
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        super().__init__(session_factory, Account)

    def get_by_id(self, id) -> Account:
        with self.session() as session:
            account = session.query(Account).filter_by(id=id).first()

            if not account:
                raise AccountNotFoundError(id)

            return account


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class AccountNotFoundError(NotFoundError):
    entity_name = "Account"
