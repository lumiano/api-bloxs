from typing import List

from sqlalchemy import Transaction

from api_bloxs.base.service import Service
from api_bloxs.modules.transaction.dto.query import TransactionQueryDto
from api_bloxs.modules.transaction.repositories.transaction import \
    TransactionRepository


class TransactionService(Service):
    """Transaction service."""

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def get_all(self) -> List[Transaction]:
        """Get all transactions."""
        return self.transaction_repository.get_all()

    def get_by_id(self, transaction_id: int) -> Transaction:
        """Get transaction by id."""
        return self.transaction_repository.get_by_id(transaction_id)

    def create(self, transaction: Transaction) -> Transaction:
        return self.transaction_repository.create(transaction)

    def update(self, transaction: Transaction) -> Transaction:
        """Update transaction."""
        return self.transaction_repository.update(transaction)

    def delete(self, transaction_id: int) -> None:
        return self.transaction_repository.delete(transaction_id)

    def get_all_by_account_id(
        self,
        query: TransactionQueryDto,
    ) -> List[Transaction]:
        """Get all transactions by account id."""
        return self.transaction_repository.get_all_by_account_id(query)
