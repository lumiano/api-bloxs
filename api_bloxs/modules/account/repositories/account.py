from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy import and_


from api_bloxs.base.repository import BaseRepository
from api_bloxs.modules.account.model.account import Account
from sqlalchemy.orm import Session


class AccountRepository(BaseRepository):
    """Account repository"""

    def __init__(self, session: Callable[..., AbstractContextManager[Session]]) -> None:
        super().__init__(session=session, model=Account)

    def get_by_id(self, id) -> Account:
        """Get account by id"""
        with self.session() as session:
            account = session.query(Account).filter_by(id=id).first()
            return account

    def create(self, obj: Account) -> Account:
        """Create account"""
        with self.session() as session:
            session.add(obj)
            session.commit()
            return obj

    def find_by_params(self, params) -> Account:
        """Find account by params"""

        with self.session() as session:
            account = session.query(Account).filter_by(**params).first()
            return account
