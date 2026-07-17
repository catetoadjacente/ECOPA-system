from database.database import get_connection


class Relatorio:
    @staticmethod
    def coletas_filtradas(data_inicio=None, data_fim=None, id_ponto=None, status=None):
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT c.id_coleta AS id, p.estabelecimento AS ponto,
                       c.observacao, c.quantidade, c.data AS data_coleta, c.status
                FROM coleta c
                JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                WHERE 1=1
            """
            params = []
            if data_inicio:
                query += " AND c.data >= %s"
                params.append(data_inicio)
            if data_fim:
                query += " AND c.data <= %s"
                params.append(data_fim)
            if id_ponto:
                query += " AND c.ponto_de_coleta_id_ponto = %s"
                params.append(id_ponto)
            if status and status != "TODOS":
                query += " AND c.status = %s"
                params.append(status)
            query += " ORDER BY c.data DESC"
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao filtrar coletas: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def coletas_por_ponto(data_inicio=None, data_fim=None):
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.estabelecimento AS ponto,
                       COUNT(c.id_coleta) AS total_coletas,
                       SUM(c.quantidade) AS total_kg,
                       SUM(CASE WHEN c.status='Pendente' THEN 1 ELSE 0 END) AS pendentes,
                       SUM(CASE WHEN c.status='Realizada' THEN 1 ELSE 0 END) AS realizadas
                FROM ponto_de_coleta p
                LEFT JOIN coleta c ON c.ponto_de_coleta_id_ponto = p.id_ponto
            """
            params = []
            conditions = []
            if data_inicio:
                conditions.append("c.data >= %s")
                params.append(data_inicio)
            if data_fim:
                conditions.append("c.data <= %s")
                params.append(data_fim)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            query += " GROUP BY p.id_ponto, p.estabelecimento ORDER BY total_coletas DESC"
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar coletas por ponto: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def resumo_destinacoes(data_inicio=None, data_fim=None):
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT d.nome AS destinacao, d.tipo,
                       COUNT(pe.id_pedido) AS total_pedidos,
                       SUM(pe.quantidade_solicitada) AS total_kg
                FROM pedido pe
                JOIN destinacao d ON pe.id_destinacao = d.id_destinacao
                WHERE pe.status != 'Cancelado'
            """
            params = []
            if data_inicio:
                query += " AND pe.data >= %s"
                params.append(data_inicio)
            if data_fim:
                query += " AND pe.data <= %s"
                params.append(data_fim)
            query += " GROUP BY d.nome, d.tipo ORDER BY total_kg DESC"
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao resumir destinacoes: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def resumo_estoque():
        connection = get_connection()
        if connection is None:
            return {}
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_lotes,
                    COALESCE(SUM(quantidade_restante), 0) AS estoque_total,
                    SUM(CASE WHEN status = 'Disponivel' THEN 1 ELSE 0 END) AS lotes_disponiveis,
                    SUM(CASE WHEN status = 'Parcialmente Consumido' THEN 1 ELSE 0 END) AS lotes_parciais,
                    SUM(CASE WHEN status = 'Esgotado' THEN 1 ELSE 0 END) AS lotes_esgotados
                FROM lote
            """)
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao resumir estoque: {e}")
            return {}
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def resumo_pedidos():
        connection = get_connection()
        if connection is None:
            return {}
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_pedidos,
                    SUM(CASE WHEN status = 'Aberto' THEN 1 ELSE 0 END) AS pedidos_abertos,
                    SUM(CASE WHEN status = 'Atendido' THEN 1 ELSE 0 END) AS pedidos_atendidos,
                    SUM(CASE WHEN status = 'Cancelado' THEN 1 ELSE 0 END) AS pedidos_cancelados
                FROM pedido
            """)
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao resumir pedidos: {e}")
            return {}
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def listar_pontos():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_ponto, estabelecimento FROM ponto_de_coleta ORDER BY estabelecimento"
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar pontos: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()
