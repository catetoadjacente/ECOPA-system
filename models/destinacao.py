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
                SELECT id_destinacao AS id, nome, tipo, endereco,
                       telefone, email, cnpj
                FROM destinacao
                ORDER BY nome ASC
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
            cursor.execute(
                "INSERT INTO destinacao (nome, tipo, endereco, telefone, email, cnpj) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (dados["nome"], dados["tipo"], dados["endereco"],
                 dados.get("telefone", ""), dados.get("email", ""),
                 dados.get("cnpj", "")))
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
            cursor.execute(
                "UPDATE destinacao SET nome=%s, tipo=%s, endereco=%s, telefone=%s, email=%s, cnpj=%s "
                "WHERE id_destinacao=%s",
                (dados["nome"], dados["tipo"], dados["endereco"],
                 dados.get("telefone", ""), dados.get("email", ""),
                 dados.get("cnpj", ""), id_dest))
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
            cursor.execute("DELETE FROM destinacao WHERE id_destinacao=%s", (id_dest,))
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
    def buscar_por_id(id_dest):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_destinacao AS id, nome, tipo, endereco,
                       telefone, email, cnpj
                FROM destinacao
                WHERE id_destinacao = %s
            """, (id_dest,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar destinacao: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def buscar_por_cnpj(cnpj):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_destinacao AS id, nome, tipo, endereco,
                       telefone, email, cnpj
                FROM destinacao
                WHERE cnpj = %s
            """, (cnpj,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar destinacao por CNPJ: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()
