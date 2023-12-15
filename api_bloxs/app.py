"""Aplication Module."""

from apiflask import APIFlask

from api_bloxs.routes.account import AccountBlueprint
from api_bloxs.shared.containers import Container


def create_app() -> APIFlask:
    container = Container()

    app = APIFlask(
        __name__,
        docs_path="/openapi/docs",
    )

    app.container = container

    app.register_blueprint(AccountBlueprint)

    return app
