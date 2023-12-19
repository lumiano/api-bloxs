from trace import Trace

from apiflask import APIBlueprint, HTTPError
from dependency_injector.wiring import Provide, inject

from api_bloxs.middlewares.auth import auth
from api_bloxs.modules.person.dto.person import PersonDto
from api_bloxs.modules.person.errors.errors import PersonAlreadyExists
from api_bloxs.modules.person.model.person import Person
from api_bloxs.modules.person.services.person import PersonService
from api_bloxs.shared.application import ApplicationContainer

person = APIBlueprint(
    "person",
    __name__,
    tag="Person",
    url_prefix="/person",
)


class PersonController:
    @person.post("/")
    @person.input(
        schema=PersonDto,
        arg_name="PersonDto",
        examples={
            "PersonDto": {
                "value": {
                    "id": 1,
                    "creation_date": "2021-01-01T00:00:00",
                    "update_date": "2021-01-01T00:00:00",
                    "name": "John Doe",
                    "document": "12345678901",
                    "birthday": "2021-01-01T00:00:00",
                    "is_active": True,
                }
            }
        },
    )
    @person.doc(
        security="ApiKeyAuth",
        description="Create person",
        operation_id="create_person",
        responses={
            200: {"description": "Person created"},
            400: {"description": "Invalid birthday"},
            400: {"description": "Person already exists"},
        },
        summary="Create person",
        tags=["Person"],
    )
    @person.output(
        schema=PersonDto,
        status_code=200,
        content_type="application/json",
        description="Person created",
        examples={
            "PersonDto": {
                "value": {
                    "id": 1,
                    "creation_date": "2021-01-01T00:00:00",
                    "update_date": "2021-01-01T00:00:00",
                    "name": "John Doe",
                    "document": "12345678901",
                    "birthday": "2021-01-01T00:00:00",
                    "is_active": True,
                }
            }
        },
    )
    @auth.login_required
    @inject
    def create_person(
        PersonDto: PersonDto,
        person_service: PersonService = Provide[ApplicationContainer.services.person],
        trace: Trace = Provide[ApplicationContainer.infra.trace],
    ):
        try:
            person = Person(**PersonDto)

            person_exists = person_service.find_by(
                document=person.document, name=person.name, id=person.id
            )

            if person_exists:
                raise PersonAlreadyExists()

            person_created = person_service.create(person)

            return person_created
        except HTTPError as e:
            trace.logger.error(
                f"[{e.status_code} - {e.__class__.__name__}] - {e.message} {e.detail} - {e.__traceback__}"
            )

            raise e

        except Exception as e:
            trace.logger.error(f"[{e.__class__.__name__}] - {e.__traceback__}")

            raise e
