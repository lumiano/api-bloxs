from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Index, String, UniqueConstraint
from sqlalchemy.orm import relationship

from api_bloxs.base.model import Model


@dataclass
class Person(Model):
    """Person model"""

    __tablename__ = "person"

    name = Column(String(255), nullable=False, doc="Name", comment="Name")
    document = Column(String(14), nullable=False, doc="Document", comment="Document")
    birthday = Column(DateTime, nullable=False, doc="Birthday", comment="Birthday")

    account = relationship(
        "Account", back_populates="person", uselist=False, lazy="subquery"
    )

    __table_args__ = (
        Index("idx_id_person", "id"),
        UniqueConstraint("id", document, name="uq_id_person_document"),
        UniqueConstraint("document", name="uq_person_document"),
    )

    def __repr__(self):
        return f"<Person(id={self.id}, name={self.name}, document={self.document}, birthday={self.birthday})>"
