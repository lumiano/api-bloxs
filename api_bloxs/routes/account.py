import logging
from typing import List
from apiflask import APIBlueprint, HTTPError
from dependency_injector.wiring import Provide, inject
from api_bloxs.modules.account.dto.account import AccountDto
from api_bloxs.modules.account.model.account import Account
from api_bloxs.modules.account.services.account import AccountService
from api_bloxs.shared.application import ApplicationContainer


account_blueprint = APIBlueprint(
    "account",
    __name__,
    tag="Account",
    url_prefix="/account",
)


class AccountController:
    @account_blueprint.get(
        "/<int:account_id>",
    )
    @account_blueprint.doc(
        description="Get account by id",
        operation_id="get_account_by_id",
        security="ApiKeyAuth",
        summary="Get account by id",
        tags=["Account"],
        responses={
            200: {"description": "Account found"},
            404: {"description": "Account not found"},
        },
    )
    @account_blueprint.output(AccountDto)
    @inject
    def get_by_id(
        account_id: int,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account_service
        ],
    ):
        try:
            account = account_service.get_by_id(account_id)

            if account is None:
                raise AccountNotFoundError(account_id)

            return Account(**account)

        except AccountNotFoundError as e:
            logging.info(f"Account not found id: {account_id}")
            raise HTTPError(404, str(e), detail="Account id not found")

        except Exception as e:
            logging.info(f"Internal server error: {e}")
            raise HTTPError(500, str(e), detail="Internal server error")

    @account_blueprint.post("/")
    @account_blueprint.input(
        schema=AccountDto,
        example={
            "account_id": 1,
            "person_id": 1,
            "balance": 1000.0,
            "daily_withdrawal_limit": 1000.0,
            "account_type": "CURRENT_ACCOUNT",
            "is_active": True,
            "creation_date": "2021-08-01T00:00:00",
            "update_date": "2021-08-01T00:00:00",
            "id": 1,
        },
        arg_name="AccountDto",
        schema_name="AccountDto",
    )
    @account_blueprint.doc(
        description="Create account",
        operation_id="create_account",
        responses={
            201: {"description": "Account created"},
            400: {"description": "Bad request"},
        },
        summary="Create account",
        tags=["Account"],
        security="ApiKeyAuth",
    )
    @account_blueprint.output(
        description="Account created",
        schema_name="Account",
        schema=AccountDto,
        example={
            "account_id": 1,
            "person_id": 1,
            "balance": 1000.0,
            "daily_withdrawal_limit": 1000.0,
            "account_type": "CURRENT_ACCOUNT",
            "is_active": True,
            "creation_date": "2021-08-01T00:00:00",
            "update_date": "2021-08-01T00:00:00",
            "id": 1,
        },
        status_code=201,
    )
    @inject
    def create(
        AccountDto: AccountDto,
        account_service: AccountService = Provide[
            ApplicationContainer.services.account_service
        ],
    ):
        try:
            account = Account(**AccountDto)

            account_exists = account_service.find_by_params(
                {"person_id": account.person_id, "account_type": account.account_type}
            )

            if account_exists:
                raise AccountAlreadyExists(account.account_id)

            return account_service.create(account)

        except AccountAlreadyExists as e:
            raise HTTPError(404, str(e), detail="Account already exists")

        except Exception as e:
            raise HTTPError(500, str(e), detail="Internal server error")


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found id: {entity_id}")


class EntityAlreadyExists(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} already exists id: {entity_id}")


class AccountNotFoundError(NotFoundError):
    entity_name = "Account"


class AccountAlreadyExists(EntityAlreadyExists):
    entity_name = "Account"
