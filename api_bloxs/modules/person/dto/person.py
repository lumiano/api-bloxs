from apiflask import Schema
from apiflask.fields import Boolean, Date, DateTime, Integer, String
from apiflask.validators import Length


class PersonDto(Schema):
    """Person DTO"""

    id = Integer(
        required=False,
        description="Person ID",
        example=1,
    )
    name = String(
        required=True,
        description="Name",
        example="John Doe",
        validate=[
            Length(min=7, max=100),
        ],
    )

    document = String(
        required=True,
        description="Document",
        example="12345678901",
        validate=[Length(min=11, max=14)],
    )

    birthday = Date(
        required=True,
        description="Birthday",
        example="1990-01-01:00:00:00",
        format="%Y-%m-%dT%H:%M:%S",
    )

    is_active = Boolean(
        required=False,
        description="Is active",
        example=True,
    )

    creation_date = DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
    update_date = DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
