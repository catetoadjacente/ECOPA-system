from database.database import get_connection


class Coleta:
    @staticmethod
    def listar_todas():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM coletas ORDER BY data_coleta DESC")
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
                INSERT INTO coletas (ponto, motorista, quantidade, data_coleta, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (dados["ponto"], dados["motorista"], dados["quantidade"],
                  dados["data_coleta"], dados.get("status", "Pendente")))
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
            cursor.execute("UPDATE coletas SET status=%s WHERE id=%s",
                           (status, id_coleta))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()