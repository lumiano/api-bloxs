from decimal import Decimal

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric

from api_bloxs.infra.database import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    id_conta = Column(Integer, nullable=False)
    id_pessoa = Column(Integer, nullable=False)
    saldo = Column(Numeric, nullable=False)
    limite_saque_diario = Column(Numeric, nullable=False)
    flag_ativo = Column(Boolean, nullable=False)
    tipo_conta = Column(Integer, nullable=False)
    data_criacao = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, id_conta={self.id_conta}, id_pessoa={self.id_pessoa}, saldo={self.saldo}, limite_saque_diario={self.limite_saque_diario}, flag_ativo={self.flag_ativo}, tipo_conta={self.tipo_conta}, data_criacao={self.data_criacao})>"
