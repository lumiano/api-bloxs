from sqlalchemy import (Column, DateTime, Index, Integer, String,
                        UniqueConstraint)

from api_bloxs.base.model import Model


class Person(Model):
    """Person model"""

    __tablename__ = "person"

    id_person = Column(
        Integer,
        nullable=False,
        doc="Person ID",
        comment="Person ID",
        autoincrement=True,
    )

    name = Column(
        String(255),
        nullable=False,
        doc="Name",
        comment="Name",
    )

    document = Column(
        String(14),
        nullable=False,
        doc="Document",
        comment="Document",
    )

    # account_id = Column(Integer, ForeignKey("accounts.id"), unique=True)

    birthday = Column(DateTime, nullable=False, doc="Birthday", comment="Birthday")
    #  account = relationship("Account", back_populates="person", uselist=False)

    Index("idx_id_person", id_person)

    UniqueConstraint("id_person", "document", name="uq_id_person_document")

    def __repr__(self) -> str:
        return f"<Person(id_person={self.id_person}, name={self.name}, document={self.document}, id={self.id}, birthday={self.birthday}, is_active={self.is_active}, creation_date={self.creation_date})>"
