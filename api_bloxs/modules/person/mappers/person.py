from apiflask import Schema
from apiflask.fields import Boolean, Date, DateTime, Integer, String


class PersonMapper(Schema):
    """Person Mapper"""

    id = Integer()
    name = String()
    document = String()
    birthday = Date()
    is_active = Boolean()
    creation_date = DateTime()
    update_date = DateTime()
