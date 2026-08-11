import logging
from database.cache import get_cached, invalidate, invalidate_prefix
from models.base import BaseModel

logger = logging.getLogger(__name__)


class Gerente(BaseModel):

    @staticmethod
    def verificar_login(nome, senha):
        return BaseModel._fetch_one(
            "SELECT senha FROM gerente WHERE nome = %s AND senha = %s LIMIT 1",
            (nome, senha)
        ) is not None

    @staticmethod
    def autenticar_e_buscar(nome, senha):
        return BaseModel._fetch_one(
            "SELECT cpf, nome, celular, email, setor FROM gerente WHERE nome = %s AND senha = %s LIMIT 1",
            (nome, senha)
        )

    @staticmethod
    def buscar_por_nome(nome):
        return BaseModel._fetch_one(
            "SELECT * FROM gerente WHERE nome = %s LIMIT 1", (nome,)
        )

    @staticmethod
    def criar(dados):
        return BaseModel._execute(
            "INSERT INTO gerente (cpf, nome, celular, email, senha, setor) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (dados["cpf"], dados["nome"], dados["celular"],
             dados["email"], dados["senha"], dados["setor"])
        )

    @staticmethod
    def listar():
        return BaseModel._fetch_all(
            "SELECT cpf, nome, celular, email, setor FROM gerente"
        )

    @staticmethod
    def buscar_por_email(email):
        return BaseModel._fetch_one(
            "SELECT * FROM gerente WHERE email = %s LIMIT 1", (email,)
        )

    @staticmethod
    def buscar_por_cpf(cpf):
        return BaseModel._fetch_one(
            "SELECT * FROM gerente WHERE cpf = %s LIMIT 1", (cpf,)
        )

    @staticmethod
    def atualizar(cpf, dados):
        return BaseModel._execute(
            "UPDATE gerente SET celular = %s, email = %s, setor = %s WHERE cpf = %s",
            (dados["celular"], dados["email"], dados["setor"], cpf)
        )

    @staticmethod
    def deletar(cpf):
        return BaseModel._execute(
            "DELETE FROM gerente WHERE cpf = %s", (cpf,)
        )
