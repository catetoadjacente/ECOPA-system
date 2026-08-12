import logging
from database.cache import get_cached, invalidate_prefix
from models.base import BaseModel

logger = logging.getLogger(__name__)


class Pedido(BaseModel):

    @staticmethod
    def criar(dados):
        return BaseModel._execute_returning_id(
            "INSERT INTO pedido (id_destinacao, quantidade_solicitada, observacao) "
            "VALUES (%s, %s, %s)",
            (dados["id_destinacao"], dados["quantidade_solicitada"],
             dados.get("observacao", ""))
        )

    @staticmethod
    def listar_todos():
        def _fetch():
            return BaseModel._fetch_all("""
                SELECT pe.id_pedido AS id, pe.quantidade_solicitada,
                       pe.data AS data_pedido, pe.status, pe.observacao,
                       d.nome AS destinacao, d.tipo AS tipo_destinacao,
                       COALESCE(SUM(pl.quantidade_consumida), 0) AS quantidade_atendida
                FROM pedido pe
                JOIN destinacao d ON pe.id_destinacao = d.id_destinacao
                LEFT JOIN pedido_lote pl ON pe.id_pedido = pl.id_pedido
                GROUP BY pe.id_pedido
                ORDER BY pe.data DESC
            """)
        return get_cached("pedidos_listar_todos", 30, _fetch)

    @staticmethod
    def obter_por_id(id_pedido):
        return BaseModel._fetch_one("""
            SELECT pe.id_pedido AS id, pe.id_destinacao,
                   pe.quantidade_solicitada, pe.data AS data_pedido,
                   pe.status, pe.observacao,
                   d.nome AS destinacao, d.tipo AS tipo_destinacao,
                   COALESCE(SUM(pl.quantidade_consumida), 0) AS quantidade_atendida
            FROM pedido pe
            JOIN destinacao d ON pe.id_destinacao = d.id_destinacao
            LEFT JOIN pedido_lote pl ON pe.id_pedido = pl.id_pedido
            WHERE pe.id_pedido = %s
            GROUP BY pe.id_pedido
        """, (id_pedido,))

    @staticmethod
    def listar_lotes_do_pedido(id_pedido):
        return BaseModel._fetch_all("""
            SELECT pl.id_pedido_lote, pl.id_lote,
                   pl.quantidade_consumida,
                   l.quantidade_coletada, l.data_criacao,
                   p.estabelecimento AS ponto
            FROM pedido_lote pl
            JOIN lote l ON pl.id_lote = l.id_lote
            JOIN coleta c ON l.id_coleta = c.id_coleta
            JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
            WHERE pl.id_pedido = %s
        """, (id_pedido,))

    @staticmethod
    def vincular_lote(id_pedido, id_lote, quantidade_consumida):
        return BaseModel._execute(
            "INSERT INTO pedido_lote (id_pedido, id_lote, quantidade_consumida) "
            "VALUES (%s, %s, %s)",
            (id_pedido, id_lote, quantidade_consumida)
        )

    @staticmethod
    def vincular_lotes_batch(id_pedido, lotes):
        from database.conecta_database import db_connection
        with db_connection() as conn:
            if conn is None:
                return 0
            try:
                cursor = conn.cursor(dictionary=True)
                inserts = []
                lotes_validos = []
                for id_lote, quantidade in lotes:
                    qtd = float(quantidade)
                    if qtd <= 0:
                        continue
                    inserts.append((id_pedido, id_lote, qtd))
                    lotes_validos.append((id_lote, qtd))
                if not inserts:
                    return 0
                cursor.executemany(
                    "INSERT INTO pedido_lote (id_pedido, id_lote, quantidade_consumida) "
                    "VALUES (%s, %s, %s)",
                    inserts)
                ids_lotes = [l[0] for l in lotes_validos]
                placeholders = ", ".join(["%s"] * len(ids_lotes))
                cursor.execute(
                    f"SELECT id_lote, quantidade_restante FROM lote WHERE id_lote IN ({placeholders})",
                    ids_lotes)
                lotes_map = {r["id_lote"]: float(r["quantidade_restante"]) for r in cursor.fetchall()}
                total = 0
                updates = []
                for id_lote, qtd in lotes_validos:
                    restante = lotes_map.get(id_lote, 0)
                    if restante >= qtd:
                        nova_qtd = restante - qtd
                        novo_status = "Esgotado" if nova_qtd <= 0 else "Parcialmente Consumido"
                        updates.append((max(nova_qtd, 0), novo_status, id_lote))
                        total += qtd
                if updates:
                    cursor.executemany(
                        "UPDATE lote SET quantidade_restante = %s, status = %s WHERE id_lote = %s",
                        updates)
                conn.commit()
                invalidate_prefix("lotes")
                invalidate_prefix("pedidos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return total
            except Exception as e:
                logger.error("Erro ao vincular lotes em batch: %s", e)
                conn.rollback()
                return 0

    @staticmethod
    def atualizar_status(id_pedido, status):
        ok = BaseModel._execute(
            "UPDATE pedido SET status=%s WHERE id_pedido=%s",
            (status, id_pedido)
        )
        if ok:
            invalidate_prefix("pedidos")
            invalidate_prefix("dashboard")
            invalidate_prefix("relatorio")
        return ok

    @staticmethod
    def deletar(id_pedido):
        from database.conecta_database import db_connection
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pedido_lote WHERE id_pedido=%s", (id_pedido,))
                cursor.execute("DELETE FROM pedido WHERE id_pedido=%s", (id_pedido,))
                conn.commit()
                invalidate_prefix("pedidos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                logger.error("Erro ao deletar pedido: %s", e)
                conn.rollback()
                return False
