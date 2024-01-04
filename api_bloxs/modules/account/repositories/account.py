from typing import List

from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload

from api_bloxs.base.repository import Repository
from api_bloxs.infra.database import Database
from api_bloxs.modules.account.model.account import Account
from api_bloxs.modules.person.model.person import Person


class AccountRepository(Repository):
    """Account repository"""

    def __init__(self, session: Database):
        self.session = session

    def get_by_id(self, id: int) -> Account:
        """Get by id"""

        with self.session.context() as session:
            return session.query(Account).filter_by(id=id).first()

    def get_all(self, query) -> List[Account]:
        """Get all"""
        sort_desc = query.get("sort") == "desc"
        order_attr = getattr(Account, query["order_by"])
        order = desc(order_attr) if sort_desc else asc(order_attr)

        with self.session.context() as session:
            query_builder = (
                session.query(Account).join(Person).options(joinedload(Account.person))
            )

            if query.get("id"):
                query_builder = query_builder.filter(Account.id == query["id"])

            if query.get("document"):
                query_builder = query_builder.filter(
                    Person.document.like(f"%{query['document']}%")
                )

            if query.get("person_id"):
                query_builder = query_builder.filter(
                    Account.person_id == query["person_id"]
                )

            if query.get("account_type"):
                query_builder = query_builder.filter(
                    Account.account_type == query["account_type"]
                )

            if query.get("is_active"):
                query_builder = query_builder.filter(
                    Account.is_active == query["is_active"]
                )

            return query_builder.order_by(order).all()

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
