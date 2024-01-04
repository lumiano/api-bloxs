from apiflask import PaginationSchema, Schema
from apiflask.fields import Boolean, Enum, Integer, List, Nested, String

from api_bloxs.modules.account.enum.account_type import AccountTypeEnum
from api_bloxs.modules.person.dto.person import PersonDto


class AccountPagination(Schema):
    """Account pagination schema."""

    id = Integer()
    balance = String()
    daily_withdrawal_limit = String()
    account_type = Enum(AccountTypeEnum)
    person_id = Integer()
    creation_date = String()
    update_date = String()
    is_active = Boolean()
    person = Nested(PersonDto)


class AccountPagination(Schema):
    """Account pagination schema."""

    items = List(Nested(AccountPagination))

    pagination = Nested(PaginationSchema)
