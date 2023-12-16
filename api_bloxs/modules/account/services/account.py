from abc import ABC, abstractmethod
from typing import List

from api_bloxs.modules.account.model.account import Account
from api_bloxs.modules.account.repositories.account import AccountRepository


class AccountService:
    """Account Service"""

    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    def get_by_id(self, account_id):
        """Get account by id"""

        return self.account_repository.get_by_id(account_id)

    def get_accounts(self):
        """Get all accounts"""

        return self.account_repository.get_accounts()

    def create(self, account):
        """Create account"""

        return self.account_repository.create(account)

    def update_account(self, account_id, account):
        """Update account"""

        return self.account_repository.update_account(account_id, account)

    def delete_account(self, account_id):
        """Delete account"""

        return self.account_repository.delete_account(account_id)

    def find_by_params(self, params) -> Account:
        """Find by params"""

        return self.account_repository.find_by_params(params)
