from database.conecta_database import db_connection
from database.cache import get_cached, invalidate, invalidate_prefix


class Pedido:

    @staticmethod
    def criar(dados):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO pedido (id_destinacao, quantidade_solicitada, observacao) "
                    "VALUES (%s, %s, %s)",
                    (dados["id_destinacao"], dados["quantidade_solicitada"],
                     dados.get("observacao", "")))
                conn.commit()
                invalidate_prefix("pedidos")
                invalidate_prefix("dashboard")
                return cursor.lastrowid
            except Exception as e:
                print(f"Erro ao criar pedido: {e}")
                conn.rollback()
                return None

    @staticmethod
    def listar_todos():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return []
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
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
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar pedidos: {e}")
                    return []
        return get_cached("pedidos_listar_todos", 30, _fetch)

    @staticmethod
    def obter_por_id(id_pedido):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
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
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar pedido: {e}")
                return None

    @staticmethod
    def listar_lotes_do_pedido(id_pedido):
        with db_connection() as conn:
            if conn is None:
                return []
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
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
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao listar lotes do pedido: {e}")
                return []

    @staticmethod
    def vincular_lote(id_pedido, id_lote, quantidade_consumida):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO pedido_lote (id_pedido, id_lote, quantidade_consumida) "
                    "VALUES (%s, %s, %s)",
                    (id_pedido, id_lote, quantidade_consumida))
                conn.commit()
                return True
            except Exception as e:
                print(f"Erro ao vincular lote ao pedido: {e}")
                conn.rollback()
                return False

    @staticmethod
    def vincular_lotes_batch(id_pedido, lotes):
        with db_connection() as conn:
            if conn is None:
                return 0
            try:
                cursor = conn.cursor(dictionary=True)
                total = 0
                for id_lote, quantidade in lotes:
                    if float(quantidade) <= 0:
                        continue
                    cursor.execute(
                        "INSERT INTO pedido_lote (id_pedido, id_lote, quantidade_consumida) "
                        "VALUES (%s, %s, %s)",
                        (id_pedido, id_lote, quantidade))
                    cursor.execute(
                        "SELECT quantidade_restante FROM lote WHERE id_lote = %s",
                        (id_lote,))
                    lote = cursor.fetchone()
                    if lote and float(lote["quantidade_restante"]) >= float(quantidade):
                        nova_qtd = float(lote["quantidade_restante"]) - float(quantidade)
                        novo_status = "Esgotado" if nova_qtd <= 0 else "Parcialmente Consumido"
                        nova_qtd = max(nova_qtd, 0)
                        cursor.execute(
                            "UPDATE lote SET quantidade_restante = %s, status = %s WHERE id_lote = %s",
                            (nova_qtd, novo_status, id_lote))
                        total += float(quantidade)
                conn.commit()
                return total
            except Exception as e:
                print(f"Erro ao vincular lotes em batch: {e}")
                conn.rollback()
                return 0

    @staticmethod
    def atualizar_status(id_pedido, status):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE pedido SET status=%s WHERE id_pedido=%s",
                    (status, id_pedido))
                conn.commit()
                invalidate_prefix("pedidos")
                invalidate_prefix("dashboard")
                return True
            except Exception as e:
                print(f"Erro ao atualizar status do pedido: {e}")
                conn.rollback()
                return False

    @staticmethod
    def deletar(id_pedido):
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
                return True
            except Exception as e:
                print(f"Erro ao deletar pedido: {e}")
                conn.rollback()
                return False
