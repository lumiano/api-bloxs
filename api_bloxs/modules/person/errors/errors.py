from apiflask import HTTPError


class PersonNotFoundError(HTTPError):
    """Person not found"""

    status_code = 400
    message = "Person not found"
    detail = "Person not found"


class PersonNotActive(HTTPError):
    """Person not active"""

    status_code = 400
    message = "Person not active"
    detail = "Person not active"


class PersonAlreadyExists(HTTPError):
    """Person already exists"""

    status_code = 400
    message = "Person already exists"
    detail = "Person has already been created"
