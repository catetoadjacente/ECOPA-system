from database.database import get_connection


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
                       c.observacao AS motorista, c.quantidade,
                       c.data AS data_coleta, 'Pendente' AS status
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
                                   quantidade, data, observacao)
                VALUES (%s, %s, %s, %s, %s)
            """, (dados["ponto"], dados.get("gerente_cpf", "00000000000"),
                  dados["quantidade"], dados["data_coleta"],
                  dados.get("motorista", "")))
            connection.commit()
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
            cursor.execute("UPDATE coleta SET observacao=%s WHERE id_coleta=%s",
                           (status, id_coleta))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()
