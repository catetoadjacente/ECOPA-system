from database.database import get_connection


class Destinacao:
    @staticmethod
    def listar_todas():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT d.id_destinacoes AS id, d.cliente, d.cnpj,
                       d.data AS data_dest, d.coleta_id_coleta,
                       c.quantidade, c.observacao,
                       p.estabelecimento AS ponto
                FROM destinacoes d
                JOIN coleta c ON d.coleta_id_coleta = c.id_coleta
                JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                ORDER BY d.data DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar destinacoes: {e}")
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
                INSERT INTO destinacoes (cnpj, cliente, data, coleta_id_coleta)
                VALUES (%s, %s, %s, %s)
            """, (dados["cnpj"], dados["cliente"], dados["data"], dados["coleta_id_coleta"]))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar destinacao: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def atualizar(id_dest, dados):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE destinacoes
                SET cnpj=%s, cliente=%s, data=%s, coleta_id_coleta=%s
                WHERE id_destinacoes=%s
            """, (dados["cnpj"], dados["cliente"], dados["data"],
                  dados["coleta_id_coleta"], id_dest))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar destinacao: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def deletar(id_dest):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM destinacoes WHERE id_destinacoes=%s", (id_dest,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar destinacao: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def listar_coletas_disponiveis():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id_coleta AS id, c.quantidade, c.data,
                       p.estabelecimento AS ponto
                FROM coleta c
                JOIN ponto_de_coleta p ON c.ponto_de_coleta_id_ponto = p.id_ponto
                WHERE c.id_coleta NOT IN (
                    SELECT coleta_id_coleta FROM destinacoes
                )
                ORDER BY c.data DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar coletas disponiveis: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()
