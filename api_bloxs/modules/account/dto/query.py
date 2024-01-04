from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf, Range

from api_bloxs.modules.account.enum.account_type import AccountTypeEnum
from api_bloxs.modules.account.model.account import Account


class AccountQueryDto(Schema):
    """Account query Dto"""

    page = Integer(
        description="Page number",
        required=False,
        load_default=1,
    )

    offset = Integer(
        description="Number of items per page",
        required=False,
        load_default=50,
        validate=[Range(min=1, max=50)],
    )

    order_by = String(
        description="Order by field",
        required=False,
        load_default="is_active",
        validate=[OneOf(Account.__table__.columns.keys())],
    )

    sort: str = String(
        description="Sort direction",
        required=False,
        load_default="desc",
        validate=[OneOf(["asc", "desc"])],
    )

    document = String(
        description="Document",
        required=False,
        validate=[Length(min=11, max=14)],
    )

    id = Integer(
        description="Account id",
        required=False,
    )

    account_type = String(
        description="Account type",
        required=False,
        validate=[OneOf(AccountTypeEnum.__members__.keys())],
    )
