from apiflask import Schema, fields
from apiflask.validators import Range


class DepositDto(Schema):
    """Deposit Dto"""

    amount = fields.Number(
        required=True,
        description="Amount",
        example=1000.0,
        validate=Range(min=0),
    )
