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
<<<<<<< HEAD
                SELECT id, ponto, motorista, quantidade,
                       data_coleta, status
                FROM coletas
                ORDER BY data_coleta DESC
=======
                SELECT c.id_coleta AS id, p.estabelecimento AS ponto,
                       c.observacao AS observacao, c.quantidade,
                       c.data AS data_coleta, c.status
                FROM coleta c
                JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                ORDER BY c.data DESC
>>>>>>> main
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
<<<<<<< HEAD
                INSERT INTO coletas (ponto, motorista, quantidade, data_coleta, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (dados["ponto"], dados["motorista"],
                  dados["quantidade"], dados["data_coleta"],
                  dados.get("status", "Pendente")))
=======
                INSERT INTO coleta (ponto_de_coleta_id_ponto, gerente_cpf,
                                   quantidade, data, observacao, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (dados["ponto"], dados.get("gerente_cpf", "00000000000"),
                  dados["quantidade"], dados["data_coleta"],
                  dados.get("observacao", ""), "Pendente"))
>>>>>>> main
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
    def deletar(id_coleta):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
<<<<<<< HEAD
            cursor.execute("DELETE FROM coletas WHERE id=%s", (id_coleta,))
=======
            cursor.execute("UPDATE coleta SET status=%s WHERE id_coleta=%s",
                           (status, id_coleta))
>>>>>>> main
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar coleta: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()
