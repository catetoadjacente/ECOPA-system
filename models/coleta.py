from database.conecta_database import get_connection
from database.cache import invalidate


class Coleta:
    @staticmethod
    def listar_todas():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def criar(dados):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO coleta (ponto_de_coleta_id_ponto, gerente_cpf,
                                   quantidade, data, observacao, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (dados["ponto"], dados.get("gerente_cpf", "00000000000"),
                  dados["quantidade"], dados["data_coleta"],
                  dados.get("observacao", ""), "Pendente"))
            connection.commit()
            invalidate("coletas_listar")
            return True
        except Exception as e:
            print(f"Erro ao criar coleta: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def atualizar_status(id_coleta, status):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE coleta SET status=%s WHERE id_coleta=%s",
                           (status, id_coleta))
            connection.commit()
            invalidate("coletas_listar")
            return True
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def resumo_dashboard():
        connection = get_connection()
        if connection is None:
            return {"total_coletas": 0, "quantidade_total": 0, "pendentes": 0, "realizadas": 0}
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_coletas,
                    COALESCE(SUM(quantidade), 0) AS quantidade_total,
                    SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END) AS pendentes,
                    SUM(CASE WHEN status = 'Realizada' THEN 1 ELSE 0 END) AS realizadas
                FROM coleta
            """)
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar resumo dashboard: {e}")
            return {"total_coletas": 0, "quantidade_total": 0, "pendentes": 0, "realizadas": 0}
        finally:
            if connection.is_connected():
                connection.close()
