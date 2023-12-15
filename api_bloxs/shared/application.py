"""Container module."""

from apiflask import APIFlask
from dependency_injector import containers, providers
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api_bloxs.shared.core import CoreContainer
from api_bloxs.shared.environment import Environment
from api_bloxs.shared.gateways import GatewaysContainer
from api_bloxs.shared.repositories import RepositoriesContainer
from api_bloxs.shared.services import ServicesContainer


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["api_bloxs.routes"])

    environment = Environment()

    loaded_environment = environment.load()

    loaded_environment.__dict__

    config = providers.Configuration()

    config.from_dict(
        loaded_environment.__dict__,
        required=True,
    )

    app = providers.Singleton(
        APIFlask,
        __name__,
    )

    db = providers.Singleton(
        SQLAlchemy,
        app=app,
    )

    migrate = providers.Singleton(
        Migrate,
        app=app,
        db=db,
    )

    core = providers.Container(CoreContainer, config=config)

    gateways = providers.Container(GatewaysContainer, config=config)

    repositories = providers.Container(RepositoriesContainer, gateways=gateways)

    services = providers.Container(
        ServicesContainer,
        repositories=repositories,
    )
