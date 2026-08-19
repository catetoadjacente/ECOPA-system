import logging
import bcrypt
from database.cache import get_cached, invalidate, invalidate_prefix
from database.conecta_database import db_connection
from models.base import BaseModel, DatabaseError

logger = logging.getLogger(__name__)


class Gerente(BaseModel):

    @staticmethod
    def verificar_login(nome, senha):
        try:
            user = BaseModel._fetch_one(
                "SELECT senha FROM gerente WHERE nome = %s LIMIT 1", (nome,)
            )
            if user and user.get("senha"):
                return bcrypt.checkpw(senha.encode(), user["senha"].encode())
            return False
        except DatabaseError:
            return False

    @staticmethod
    def autenticar_e_buscar(nome, senha):
        if not Gerente.verificar_login(nome, senha):
            return None
        try:
            return BaseModel._fetch_one(
                "SELECT cpf, nome, celular, email FROM gerente WHERE nome = %s LIMIT 1",
                (nome,)
            )
        except DatabaseError:
            return None

    @staticmethod
    def buscar_por_nome(nome):
        try:
            return BaseModel._fetch_one(
                "SELECT cpf, nome, celular, email FROM gerente WHERE nome = %s LIMIT 1",
                (nome,)
            )
        except DatabaseError:
            return None

    @staticmethod
    def criar(dados):
        try:
            senha_hash = bcrypt.hashpw(dados["senha"].encode(), bcrypt.gensalt()).decode()
            return BaseModel._execute(
                "INSERT INTO gerente (cpf, nome, celular, email, senha) "
                "VALUES (%s, %s, %s, %s, %s)",
                (dados["cpf"], dados["nome"], dados["celular"],
                 dados["email"], senha_hash)
            )
        except DatabaseError:
            return False

    @staticmethod
    def listar():
        try:
            return BaseModel._fetch_all(
                "SELECT cpf, nome, celular, email FROM gerente"
            )
        except DatabaseError:
            return []

    @staticmethod
    def buscar_por_email(email):
        try:
            return BaseModel._fetch_one(
                "SELECT cpf, nome, celular, email FROM gerente WHERE email = %s LIMIT 1",
                (email,)
            )
        except DatabaseError:
            return None

    @staticmethod
    def buscar_por_cpf(cpf):
        try:
            return BaseModel._fetch_one(
                "SELECT cpf, nome, celular, email FROM gerente WHERE cpf = %s LIMIT 1",
                (cpf,)
            )
        except DatabaseError:
            return None

    @staticmethod
    def atualizar(cpf, dados):
        try:
            return BaseModel._execute(
                "UPDATE gerente SET celular = %s, email = %s WHERE cpf = %s",
                (dados["celular"], dados["email"], cpf)
            )
        except DatabaseError:
            return False

    @staticmethod
    def deletar(cpf):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE coleta SET gerente_cpf = NULL WHERE gerente_cpf = %s", (cpf,))
                cursor.execute("DELETE FROM gerente WHERE cpf = %s", (cpf,))
                conn.commit()
                return True
            except Exception as e:
                logger.error("Erro ao deletar gerente: %s", e)
                conn.rollback()
                return False
