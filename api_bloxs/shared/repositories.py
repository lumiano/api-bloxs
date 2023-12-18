from dependency_injector import containers, providers

from api_bloxs.modules.account.repositories.account import AccountRepository
from api_bloxs.modules.person.repositories.person import PersonRepository
from api_bloxs.modules.transaction.repositories.transaction import \
    TransactionRepository


class RepositoriesContainer(containers.DeclarativeContainer):
    """Repositories container."""

    infra = providers.DependenciesContainer()

    account: providers.Provider[AccountRepository] = providers.Factory(
        AccountRepository, database=infra.database
    )

    person: providers.Provider[PersonRepository] = providers.Factory(
        PersonRepository, database=infra.database
    )

    transaction: providers.Provider[TransactionRepository] = providers.Factory(
        TransactionRepository, database=infra.database
    )
