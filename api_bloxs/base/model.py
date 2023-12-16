from sqlalchemy import Boolean, Column, DateTime, Integer, func


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listens_for

Base = declarative_base()


class Model(Base):
    """Base model class."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, doc="ID", comment="ID")

    creation_date = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        doc="Creation date",
        comment="Creation date",
    )
    update_date = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Update date",
        comment="Update date",
    )

    is_active = Column(
        Boolean, nullable=False, doc="Active flag", comment="Active flag"
    )


@listens_for(Model, "before_update", propagate=True)
def before_insert(mapper, connection, target: Model):
    target.update_date = func.now()
