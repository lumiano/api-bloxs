from apiflask import HTTPError


class InternalServerError(HTTPError):
    status_code = 500
    message = "Internal server error"
    detail = "Internal server error"
