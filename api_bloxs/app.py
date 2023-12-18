from glob import glob
from importlib import import_module
from os.path import basename, isfile, join
from pathlib import Path

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api_bloxs.base.model import Base
from api_bloxs.shared.application import ApplicationContainer


class App:
    """Application class."""

    def __init__(self) -> None:
        """Initialize application."""
        self.app = APIFlask(
            __name__,
            title="API Bloxs",
            version="1.0.0",
            docs_path="/openapi/docs",
            json_errors=False,
        )

        # add middleware in path

        self.app.security_schemes = {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
            }
        }

        self.container = ApplicationContainer()
        self.config = self.container.config
        self.setup()

    def setup(self) -> None:
        """Set up the application."""
        self._configure_app()
        self._setup_database()
        self._register_blueprints()

    def _configure_app(self) -> None:
        """Configure application settings."""
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

    def _setup_database(self) -> None:
        """Set up the database."""
        db = SQLAlchemy(
            app=self.app,
            add_models_to_shell=True,
            metadata=Base.metadata,
        )

        migrate = Migrate(self.app, db)
        migrate.init_app(self.app, db)

    def _register_blueprints(self) -> None:
        """Register blueprints with the application."""
        routes = glob(join(Path(__file__).parent, "routes/*.py"))

        modules = [
            basename(f)[:-3]
            for f in routes
            if isfile(f) and not f.endswith("__init__.py")
        ]

        blueprints = [
            import_module(f"api_bloxs.routes.{module}").api for module in modules
        ]

        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)

    @classmethod
    def __call__(cls) -> APIFlask:
        """Call the application."""
        return cls().app


app = App.__call__()
