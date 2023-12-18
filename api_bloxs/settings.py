from glob import glob
from importlib import import_module
from os.path import basename, isfile, join
from pathlib import Path

from apiflask import APIFlask


class ApiKeyAuth:
    """ApiKeyAuth for APIFlask"""

    schema = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
        }
    }


class SecuritySchemes:
    """Security schemes for APIFlask"""

    @classmethod
    def build(
        cls,
    ) -> None:
        return ApiKeyAuth.schema


class Blueprints:
    """Blueprints class"""

    def __init__(self):
        pass

    def register(self, app: APIFlask) -> None:
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
            app.register_blueprint(blueprint)

    @classmethod
    def build(cls, app: APIFlask) -> None:
        cls().register(app)
