from apiflask import Schema, fields
from apiflask.validators import Range

from api_bloxs.modules.account.enum.account_type import AccountTypeEnum


class AccountDto(Schema):
    """Account DTO."""

    id = fields.Integer(required=False, validate=Range(min=1))

    person_id = fields.Integer(required=True, validate=Range(min=1))
    balance = fields.Decimal(
        required=True, validate=Range(min=0), allow_nan=False, as_string=True
    )
    daily_withdrawal_limit = fields.Decimal(required=True, validate=Range(min=0))
    is_active = fields.Boolean(required=True)
    account_type = fields.Enum(AccountTypeEnum, required=True)
    creation_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
    update_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
