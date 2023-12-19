from apiflask import APIFlask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api_bloxs.base.model import Base
from api_bloxs.controllers.account import account
from api_bloxs.controllers.login import login
from api_bloxs.controllers.person import person
from api_bloxs.shared.application import ApplicationContainer


class App:
    """App class"""

    @classmethod
    def build(cls) -> APIFlask:
        app = APIFlask(
            __name__,
            title="API Bloxs",
            version="1.0.0",
            docs_path="/openapi/docs",
            json_errors=False,
        )

        application_container = ApplicationContainer()

        config = application_container.config

        """Security schemes for APIFlask"""
        app.security_schemes = {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
            }
        }

        """SQLAlchemy configuration"""
        app.config.update(
            {
                "SQLALCHEMY_DATABASE_URI": config.SQLALCHEMY_DATABASE_URI(),
                "SQLALCHEMY_TRACK_MODIFICATIONS": config.SQLALCHEMY_TRACK_MODIFICATIONS(),
                "SQLALCHEMY_ECHO": config.SQLALCHEMY_ECHO(),
            }
        )

        database = SQLAlchemy(
            app=app,
            add_models_to_shell=True,
            metadata=Base.metadata,
        )

        migrate = Migrate(app, database)

        """Blueprints"""
        [app.register_blueprint(blueprint) for blueprint in [account, person, login]]

        return app

    @classmethod
    def create(cls) -> APIFlask:
        return cls.build()


app = App.create()
