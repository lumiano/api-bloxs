from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Index, Integer, Numeric,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from api_bloxs.base.model import Model


class Transaction(Model):
    """Transaction model"""

    __tablename__ = "transaction"

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    account = relationship("Account", back_populates="transactions")
    amount = Column(Numeric(10, 2), nullable=False, comment="Amount")
    transaction_date = Column(DateTime, nullable=False, comment="Transaction date")

    __table_args__ = (
        Index("idx_id_transaction", "id"),
        Index("idx_account_id", "account_id"),
        UniqueConstraint(
            "account_id", "transaction_date", name="uq_account_transaction_date"
        ),
        ForeignKeyConstraint(["account_id"], ["account.id"], name="fk_account_id"),
        CheckConstraint("amount > 0", name="ck_amount"),
    )

    def __repr__(self):
        return f"<Transaction(id={self.id}, account_id={self.account_id}, amount={self.amount}, transaction_date={self.transaction_date})>"
