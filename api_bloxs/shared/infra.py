from dependency_injector import containers, providers

from api_bloxs.infra.database import MySQLDatabase
from api_bloxs.infra.environment import Environment
from api_bloxs.infra.trace import Trace


class InfraContainer(containers.DeclarativeContainer):
    """Infra container"""

    config = providers.Configuration()

    environment = providers.Singleton(Environment)

    trace: providers.Provider[Trace] = providers.Singleton(Trace)

    database: providers.Provider[MySQLDatabase] = providers.Singleton(
        MySQLDatabase,
        db_url=config.DATABASE_DSN,
        trace=trace,
    )
