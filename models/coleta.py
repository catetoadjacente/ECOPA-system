import logging
from database.cache import get_cached, invalidate_prefix
from models.base import BaseModel, DatabaseError

logger = logging.getLogger(__name__)


class Coleta(BaseModel):

    @staticmethod
    def listar_todas():
        def _fetch():
            return BaseModel._fetch_all("""
                SELECT c.id_coleta AS id, p.estabelecimento AS ponto,
                       c.observacao AS observacao, c.quantidade,
                       c.data AS data_coleta, c.status,
                       CASE WHEN EXISTS (
                           SELECT 1 FROM lote l WHERE l.id_coleta = c.id_coleta
                       ) THEN 1 ELSE 0 END AS tem_lote
                FROM coleta c
                JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                ORDER BY c.data DESC
            """)
        return get_cached("coletas_listar", 30, _fetch)

    @staticmethod
    def criar(dados):
        try:
            coleta_id = BaseModel._execute_returning_id("""
                INSERT INTO coleta (ponto_de_coleta_id_ponto, gerente_cpf,
                                   quantidade, data, observacao, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (dados["ponto"], dados.get("gerente_cpf", "00000000000"),
                  dados["quantidade"], dados["data_coleta"],
                  dados.get("observacao", ""), "Pendente"))
            if coleta_id:
                invalidate_prefix("coletas")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return coleta_id
        except DatabaseError:
            return None

    @staticmethod
    def buscar_por_id(id_coleta):
        try:
            return BaseModel._fetch_one(
                "SELECT id_coleta AS id, quantidade, status FROM coleta WHERE id_coleta = %s",
                (id_coleta,)
            )
        except DatabaseError:
            return None

    @staticmethod
    def atualizar_status(id_coleta, status):
        try:
            ok = BaseModel._execute(
                "UPDATE coleta SET status=%s WHERE id_coleta=%s",
                (status, id_coleta)
            )
            if ok:
                invalidate_prefix("coletas")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
            return ok
        except DatabaseError:
            return False

    @staticmethod
    def resumo_dashboard():
        def _fetch():
            try:
                return BaseModel._fetch_one("""
                    SELECT
                        COUNT(*) AS total_coletas,
                        COALESCE(SUM(quantidade), 0) AS quantidade_total,
                        SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END) AS pendentes,
                        SUM(CASE WHEN status = 'Realizada' THEN 1 ELSE 0 END) AS realizadas
                    FROM coleta
                    WHERE DATE(data) = CURDATE()
                """) or {"total_coletas": 0, "quantidade_total": 0, "pendentes": 0, "realizadas": 0}
            except DatabaseError:
                return {"total_coletas": 0, "quantidade_total": 0, "pendentes": 0, "realizadas": 0}
        return get_cached("dashboard_resumo", 30, _fetch)
