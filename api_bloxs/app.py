from apiflask import APIFlask
from flask_migrate import Migrate

from api_bloxs.infra.sqlalchemy import SQLAlchemyConfig
from api_bloxs.settings import Blueprints, SecuritySchemes
from api_bloxs.shared.application import ApplicationContainer

container = ApplicationContainer()


app = APIFlask(
    __name__,
    title="API Bloxs",
    version="1.0.0",
    docs_path="/openapi/docs",
    json_errors=False,
)


app.security_schemes = SecuritySchemes.build()

db = SQLAlchemyConfig.build(app, container)


migrate = Migrate(app, db)

blueprints = Blueprints.build(app)
