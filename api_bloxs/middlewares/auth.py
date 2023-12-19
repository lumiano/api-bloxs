from apiflask import HTTPTokenAuth

auth = HTTPTokenAuth(
    description="API Key Authentication",
    scheme="ApiKeyAuth",
    realm="Access to the API requires an API Key",
    header="X-API-Key",
    security_scheme_name="ApiKeyAuth",
)
