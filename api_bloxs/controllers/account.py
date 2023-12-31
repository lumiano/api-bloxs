from datetime import datetime
from decimal import Decimal

from apiflask import APIBlueprint, HTTPError
from dependency_injector.wiring import Provide, inject

from api_bloxs.infra.errors import InternalServerError
from api_bloxs.infra.trace import Trace
from api_bloxs.middlewares.auth import auth
from api_bloxs.modules.account.dto.account import AccountDto
from api_bloxs.modules.account.dto.query import AccountQueryDto
from api_bloxs.modules.account.enum.account_type import AccountTypeEnum
from api_bloxs.modules.account.errors.errors import (
    AccountBalanceError, AccountDailyWithdrawalLimitError, AccountDeactivated,
    AccountNotFound, AccountTypePerson)
from api_bloxs.modules.account.mappers.account_person import \
    AccountPersonMapper
from api_bloxs.modules.account.mappers.pagination import AccountPagination
from api_bloxs.modules.account.model.account import Account
from api_bloxs.modules.account.services.account import AccountService
from api_bloxs.modules.deposit.model.deposit import DepositDto
from api_bloxs.modules.person.errors.errors import (PersonNotActive,
                                                    PersonNotFoundError)
from api_bloxs.modules.person.services.person import PersonService
from api_bloxs.modules.transaction.dto.query import TransactionQueryDto
from api_bloxs.modules.transaction.mappers.pagination import \
    TransactionsPagination
from api_bloxs.modules.transaction.model.transaction import Transaction
from api_bloxs.modules.transaction.services.transaction import \
    TransactionService
from api_bloxs.modules.withdraw.dto.withdraw import WithdrawDto
from api_bloxs.shared.application import ApplicationContainer

account = APIBlueprint(
    "account",
    __name__,
    tag="Account",
    url_prefix="/account",
)


