from database.conecta_database import db_connection
from database.cache import get_cached, invalidate, invalidate_prefix


class Coleta:
    @staticmethod
    def listar_todas():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return []
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
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
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar coletas: {e}")
                    return []
        return get_cached("coletas_listar", 30, _fetch)

    @staticmethod
    def criar(dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO coleta (ponto_de_coleta_id_ponto, gerente_cpf,
                                       quantidade, data, observacao, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (dados["ponto"], dados.get("gerente_cpf", "00000000000"),
                      dados["quantidade"], dados["data_coleta"],
                      dados.get("observacao", ""), "Pendente"))
                conn.commit()
                invalidate_prefix("coletas")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao criar coleta: {e}")
                conn.rollback()
                return False

    @staticmethod
    def buscar_por_id(id_coleta):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT id_coleta AS id, quantidade, status FROM coleta WHERE id_coleta = %s",
                    (id_coleta,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar coleta por id: {e}")
                return None

    @staticmethod
    def atualizar_status(id_coleta, status):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE coleta SET status=%s WHERE id_coleta=%s",
                               (status, id_coleta))
                conn.commit()
                invalidate_prefix("coletas")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao atualizar status: {e}")
                return False

    @staticmethod
    def resumo_dashboard():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return {"total_coletas": 0, "quantidade_total": 0, "pendentes": 0, "realizadas": 0}
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT
                            COUNT(*) AS total_coletas,
                            COALESCE(SUM(quantidade), 0) AS quantidade_total,
                            SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END) AS pendentes,
                            SUM(CASE WHEN status = 'Realizada' THEN 1 ELSE 0 END) AS realizadas
                        FROM coleta
                        WHERE DATE(data) = CURDATE()
                    """)
                    return cursor.fetchone()
                except Exception as e:
                    print(f"Erro ao buscar resumo dashboard: {e}")
                    return {"total_coletas": 0, "quantidade_total": 0, "pendentes": 0, "realizadas": 0}
        return get_cached("dashboard_resumo", 30, _fetch)
