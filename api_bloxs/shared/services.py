from dependency_injector import containers, providers

from api_bloxs.base.service import Service
from api_bloxs.modules.account.services.account import AccountService
from api_bloxs.modules.person.services.person import PersonService
from api_bloxs.modules.transaction.services.transaction import \
    TransactionService


class ServicesContainer(containers.DeclarativeContainer):
    """Service providers."""

    repositories = providers.DependenciesContainer()

    account: providers.Provider[AccountService] = providers.Factory(
        AccountService, account_repository=repositories.account
    )

    person: providers.Provider[PersonService] = providers.Factory(
        PersonService, person_repository=repositories.person
    )

    transaction: providers.Provider[TransactionService] = providers.Factory(
        TransactionService, transaction_repository=repositories.transaction
    )
