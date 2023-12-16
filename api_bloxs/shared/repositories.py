"""Repositories container."""


from dependency_injector import containers, providers

from api_bloxs.modules.account.repositories.account import AccountRepository


class RepositoriesContainer(containers.DeclarativeContainer):
    gateways = providers.DependenciesContainer()

    account_repository = providers.Factory(
        AccountRepository, session=gateways.database.provided.session
    )
