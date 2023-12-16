from typing import List, Dict

from apiflask import APIBlueprint, APIFlask

from api_bloxs.shared.application import ApplicationContainer

from api_bloxs.routes.account import account_blueprint
from api_bloxs.routes.person import person_blueprint


class AppConfigurator:
    """Configures application settings."""

    def __init__(self, app, config: ApplicationContainer) -> None:
        self.app = app
        self.config = config

    def configure(self) -> None:
        """Set up application configuration."""
        config_data = {
            "SQLALCHEMY_DATABASE_URI": self.config.SQLALCHEMY_DATABASE_URI(),
            "SQLALCHEMY_TRACK_MODIFICATIONS": self.config.SQLALCHEMY_TRACK_MODIFICATIONS(),
            "DEBUG": self.config.FLASK_DEBUG(),
            "SQLALCHEMY_ECHO": self.config.SQLALCHEMY_ECHO(),
        }

        env = self.config.FLASK_ENV()

        if env == "production":
            config_data.update(
                {
                    "DEBUG": False,
                    "SQLALCHEMY_ECHO": False,
                }
            )

        self.app.config.update(config_data)


class DatabaseInitializer:
    """Initializes the application database."""

    def __init__(self, container: ApplicationContainer, config) -> None:
        self.container = container
        self.config = config

    def initialize(self) -> None:
        """Set up the database."""

        if self.config.FLASK_ENV() == "test":
            self.create_database()

        self.container.migrate()

    def create_database(self) -> None:
        """Create the database."""
        gateways = self.container.gateways()
        db = gateways.database()
        db.create_database()


class BlueprintInitializer:
    """Registers blueprints with the application."""

    def __init__(self, app) -> None:
        self.app = app

    def register_blueprints(
        self,
    ) -> None:
        """Register blueprints."""
        for blueprint in self.load_blueprints():
            self.app.register_blueprint(blueprint)

    def load_blueprints(self) -> List[APIBlueprint]:
        """Load blueprints."""
        return [account_blueprint, person_blueprint]


class App:
    """Application class."""

    def __init__(self) -> None:
        """Initialize application."""
        self.container = ApplicationContainer()
        self.app = self.container.app()
        self.config = self.container.config

        self.setup()

    def setup(self) -> None:
        """Set up the application."""

        configurer = AppConfigurator(self.app, self.config)

        configurer.configure()

        database_initializer = DatabaseInitializer(self.container, self.config)

        database_initializer.initialize()

        blueprint_registrar = BlueprintInitializer(self.app)

        blueprint_registrar.register_blueprints()

    def __call__(self) -> APIFlask:
        """Return application."""
        return self.app


app = App().__call__()
