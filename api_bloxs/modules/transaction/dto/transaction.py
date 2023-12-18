from apiflask import Schema
from apiflask.fields import DateTime, Integer, Number
from apiflask.validators import Range


class TransactionDto(Schema):
    """Transaction Dto"""

    id = Integer(
        required=False,
        validate=Range(min=1),
        description="Transaction id",
        example=1,
    )
    account_id: Integer(
        required=True,
        description="Account id",
        example=1,
    )
    amount: Number(
        required=True,
        description="Amount",
        example=1000.0,
        validate=Range(min=0),
    )
    transaction_date: DateTime(
        required=True,
        description="Transaction date",
        example="2021-08-01T00:00:00",
        format="%Y-%m-%dT%H:%M:%S",
    )
    creation_date = DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
    update_date = DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
