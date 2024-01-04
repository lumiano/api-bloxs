from typing import List

from api_bloxs.base.service import Service
from api_bloxs.modules.account.model.account import Account
from api_bloxs.modules.account.repositories.account import AccountRepository


class AccountService(Service):
    """Account service."""

    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def get_all(self, query) -> List[Account]:
        """Get all accounts."""
        return self.account_repository.get_all(query)

    def get_by_id(self, account_id: int) -> Account:
        """Get account by id."""
        return self.account_repository.get_by_id(account_id)

    def create(self, account: Account) -> Account:
        """Create account."""
        return self.account_repository.create(account)

    def update(self, account: Account) -> Account:
        """Update account."""
        return self.account_repository.update(account)

    def delete(self, account_id: int) -> None:
        """Delete account."""
        return self.account_repository.delete(account_id)

    def get_by_type_and_person_id(self, account_type: str, person_id: int) -> Account:
        """Get by id"""
        return self.account_repository.get_by_type_and_person_id(
            account_type, person_id
        )
