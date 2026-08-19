import logging
from database.cache import get_cached, invalidate_prefix
from models.base import BaseModel, DatabaseError

logger = logging.getLogger(__name__)


class Ponto(BaseModel):

    @staticmethod
    def buscar_por_estabelecimento(estabelecimento):
        try:
            return BaseModel._fetch_one("""
                SELECT id_ponto
                FROM ponto_de_coleta
                WHERE estabelecimento = %s AND ativo = 1
                LIMIT 1
            """, (estabelecimento,))
        except DatabaseError:
            return None

    @staticmethod
    def buscar_por_idponto(idponto):
        try:
            return BaseModel._fetch_one("""
                SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.proprietario
                FROM ponto_de_coleta p
                WHERE p.id_ponto = %s LIMIT 1
            """, (idponto,))
        except DatabaseError:
            return None

    @staticmethod
    def criar(dados):
        try:
            ok = BaseModel._execute("""
                INSERT INTO ponto_de_coleta (endereco, email, estabelecimento,
                                             telefone, proprietario)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dados["endereco"], dados["email"],
                dados["estabelecimento"], dados["telefone"], dados["proprietario"]
            ))
            if ok:
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def listar():
        def _fetch():
            return BaseModel._fetch_all("""
                SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.proprietario
                FROM ponto_de_coleta p
                WHERE p.ativo = 1
                ORDER BY p.estabelecimento
            """)
        return get_cached("pontos_listar", 120, _fetch)

    @staticmethod
    def listar_todos():
        def _fetch():
            return BaseModel._fetch_all("""
                SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.proprietario, p.ativo
                FROM ponto_de_coleta p
                ORDER BY p.ativo DESC, p.estabelecimento
            """)
        return get_cached("pontos_listar_todos", 120, _fetch)

    @staticmethod
    def atualizar(idponto, dados):
        try:
            ok = BaseModel._execute("""
                UPDATE ponto_de_coleta
                SET endereco=%s, email=%s, telefone=%s, proprietario=%s
                WHERE id_ponto=%s
            """, (
                dados["endereco"], dados["email"],
                dados["telefone"], dados["proprietario"], idponto
            ))
            if ok:
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def deletar(idponto):
        try:
            ok = BaseModel._execute(
                "DELETE FROM ponto_de_coleta WHERE id_ponto=%s", (idponto,)
            )
            if ok:
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def desativar(idponto):
        try:
            ok = BaseModel._execute(
                "UPDATE ponto_de_coleta SET ativo = 0 WHERE id_ponto = %s", (idponto,)
            )
            if ok:
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def reativar(idponto):
        try:
            ok = BaseModel._execute(
                "UPDATE ponto_de_coleta SET ativo = 1 WHERE id_ponto = %s", (idponto,)
            )
            if ok:
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def salvar_horarios(id_ponto, horarios):
        from database.conecta_database import db_connection
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM horario_ponto WHERE ponto_de_coleta_id_ponto = %s",
                    (id_ponto,)
                )
                for h in horarios:
                    cursor.execute("""
                        INSERT INTO horario_ponto
                        (dia_semana, abertura, fechamento, ativo, ponto_de_coleta_id_ponto)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (h["dia_semana"], h["abertura"], h["fechamento"],
                        h["ativo"], id_ponto))
                conn.commit()
                invalidate_prefix(f"pontos_horarios_{id_ponto}")
                return True
            except Exception as e:
                logger.error("Erro ao salvar horarios: %s", e)
                conn.rollback()
                return False

    @staticmethod
    def buscar_horarios(id_ponto):
        def _fetch():
            return BaseModel._fetch_all(
                "SELECT * FROM horario_ponto WHERE ponto_de_coleta_id_ponto = %s ORDER BY dia_semana",
                (id_ponto,)
            )
        return get_cached(f"pontos_horarios_{id_ponto}", 120, _fetch)
