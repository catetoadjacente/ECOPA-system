from database.conecta_database import get_connection


class Pedido:

    @staticmethod
    def criar(dados):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO pedido (id_destinacao, quantidade_solicitada, observacao) "
                "VALUES (%s, %s, %s)",
                (dados["id_destinacao"], dados["quantidade_solicitada"],
                 dados.get("observacao", "")))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar pedido: {e}")
            connection.rollback()
            return None
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def obter_por_id(id_pedido):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def listar_lotes_do_pedido(id_pedido):
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
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
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def vincular_lote(id_pedido, id_lote, quantidade_consumida):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO pedido_lote (id_pedido, id_lote, quantidade_consumida) "
                "VALUES (%s, %s, %s)",
                (id_pedido, id_lote, quantidade_consumida))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao vincular lote ao pedido: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def atualizar_status(id_pedido, status):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE pedido SET status=%s WHERE id_pedido=%s",
                (status, id_pedido))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar status do pedido: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def deletar(id_pedido):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM pedido_lote WHERE id_pedido=%s", (id_pedido,))
            cursor.execute("DELETE FROM pedido WHERE id_pedido=%s", (id_pedido,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar pedido: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()
