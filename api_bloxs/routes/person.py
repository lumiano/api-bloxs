from apiflask import APIBlueprint
from dependency_injector.wiring import inject

from api_bloxs.modules.person.dto.person import PersonDto
from api_bloxs.modules.person.model.person import Person

person_blueprint = APIBlueprint(
    "person",
    __name__,
    tag="Person",
    url_prefix="/person",
)


class PersonController:
    @person_blueprint.post("/")
    @person_blueprint.input(
        schema=PersonDto,
        arg_name="PersonDto",
        examples={
            "PersonDto": {
                "value": {
                    "id_person": 1,
                    "creation_date": "2021-01-01T00:00:00",
                    "update_date": "2021-01-01T00:00:00",
                    "name": "John Doe",
                    "document": "12345678901",
                    "birthday": "1990-01-01",
                }
            }
        },
    )
    @person_blueprint.doc(
        description="Create person",
        operation_id="create_person",
        responses={
            201: {"description": "Person created"},
            400: {"description": "Invalid data"},
        },
        summary="Create person",
        tags=["Person"],
    )
    @inject
    def create_person(PersonDto: PersonDto):
        person = Person(**PersonDto)

        print(person)

        return {"status": "ok"}
