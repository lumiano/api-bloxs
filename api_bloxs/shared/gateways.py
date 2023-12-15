"""Core container."""

from dependency_injector import containers, providers

from api_bloxs.infra.database import MySQLDatabase


class GatewaysContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(MySQLDatabase, db_url=config.DATABASE_DSN)
