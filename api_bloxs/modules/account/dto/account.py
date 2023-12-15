from apiflask import Schema
from apiflask.fields import Integer, String


class AccountDto(Schema):
    id = Integer()
    id_conta = Integer()
    id_pessoa = Integer()
    saldo = Integer()
    limite_saque_diario = Integer()
    flag_ativo = Integer()
    tipo_conta = Integer()
    data_criacao = String()
