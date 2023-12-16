"""Service providers."""

from dependency_injector import containers, providers

from api_bloxs.modules.account.service.account import AccountService


class ServicesContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    account_service = providers.Factory(
        AccountService,
        account_repository=repositories.account_repository,
    )
