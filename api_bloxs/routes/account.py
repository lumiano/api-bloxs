from apiflask import APIBlueprint
from dependency_injector.wiring import Provide, inject

from api_bloxs.modules.account.model.account import Account
from api_bloxs.modules.account.service.account import AccountService
from api_bloxs.shared.containers import Container

AccountBlueprint = APIBlueprint("account", __name__)


class AccountController:
    @AccountBlueprint.get(
        "/accounts/<int:account_id>",
    )
    @AccountBlueprint.doc(
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
    @inject
    def get_by_id(
        account_id: int,
        account_service: AccountService = Provide[Container.account_service],
    ):
        try:
            account = account_service.get_by_id(account_id)

            return Account(**account)
        except Exception as e:
            return str(e)
