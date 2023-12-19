from apiflask import APIBlueprint, HTTPTokenAuth

from api_bloxs.middlewares.auth import auth
from api_bloxs.shared.application import ApplicationContainer

login = APIBlueprint("auth", __name__, url_prefix="/auth")


class AuthController:
    @auth.verify_token
    def verify_token(
        token,
    ):
        container = ApplicationContainer()

        config = container.config

        return token == config.API_KEY()

    @login.post(
        "/login",
    )
    @auth.login_required
    @login.doc(
        description="Login",
        operation_id="login",
        responses={
            200: {"description": "Logged in"},
            401: {"description": "Unauthorized"},
        },
        summary="Login",
        tags=["Auth"],
        security="ApiKeyAuth",
    )
    def login():
        container = ApplicationContainer()

        config = container.config

        return {"message": "Logged in", "api_key": config.API_KEY()}
