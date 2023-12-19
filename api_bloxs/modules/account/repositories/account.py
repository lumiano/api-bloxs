from typing import List

from api_bloxs.base.repository import Repository
from api_bloxs.infra.database import Database
from api_bloxs.modules.account.model.account import Account


class AccountRepository(Repository):
    """Account repository"""

    def __init__(self, session: Database):
        self.session = session

    def get_by_id(self, id: int) -> Account:
        """Get by id"""

        with self.session.context() as session:
            return session.query(Account).filter_by(id=id).first()

    def get_all(self) -> List[Account]:
        """Get all"""
        with self.session.context() as session:
            return session.query(Account).all()

    def create(self, account: Account) -> Account:
        """Create"""
        with self.session.context() as session:
            session.add(account)

            session.commit()
            return self.get_by_id(account.id)

    def update(self, account: Account) -> Account:
        """Update"""
        with self.session.context() as session:
            session.merge(account)
            session.commit()

            return self.get_by_id(account.id)

    def delete(self, id: int) -> None:
        """Delete"""
        with self.session.context() as session:
            session.query(Account).filter_by(id=id).delete()
            session.commit()

    def get_by_type_and_person_id(self, account_type: str, person_id: int) -> Account:
        """Get by id"""

        with self.session.context() as session:
            return (
                session.query(Account)
                .filter_by(account_type=account_type, person_id=person_id)
                .first()
            )
