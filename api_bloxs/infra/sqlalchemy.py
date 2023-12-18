from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy

from api_bloxs.base.model import Base
from api_bloxs.shared.application import ApplicationContainer


class SQLAlchemyConfig:

    """SQLAlchemyConfig class"""

    @classmethod
    def build(cls, app: APIFlask, container: ApplicationContainer) -> None:
        app.config.update(
            {
                "SQLALCHEMY_DATABASE_URI": container.config.SQLALCHEMY_DATABASE_URI(),
                "SQLALCHEMY_TRACK_MODIFICATIONS": container.config.SQLALCHEMY_TRACK_MODIFICATIONS(),
                "SQLALCHEMY_ECHO": container.config.SQLALCHEMY_ECHO(),
            }
        )

        return cls._db(app)

    @classmethod
    def _db(cls, app: APIFlask) -> SQLAlchemy:
        return SQLAlchemy(
            app=app,
            add_models_to_shell=True,
            metadata=Base.metadata,
        )
