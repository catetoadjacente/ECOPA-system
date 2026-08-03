from database.conecta_database import db_connection
from database.cache import get_cached, invalidate, invalidate_prefix


class Lote:

    @staticmethod
    def criar_por_coleta(id_coleta, quantidade):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO lote (id_coleta, quantidade_coletada, quantidade_restante, status) "
                    "VALUES (%s, %s, %s, 'Disponivel')",
                    (id_coleta, quantidade, quantidade))
                conn.commit()
                invalidate_prefix("lotes")
                invalidate_prefix("dashboard")
                return True
            except Exception as e:
                print(f"Erro ao criar lote: {e}")
                conn.rollback()
                return False

    @staticmethod
    def listar_disponiveis():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return []
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT l.id_lote AS id, l.id_coleta,
                               l.quantidade_coletada, l.quantidade_restante,
                               l.status, l.data_criacao,
                               c.data AS data_coleta,
                               p.estabelecimento AS ponto
                        FROM lote l
                        JOIN coleta c ON l.id_coleta = c.id_coleta
                        JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                        WHERE l.quantidade_restante > 0
                        ORDER BY l.data_criacao DESC
                    """)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar lotes: {e}")
                    return []
        return get_cached("lotes_disponiveis", 30, _fetch)

    @staticmethod
    def listar_todos():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return []
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT l.id_lote AS id, l.id_coleta,
                               l.quantidade_coletada, l.quantidade_restante,
                               l.status, l.data_criacao,
                               c.data AS data_coleta,
                               p.estabelecimento AS ponto
                        FROM lote l
                        JOIN coleta c ON l.id_coleta = c.id_coleta
                        JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                        ORDER BY l.data_criacao DESC
                    """)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar lotes: {e}")
                    return []
        return get_cached("lotes_listar_todos", 30, _fetch)

    @staticmethod
    def consumir(id_lote, quantidade):
        """Consome lote em uma unica query atomica."""
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    UPDATE lote
                    SET quantidade_restante = CASE
                            WHEN quantidade_restante - %s <= 0 THEN 0
                            ELSE quantidade_restante - %s
                        END,
                        status = CASE
                            WHEN quantidade_restante - %s <= 0 THEN 'Esgotado'
                            WHEN quantidade_restante - %s > 0 AND quantidade_restante < quantidade_coletada
                            THEN 'Parcialmente Consumido'
                            ELSE status
                        END
                    WHERE id_lote = %s AND quantidade_restante >= %s
                """, (quantidade, quantidade, quantidade, quantidade, id_lote, quantidade))
                conn.commit()
                if cursor.rowcount > 0:
                    invalidate_prefix("lotes")
                    invalidate_prefix("dashboard")
                    return True
                return False
            except Exception as e:
                print(f"Erro ao consumir lote: {e}")
                conn.rollback()
                return False

    @staticmethod
    def obter_por_id(id_lote):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT l.id_lote AS id, l.id_coleta,
                           l.quantidade_coletada, l.quantidade_restante,
                           l.status, l.data_criacao,
                           c.data AS data_coleta,
                           p.estabelecimento AS ponto
                    FROM lote l
                    JOIN coleta c ON l.id_coleta = c.id_coleta
                    JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                    WHERE l.id_lote = %s
                """, (id_lote,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar lote: {e}")
                return None

    @staticmethod
    def buscar_por_coleta(id_coleta):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM lote WHERE id_coleta = %s LIMIT 1",
                    (id_coleta,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar lote por coleta: {e}")
                return None

    @staticmethod
    def resumo_estoque_dashboard():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return {"total_lotes": 0, "estoque_total": 0}
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT
                            COUNT(*) AS total_lotes,
                            COALESCE(SUM(quantidade_restante), 0) AS estoque_total
                        FROM lote
                        WHERE status != 'Esgotado'
                    """)
                    return cursor.fetchone()
                except Exception as e:
                    print(f"Erro ao buscar resumo estoque: {e}")
                    return {"total_lotes": 0, "estoque_total": 0}
        return get_cached("dashboard_estoque", 30, _fetch)
