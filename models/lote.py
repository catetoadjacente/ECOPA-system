from database.conecta_database import get_connection


class Lote:

    @staticmethod
    def criar_por_coleta(id_coleta, quantidade):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO lote (id_coleta, quantidade_coletada, quantidade_restante, status) "
                "VALUES (%s, %s, %s, 'Disponivel')",
                (id_coleta, quantidade, quantidade))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar lote: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def listar_disponiveis():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def listar_todos():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def consumir(id_lote, quantidade):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT quantidade_restante FROM lote WHERE id_lote = %s",
                (id_lote,))
            lote = cursor.fetchone()
            if lote is None:
                return False
            if float(lote["quantidade_restante"]) < float(quantidade):
                return False
            nova_qtd = float(lote["quantidade_restante"]) - float(quantidade)
            if nova_qtd <= 0:
                novo_status = "Esgotado"
                nova_qtd = 0
            else:
                novo_status = "Parcialmente Consumido"
            cursor.execute(
                "UPDATE lote SET quantidade_restante = %s, status = %s WHERE id_lote = %s",
                (nova_qtd, novo_status, id_lote))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao consumir lote: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def obter_por_id(id_lote):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def buscar_por_coleta(id_coleta):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM lote WHERE id_coleta = %s LIMIT 1",
                (id_coleta,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar lote por coleta: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()
