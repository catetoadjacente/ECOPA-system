from database.database import get_connection


class Ponto:
    @staticmethod
    def buscar_por_estabelecimento(estabelecimento):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT idponto FROM ponto WHERE estabelecimento = %s LIMIT 1",
                (estabelecimento,)
            )
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar ponto por estabelecimento: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def buscar_por_idponto(idponto):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT idponto, endereco, email, estabelecimento,
                       telefone, propretario as proprietario
                FROM ponto
                WHERE idponto = %s LIMIT 1
            """, (idponto,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar ponto de coleta: {e}")
            return None
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
                INSERT INTO ponto (endereco, email, estabelecimento, telefone, propretario)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dados["endereco"], dados["email"],
                dados["estabelecimento"], dados["telefone"], dados["proprietario"]
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar ponto de coleta: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def listar():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT idponto, endereco, email, estabelecimento,
                       telefone, propretario as proprietario
                FROM ponto
                ORDER BY estabelecimento
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar pontos de coleta: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def atualizar(idponto, dados):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE ponto
                SET endereco=%s, email=%s, telefone=%s, propretario=%s
                WHERE idponto=%s
            """, (
                dados["endereco"], dados["email"],
                dados["telefone"], dados["proprietario"], idponto
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar ponto de coleta: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def deletar(idponto):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM ponto WHERE idponto=%s", (idponto,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar ponto de coleta: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()
