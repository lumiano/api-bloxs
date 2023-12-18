from apiflask import HTTPError


class AccountTypePerson(HTTPError):
    """Account type person"""

    status_code = 403
    message = "Forbidden"
    detail = "You already have an account of this type"


class AccountTypeError(HTTPError):
    """Account type error"""

    status_code = 400
    message = "Invalid account type"
    detail = "Invalid account type"


class AccountAlreadyExists(HTTPError):
    """Account already exists"""

    status_code = 400
    message = "Account already exists"
    detail = "Person already has an account"


class AccountDeactivated(HTTPError):
    """Account deactivated"""

    status_code = 400
    message = "Account deactivated"
    detail = "Account deactivated, please contact your manager"


class AccountNotFound(HTTPError):
    """Account not found"""

    status_code = 404
    message = "Account not found"
    detail = "Account with this id not found"


class AccountBalanceError(HTTPError):
    """Account balance error"""

    status_code = 400
    message = "Balance not sufficient"
    detail = "Balance not sufficient, please check your balance"


class AccountDailyWithdrawalLimitError(HTTPError):
    """Account daily withdrawal limit error"""

    status_code = 400
    message = "Daily withdrawal limit reached"
    detail = "Daily withdrawal limit reached, please check your daily withdrawal limit"