class AccountController:
    @account.get("/")
    @account.doc(
        security="ApiKeyAuth",
        description="Get all accounts",
        operation_id="get_all_accounts",
        responses={
            200: {"description": "Accounts found"},
            500: {"description": "Internal server error"},
        },
        summary="Get all accounts",
        tags=["Account"],
    )
    @account.input(
        location="query",
        arg_name="AccountQueryDto",
        schema_name="AccountQueryDto",
        schema=AccountQueryDto,
        example={
            "page": 1,
            "offset": 10,
            "order_by": "id",
            "sort": "desc",
            "id": 1,
            "document": "12345678900",
            "account_type": "CURRENT_ACCOUNT",
        },
    )
    @account.output(
        description="Accounts found",
        schema_name="AccountsPagination",
        schema=AccountPagination,
        example={
            "items": [
                {
                    "id": 1,
                    "person_id": 1,
                    "balance": 1000.0,
                    "daily_withdrawal_limit": 1000.0,
                    "account_type": "CURRENT_ACCOUNT",
                    "is_active": True,
                    "creation_date": "2021-08-01T00:00:00",
                    "update_date": "2021-08-01T00:00:00",
                    "person": {
                        "id": 1,
                        "name": "John Doe",
                        "document": "12345678900",
                        "is_active": True,
                        "creation_date": "2021-08-01T00:00:00",
                        "update_date": "2021-08-01T00:00:00",
                        "birthday": "1990-01-01T00:00:00",
                    },
                }
            ],
            "pagination": {
                "page": 1,
                "offset": 10,
                "total": 1,
            },
        },
    )
    @auth.login_required
    @inject
    def get_all(
        AccountQueryDto: AccountQueryDto,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ) -> TransactionsPagination:
        try:
            q = {k: v for k, v in AccountQueryDto.items() if v is not None}

            accounts = account_service.get_all(q)

            return {
                "items": accounts,
                "pagination": {
                    "page": q["page"],
                    "per_page": q["offset"],
                    "total": len(accounts),
                },
            }

        except HTTPError as e:
            print(e)
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")

            raise InternalServerError()

    @account.get(
        "/<int:account_id>",
    )
    @account.doc(
        description="Get account by id",
        operation_id="get_account_by_id",
        responses={
            200: {"description": "Account found"},
            404: {"description": "Account not found"},
            500: {"description": "Internal server error"},
        },
        summary="Get account by id",
        tags=["Account"],
        security="ApiKeyAuth",
    )
    @account.output(
        description="Account found",
        schema_name="Account",
        schema=AccountDto,
        links={
            "self": {
                "operationId": "get_account_by_id",
                "parameters": {"account_id": "$response.body#/id"},
            }
        },
    )
    @auth.login_required
    @inject
    def get_by_id(
        account_id: int,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ):
        try:
            account = account_service.get_by_id(account_id)

            if account is None:
                raise AccountNotFound()

            if account.is_active is False:
                raise AccountDeactivated()

            return account

        except HTTPError as e:
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")

            raise InternalServerError()

    @account.post("/")
    @account.input(
        schema=AccountDto,
        example={
            "person_id": 1,
            "balance": 1000.0,
            "daily_withdrawal_limit": 1000.0,
            "account_type": "CURRENT_ACCOUNT",
            "is_active": True,
            "creation_date": "2021-08-01T00:00:00",
            "update_date": "2021-08-01T00:00:00",
        },
        arg_name="AccountDto",
        schema_name="AccountDto",
    )
    @account.doc(
        description="Create account",
        operation_id="create_account",
        responses={
            201: {"description": "Account created"},
            400: {"description": "Invalid account type"},
            400: {"description": "Invalid balance"},
            400: {"description": "Invalid daily withdrawal limit"},
            400: {"description": "Person not found"},
            400: {"description": "Person not active"},
            400: {"description": "Account already exists"},
            500: {"description": "Internal server error"},
        },
        summary="Create account",
        tags=["Account"],
        security="ApiKeyAuth",
    )
    @account.output(
        description="Account created",
        schema_name="AccountPersonMapper",
        schema=AccountPersonMapper,
        links={
            "self": {
                "operationId": "create_account",
                "parameters": {"account_id": "$response.body#/id"},
            },
        },
        example={
            "id": 1,
            "person_id": 1,
            "balance": 1000.0,
            "daily_withdrawal_limit": 1000.0,
            "account_type": "CURRENT_ACCOUNT",
            "is_active": True,
            "creation_date": "2021-08-01T00:00:00",
            "update_date": "2021-08-01T00:00:00",
            "person": {
                "id": 1,
                "name": "John Doe",
                "document": "12345678900",
                "is_active": True,
                "creation_date": "2021-08-01T00:00:00",
                "update_date": "2021-08-01T00:00:00",
                "birthday": "1990-01-01T00:00:00",
            },
        },
    )
    @auth.login_required
    @inject
    def create(
        AccountDto: AccountDto,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        person_service: PersonService = Provide[ApplicationContainer.services.person],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ):
        try:
            account = Account(**AccountDto)

            if account.balance < 0:
                raise AccountBalanceError()

            if account.account_type not in AccountTypeEnum:
                raise AccountTypePerson()

            account_type_person = account_service.get_by_type_and_person_id(
                account.account_type, account.person_id
            )

            if account_type_person is not None:
                raise AccountTypePerson()

            person = person_service.get_by_id(account.person_id)

            if person is None:
                raise PersonNotFoundError()

            if person.is_active is False:
                raise PersonNotActive()

            account = account_service.create(account)

            return {
                "id": account.id,
                "person_id": account.person_id,
                "balance": account.balance,
                "daily_withdrawal_limit": account.daily_withdrawal_limit,
                "account_type": account.account_type,
                "is_active": account.is_active,
                "creation_date": account.creation_date,
                "update_date": account.update_date,
                "person": {
                    "id": person.id,
                    "name": person.name,
                    "document": person.document,
                    "is_active": person.is_active,
                    "creation_date": person.creation_date,
                    "update_date": person.update_date,
                    "birthday": person.birthday,
                },
            }

        except HTTPError as e:
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            print(e)
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")

            raise InternalServerError()

    @account.post("/<int:account_id>/deposit")
    @account.doc(
        security="ApiKeyAuth",
        description="Deposit",
        operation_id="deposit",
        responses={
            200: {"description": "Deposit"},
            401: {"description": "Unauthorized"},
            404: {"description": "Account not found"},
            500: {"description": "Internal server error"},
        },
        summary="Deposit",
        tags=["Account"],
    )
    @account.input(
        schema_name="DepositDto",
        schema=DepositDto,
        example={
            "amount": 1000.0,
        },
        examples={
            "DepositDto": {
                "value": {
                    "amount": 1000.0,
                },
                "summary": "Deposit",
            }
        },
        arg_name="deposit_dto",
    )
    @account.output(
        example={
            "balance": 1000.0,
        },
        examples={
            "DepositDto": {
                "value": {
                    "balance": 1000.0,
                },
                "summary": "Deposit",
            }
        },
        schema_name="DepositDto",
        schema=DepositDto,
    )
    @inject
    @auth.login_required
    def deposit(
        account_id: int,
        deposit_dto: DepositDto,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
        transaction_service: TransactionService = Provide[
            ApplicationContainer.services.transaction
        ],
    ):
        try:
            account = account_service.get_by_id(account_id)

            if account is None:
                raise AccountNotFound()

            if account.is_active is False:
                raise AccountDeactivated()

            amount = deposit_dto["amount"]

            account.balance += Decimal(str(amount))

            account_service.update(account)

            transaction = Transaction(
                is_active=True,
                account_id=account_id,
                amount=amount,
                transaction_date=datetime.now(),
            )

            transaction_created = transaction_service.create(transaction)

            return transaction_created
        except AccountNotFound as e:
            trace.logger.error(e)
            raise e

        except Exception as e:
            trace.logger.error(e)
            raise e

    @account.post("/<int:account_id>/withdraw")
    @account.doc(
        description="Withdraw",
        operation_id="withdraw",
        responses={
            200: {"description": "Withdraw"},
            401: {"description": "Unauthorized"},
            404: {"description": "Account not found"},
            500: {"description": "Internal server error"},
        },
        summary="Withdraw",
        tags=["Account"],
        security="ApiKeyAuth",
    )
    @account.input(
        schema_name="WithdrawDto",
        schema=WithdrawDto,
        example={
            "amount": 1000.0,
        },
        examples={
            "WithdrawDto": {
                "value": {
                    "amount": 1000.0,
                },
                "summary": "Withdraw",
            }
        },
        arg_name="WithdrawDto",
    )
    @account.output(
        example={
            "balance": 1000.0,
        },
        examples={
            "WithdrawDto": {
                "value": {
                    "balance": 1000.0,
                },
                "summary": "Withdraw",
            }
        },
        schema_name="WithdrawDto",
        schema=WithdrawDto,
        links={
            "self": {
                "operationId": "withdraw",
                "parameters": {"account_id": "$response.body#/id"},
            }
        },
        description="Withdraw",
    )
    @auth.login_required
    @inject
    def withdraw(
        WithdrawDto: WithdrawDto,
        account_id: int,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        transaction_service: TransactionService = Provide[
            ApplicationContainer.services.transaction
        ],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ):
        try:
            account = account_service.get_by_id(account_id)

            if account.is_active is False:
                raise AccountDeactivated()

            if account is None:
                raise AccountNotFound()

            amount = WithdrawDto["amount"]

            amount = Decimal(str(amount))

            if account.balance < amount:
                raise AccountBalanceError()

            if account.daily_withdrawal_limit < amount:
                raise AccountDailyWithdrawalLimitError()

            account.balance -= amount

            account_service.update(account)

            transaction = Transaction(
                is_active=True,
                account_id=account_id,
                amount=amount,
                transaction_date=datetime.now(),
            )

            transaction_created = transaction_service.create(transaction)

            return transaction_created

        except HTTPError as e:
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")
            raise e

    @account.post("/<int:account_id>/freezed")
    @account.doc(
        description="Account freezed",
        operation_id="freezed",
        responses={
            200: {"description": "Freezed"},
            401: {"description": "Unauthorized"},
            404: {"description": "Account not found"},
            500: {"description": "Internal server error"},
        },
        summary="Account freezed, you can't deposit or withdraw",
        tags=["Account"],
        security="ApiKeyAuth",
    )
    @account.output(
        examples={
            "AccountDto": {
                "value": {
                    "is_active": False,
                },
                "summary": "Freezed",
            }
        },
        schema_name="AccountDto",
        schema=AccountDto,
        links={
            "self": {
                "operationId": "freezed",
                "parameters": {"account_id": "$response.body#/id"},
            }
        },
        description="Freezed",
    )
    @auth.login_required
    @inject
    def freezed(
        account_id: int,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ):
        try:
            account = account_service.get_by_id(account_id)

            if account is None:
                raise AccountNotFound()

            if account.is_active is False:
                raise AccountDeactivated()

            account.is_active = False

            account_service.update(account)

            return account

        except HTTPError as e:
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")
            raise e

    @account.get("/<int:account_id>/transaction")
    @account.doc(
        description="Get transactions by account id",
        operation_id="transactions",
        responses={
            200: {"description": "Transactions"},
            401: {"description": "Unauthorized"},
            404: {"description": "Account not found"},
            500: {"description": "Internal server error"},
        },
        summary="Get transactions by account id",
        tags=["Account"],
        security="ApiKeyAuth",
    )
    @account.input(
        location="query",
        arg_name="TransactionQueryDto",
        schema_name="TransactionQueryDto",
        schema=TransactionQueryDto,
        example={
            "page": 1,
            "offset": 10,
            "order_by": "transaction_date",
            "sort": "desc",
        },
    )
    @account.output(
        description="Transactions",
        schema_name="TransactionsPagination",
        schema=TransactionsPagination,
        example={
            "items": [
                {
                    "id": 1,
                    "account_id": 1,
                    "amount": 1000.0,
                    "transaction_date": "2021-08-01T00:00:00",
                    "is_active": True,
                    "creation_date": "2021-08-01T00:00:00",
                    "update_date": "2021-08-01T00:00:00",
                }
            ],
            "pagination": {
                "page": 1,
                "offset": 10,
                "total": 1,
            },
        },
    )
    @inject
    def transactions(
        account_id: int,
        TransactionQueryDto: TransactionQueryDto,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account
        ],
        transaction_service: TransactionService = Provide[
            ApplicationContainer.services.transaction
        ],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ) -> TransactionsPagination:
        try:
            account = account_service.get_by_id(account_id)

            if account is None:
                raise AccountNotFound()

            if account.is_active is False:
                raise AccountDeactivated()

            transactions = transaction_service.get_all_by_account_id(
                query={
                    "account_id": account_id,
                    "page": TransactionQueryDto["page"],
                    "offset": TransactionQueryDto["offset"],
                    "order_by": TransactionQueryDto["order_by"],
                    "sort": TransactionQueryDto["sort"],
                },
            )

            return {
                "items": transactions,
                "pagination": {
                    "page": TransactionQueryDto["page"],
                    "per_page": TransactionQueryDto["offset"],
                    "total": len(transactions),
                },
            }

        except HTTPError as e:
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")
            raise e
