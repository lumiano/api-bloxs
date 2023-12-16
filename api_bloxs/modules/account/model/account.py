from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Enum,
    Index,
    UniqueConstraint,
)
from api_bloxs.base.model import Model
from sqlalchemy.orm import relationship


from api_bloxs.modules.account.enum.account_type import AccountTypeEnum


class Account(Model):
    """Account model"""

    __tablename__ = "account"

    account_id = Column(Integer, nullable=False, doc="Account ID", comment="Account ID")
    person_id = Column(Integer, nullable=False, doc="Person ID", comment="Person ID")
    balance = Column(
        Numeric(precision=10, scale=2), nullable=False, doc="Balance", comment="Balance"
    )
    daily_withdrawal_limit = Column(
        Numeric(precision=10, scale=2),
        nullable=False,
        doc="Daily withdrawal limit",
        comment="Daily withdrawal limit",
    )

    account_type = Column(
        Enum(AccountTypeEnum),
        nullable=False,
        doc="Account type",
        comment="Account type",
    )

    # person = relationship("Person", back_populates="account")

    Index(
        "idx_person_id",
        person_id,
    )

    UniqueConstraint("account_id", "account_type", name="uq_account_id_account_type")

    Index(
        "idx_account_id_account_type",
        account_id,
        account_type,
    )

    def __repr__(self) -> str:
        return f"<Account(account_id={self.account_id}, person_id={self.person_id}, balance={self.balance}, id={self.id}, daily_withdrawal_limit={self.daily_withdrawal_limit}, is_active={self.is_active}, account_type={self.account_type}, creation_date={self.creation_date})>"
