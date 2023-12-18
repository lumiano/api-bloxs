from typing import List

from api_bloxs.base.service import Service
from api_bloxs.modules.person.model.person import Person
from api_bloxs.modules.person.repositories.person import PersonRepository


class PersonService(Service):
    """Service for person."""

    def __init__(self, person_repository: PersonRepository):
        self.person_repository = person_repository

        print("PersonService.__init__")

    def get_all(self) -> List[Person]:
        """Get all persons."""
        return self.person_repository.get_all()

    def get_by_id(self, person_id: int) -> Person:
        """Get person by id."""

        return self.person_repository.get_by_id(person_id)

    def create(self, person: Person) -> Person:
        """Create person."""
        return self.person_repository.create(person)

    def update(self, person: Person) -> Person:
        """Update person."""
        return self.person_repository.update(person)

    def delete(self, person_id: int) -> None:
        """Delete person."""
        return self.person_repository.delete(person_id)

    def get_by_document(self, document: str) -> Person:
        """Get person by document."""
        return self.person_repository.get_by_document(document)

    def find_by(self, document: str, name: str, id: int) -> Person:
        """Get person by document or name."""
        return self.person_repository.find_by(document, name, id)
