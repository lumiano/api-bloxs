from sqlalchemy import (CheckConstraint, Column, Enum, ForeignKey, Index,
                        Integer, Numeric, UniqueConstraint)
from sqlalchemy.orm import relationship

from api_bloxs.base.model import Model
from api_bloxs.modules.account.enum.account_type import AccountTypeEnum


class Account(Model):
    """Account model"""

    __tablename__ = "account"

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

    person_id = Column(
        Integer,
        ForeignKey(
            "person.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
            name="fk_person_id",
        ),
        nullable=False,
        doc="Person ID",
        comment="Person ID",
    )

    person = relationship(
        "Person",
        back_populates="account",
    )

    transactions = relationship("Transaction", back_populates="account")

    __table_args__ = (
        Index("idx_person_id", "id"),
        UniqueConstraint("id", name="uq_account_id"),
        Index("idx_account_id_account_type", "id", account_type),
        CheckConstraint("balance >= 0", name="ck_balance"),
        CheckConstraint(
            "daily_withdrawal_limit >= 0", name="ck_daily_withdrawal_limit"
        ),
    )

    def __repr__(self):
        return f"<Account(id={self.id}, balance={self.balance}, daily_withdrawal_limit={self.daily_withdrawal_limit}, account_type={self.account_type})>"
