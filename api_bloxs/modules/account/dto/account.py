from apiflask import Schema
from apiflask.fields import Boolean, DateTime, Decimal, Enum, Integer
from apiflask.validators import Range

from api_bloxs.modules.account.enum.account_type import AccountTypeEnum


class AccountDto(Schema):
    """Account DTO."""

    id = Integer(required=False, validate=Range(min=1))

    person_id = Integer(required=True, validate=Range(min=1))
    balance = Decimal(
        required=True, validate=Range(min=0), allow_nan=False, as_string=True
    )
    daily_withdrawal_limit = Decimal(required=True, validate=Range(min=0))
    is_active = Boolean(required=True, default=True)
    account_type = Enum(AccountTypeEnum, required=True)
    creation_date = DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
    update_date = DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
