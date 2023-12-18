from apiflask import Schema, fields, validators


class TransactionDto(Schema):
    """Transaction Dto"""

    id = fields.Integer(
        required=False,
        validate=validators.Range(min=1),
        description="Transaction id",
        example=1,
    )

    account_id: fields.Integer(
        required=True,
        description="Account id",
        example=1,
    )
    amount: fields.Number(
        required=True,
        description="Amount",
        example=1000.0,
        validate=validators.Range(min=0),
    )

    transaction_date: fields.DateTime(
        required=True,
        description="Transaction date",
        example="2021-08-01T00:00:00",
        format="%Y-%m-%dT%H:%M:%S",
    )

    creation_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
    update_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
