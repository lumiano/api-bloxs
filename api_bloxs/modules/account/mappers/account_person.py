from apiflask import Schema
from apiflask.fields import Boolean, Enum, Integer, Nested, String

from api_bloxs.modules.account.enum.account_type import AccountTypeEnum
from api_bloxs.modules.person.mappers.person import PersonMapper


class AccountPersonMapper(Schema):
    """Account Person Mapper"""

    person = Nested(PersonMapper)


class AccountPersonMapper(Schema):
    """Account Person Mapper"""

    id = Integer()
    balance = String()
    daily_withdrawal_limit = String()
    account_type = Enum(AccountTypeEnum)
    person_id = Integer()
    creation_date = String()
    update_date = String()
    is_active = Boolean()

    person = Nested(PersonMapper)
