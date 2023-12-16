from apiflask import Schema, fields


class PersonDto(Schema):
    id_person = fields.Integer(
        required=False,
        description="Person ID",
        example=1,
    )
    name = fields.String(
        required=True,
        description="Name",
        example="John Doe",
    )

    document = fields.String(
        required=True,
        description="Document",
        example="12345678901",
    )

    birthday = fields.Date(
        required=True,
        description="Birthday",
        example="1990-01-01",
    )

    creation_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
    update_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=False)
