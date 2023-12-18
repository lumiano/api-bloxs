from typing import List

from sqlalchemy import asc, desc

from api_bloxs.base.database import Database
from api_bloxs.base.repository import Repository
from api_bloxs.modules.transaction.dto.transaction import TransactionDto
from api_bloxs.modules.transaction.model.transaction import Transaction


class TransactionRepository(Repository):
    """Transaction repository"""

    def __init__(self, session: Database):
        self.session = session

    def get_by_id(self, id):
        """Get by id"""

        with self.session.context() as session:
            return session.query(Transaction).filter_by(id=id).first()

    def get_all(self):
        """Get all"""
        with self.session.context() as session:
            return session.query(Transaction).all()

    def create(self, transaction):
        """Create"""
        with self.session.context() as session:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            return transaction

    def update(self, transaction):
        """Update"""
        with self.session.context() as session:
            session.merge(transaction)
            session.commit()

            return self.get_by_id(transaction.id)

    def delete(self, id):
        """Delete"""
        with self.session.context() as session:
            session.query(Transaction).filter_by(id=id).delete()
            session.commit()

    def get_all_by_account_id(self, query: TransactionDto) -> List[Transaction]:
        """Get transactions by account id and pagination"""

        sort_desc = query.get("sort") == "desc"
        order_attr = getattr(Transaction, query["order_by"])
        order = desc(order_attr) if sort_desc else asc(order_attr)

        with self.session.context() as session:
            return (
                session.query(Transaction)
                .filter_by(account_id=query["account_id"])
                .order_by(order)
                .offset((query["page"] - 1) * query["offset"])
                .limit(query["offset"])
                .all()
            )
