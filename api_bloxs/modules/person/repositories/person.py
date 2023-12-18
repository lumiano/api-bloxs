from typing import List

from sqlalchemy import or_

from api_bloxs.base.database import Database
from api_bloxs.base.repository import Repository
from api_bloxs.modules.person.model.person import Person


class PersonRepository(Repository):
    """Person repository"""

    def __init__(self, session: Database):
        self.session = session

    def get_by_id(self, id: int) -> Person:
        """Get by id"""

        with self.session.context() as session:
            return session.query(Person).filter_by(id=id).first()

    def get_all(self) -> List[Person]:
        """Get all"""
        with self.session.context() as session:
            return session.query(Person).all()

    def create(self, person: Person) -> Person:
        """Create"""
        with self.session.context() as session:
            session.add(person)

            session.commit()
            return self.get_by_id(person.id)

    def update(self, id: int, person: Person) -> Person:
        """Update"""
        pass

    def delete(self, id: int) -> None:
        """Delete"""
        with self.session.context() as session:
            person = session.query(Person).filter_by(id=id).first()
            session.delete(person)

            session.commit()

    def get_by_document(self, document: str) -> Person:
        """Get person by document"""
        with self.session.context() as session:
            return session.query(Person).filter_by(document=document).first()

    def find_by(self, document: str, name: str, id: int) -> Person:
        """Get person by document or name"""
        with self.session.context() as session:
            return (
                session.query(Person)
                .filter(
                    or_(
                        Person.document == document,
                        Person.name == name,
                        Person.id == id,
                    )
                )
                .first()
            )
