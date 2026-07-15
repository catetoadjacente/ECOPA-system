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
                SELECT d.cliente, d.cnpj, d.data AS data_dest,
                       p.estabelecimento AS ponto, c.quantidade
                FROM destinacoes d
                JOIN coleta c ON d.coleta_id_coleta = c.id_coleta
                JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                WHERE 1=1
            """
            params = []
            if data_inicio:
                query += " AND d.data >= %s"
                params.append(data_inicio)
            if data_fim:
                query += " AND d.data <= %s"
                params.append(data_fim)
            query += " ORDER BY d.data DESC"
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar destinacoes: {e}")
            return []
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
