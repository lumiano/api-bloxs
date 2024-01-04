from apiflask import PaginationSchema, Schema
from apiflask.fields import Integer, List, Nested, String


class TransactionsPagination(Schema):
    id = Integer()
    account_id = Integer()
    amount = Integer()
    transaction_date = String()
    creation_date = String()
    update_date = String()


class TransactionsPagination(Schema):
    """Transactions pagination schema."""

    items = List(Nested(TransactionsPagination))

    pagination = Nested(PaginationSchema)
