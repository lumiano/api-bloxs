from apiflask import APIBlueprint, HTTPTokenAuth

from api_bloxs.shared.application import ApplicationContainer

api = APIBlueprint("auth", __name__, url_prefix="/auth")


auth = HTTPTokenAuth(
    description="API Key Authentication",
    scheme="ApiKeyAuth",
    realm="Access to the API requires an API Key",
    header="X-API-Key",
    security_scheme_name="ApiKeyAuth",
)


class AuthController:
    @auth.verify_token
    def verify_token(
        token,
    ):
        container = ApplicationContainer()

        config = container.config

        return token == config.API_KEY()

    @api.post(
        "/login",
    )
    @auth.login_required
    @api.doc(
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

    @api.post(
        "/logout",
    )
    @api.doc(
        description="Logout",
        operation_id="logout",
        responses={
            200: {"description": "Logged out"},
            401: {"description": "Unauthorized"},
        },
        summary="Logout",
        tags=["Auth"],
    )
    def logout():
        return {"message": "Logged out"}

    @api.get(
        "/protected",
    )
    @api.doc(
        description="Protected",
        operation_id="protected",
        responses={
            200: {"description": "Protected"},
            401: {"description": "Unauthorized"},
        },
        security="ApiKeyAuth",
        summary="Protected",
        tags=["Auth"],
    )
    @auth.login_required
    def protected():
        return {"message": "Protected"}
