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

    def create_account(self, account):
        """Create account"""
        return self.account_repository.create_account(account)

    def update_account(self, account_id, account):
        """Update account"""
        return self.account_repository.update_account(account_id, account)

    def delete_account(self, account_id):
        """Delete account"""
        return self.account_repository.delete_account(account_id)
