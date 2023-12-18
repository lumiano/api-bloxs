from typing import List

from api_bloxs.base.repository import Repository
from api_bloxs.modules.transaction.model.transaction import Transaction


class TransactionRepository(Repository):
    """Transaction repository"""

    def __init__(self, database):
        self.database = database

    def get_by_id(self, id):
        """Get by id"""

        with self.database.session() as session:
            return session.query(Transaction).filter_by(id=id).first()

    def get_all(self):
        """Get all"""
        with self.database.session() as session:
            return session.query(Transaction).all()

    def create(self, transaction):
        """Create"""
        with self.database.session() as session:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            return transaction

    def update(self, transaction):
        """Update"""
        with self.database.session() as session:
            session.merge(transaction)
            session.commit()

            return self.get_by_id(transaction.id)

    def delete(self, id):
        """Delete"""
        with self.database.session() as session:
            session.query(Transaction).filter_by(id=id).delete()
            session.commit()

    def get_transactions_by_account_id(self, account_id) -> List[Transaction]:
        """Get transactions by account id"""
        with self.database.session() as session:
            return (
                session.query(Transaction)
                .filter_by(account_id=account_id)
                .order_by(Transaction.transaction_date)
                .all()
            )
