import logging
from database.cache import get_cached, invalidate_prefix
from models.base import BaseModel, DatabaseError

logger = logging.getLogger(__name__)


class Destinacao(BaseModel):

    @staticmethod
    def listar_todas():
        def _fetch():
            return BaseModel._fetch_all("""
                SELECT id_destinacao AS id, nome, tipo, endereco,
                       telefone, email, cnpj
                FROM destinacao
                ORDER BY nome ASC
            """)
        return get_cached("destinacoes_listar", 120, _fetch)

    @staticmethod
    def criar(dados):
        try:
            destinacao_id = BaseModel._execute_returning_id(
                "INSERT INTO destinacao (nome, tipo, endereco, telefone, email, cnpj) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (dados["nome"], dados["tipo"], dados["endereco"],
                 dados.get("telefone", ""), dados.get("email", ""),
                 dados.get("cnpj", ""))
            )
            if destinacao_id:
                invalidate_prefix("destinacoes")
                invalidate_prefix("pedidos")
                invalidate_prefix("relatorio")
            return destinacao_id
        except DatabaseError:
            return None

    @staticmethod
    def atualizar(id_dest, dados):
        try:
            ok = BaseModel._execute(
                "UPDATE destinacao SET nome=%s, tipo=%s, endereco=%s, telefone=%s, email=%s, cnpj=%s "
                "WHERE id_destinacao=%s",
                (dados["nome"], dados["tipo"], dados["endereco"],
                 dados.get("telefone", ""), dados.get("email", ""),
                 dados.get("cnpj", ""), id_dest)
            )
            if ok:
                invalidate_prefix("destinacoes")
                invalidate_prefix("pedidos")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def deletar(id_dest):
        try:
            ok = BaseModel._execute(
                "DELETE FROM destinacao WHERE id_destinacao=%s", (id_dest,)
            )
            if ok:
                invalidate_prefix("destinacoes")
                invalidate_prefix("pedidos")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def buscar_por_id(id_dest):
        try:
            return BaseModel._fetch_one("""
                SELECT id_destinacao AS id, nome, tipo, endereco,
                       telefone, email, cnpj
                FROM destinacao
                WHERE id_destinacao = %s
            """, (id_dest,))
        except DatabaseError:
            return None

    @staticmethod
    def buscar_por_cnpj(cnpj):
        try:
            return BaseModel._fetch_one("""
                SELECT id_destinacao AS id, nome, tipo, endereco,
                       telefone, email, cnpj
                FROM destinacao
                WHERE cnpj = %s
            """, (cnpj,))
        except DatabaseError:
            return None
