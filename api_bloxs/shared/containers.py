"""Container module."""

from dependency_injector import containers, providers

from api_bloxs.infra.database import Database
from api_bloxs.modules.account.repositories.account import AccountRepository
from api_bloxs.modules.account.service.account import AccountService
from api_bloxs.shared.environment import Environment


class Container(containers.DeclarativeContainer):
    """
    Application container.
    """

    wiring_config = containers.WiringConfiguration(packages=["api_bloxs.routes"])

    environment = Environment()

    configuration = providers.Configuration()

    configuration.from_dict(
        {
            "database": {
                "url": environment.get("DATABASE_URL"),
            },
            "flask": {
                "debug": environment.get("FLASK_DEBUG"),
                "app": environment.get("FLASK_APP"),
                "port": environment.get("FLASK_PORT"),
            },
            "package": {
                "name": environment.get("PACKAGE_NAME"),
            },
        }
    )

    db = providers.Singleton(
        Database,
        db_url=configuration.database.url(),
    )

    account_repository = providers.Factory(
        AccountRepository,
        session_factory=db.provided.session,
    )

    account_service = providers.Factory(
        AccountService,
        account_repository=account_repository,
    )
