from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import OneOf, Range

from api_bloxs.modules.transaction.model.transaction import Transaction


class TransactionQueryDto(Schema):
    """Transaction query Dto"""

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
        load_default="transaction_date",
        validate=[OneOf(Transaction.__table__.columns.keys())],
    )

    sort: str = String(
        description="Sort direction",
        required=False,
        load_default="desc",
        validate=[OneOf(["asc", "desc"])],
    )
