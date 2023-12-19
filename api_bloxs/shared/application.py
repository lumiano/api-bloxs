from dependency_injector import containers, providers

from api_bloxs.infra.environment import Environment
from api_bloxs.shared.infra import InfraContainer
from api_bloxs.shared.repositories import RepositoriesContainer
from api_bloxs.shared.services import ServicesContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container"""

    wiring_config = containers.WiringConfiguration(packages=["api_bloxs.controllers"])

    environment: providers.Provider[Environment] = providers.Singleton(Environment)

    _envs = environment()

    config = providers.Configuration()

    config.from_dict(_envs.load().__dict__, required=True)

    infra: providers.Provider[InfraContainer] = providers.Container(
        InfraContainer, config=config
    )

    repositories: providers.Provider[RepositoriesContainer] = providers.Container(
        RepositoriesContainer, infra=infra
    )

    services: providers.Provider[ServicesContainer] = providers.Container(
        ServicesContainer,
        repositories=repositories,
    )
