"""Core container."""


from dependency_injector import containers, providers


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
