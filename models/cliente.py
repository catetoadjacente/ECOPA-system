from database.database import get_connection


class Cliente:
    @staticmethod
    def buscar_por_estabelecimento(estabelecimento):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_ponto FROM ponto_de_coleta WHERE estabelecimento = %s LIMIT 1",
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
            query = """
                SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.proprietario,
                       d.id_destinacoes, d.cnpj, d.cliente as cliente_nome, d.data
                FROM ponto_de_coleta p
                LEFT JOIN destinacoes d ON p.estabelecimento = d.cliente
                WHERE p.id_ponto = %s LIMIT 1
            """
            cursor.execute(query, (idponto,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
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
                INSERT INTO ponto_de_coleta (endereco, email, estabelecimento,
                                             telefone, proprietario)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dados["endereco"], dados["email"],
                dados["estabelecimento"], dados["telefone"], dados["proprietario"]
            ))
            cursor.execute("""
                INSERT INTO destinacoes (cnpj, cliente, data, coleta_id_coleta)
                VALUES (%s, %s, %s, %s)
            """, (
                dados["cnpj"], dados["cliente"],
                dados["data"], dados.get("coleta_id_coleta")
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar cliente: {e}")
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
            query = """
                SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.proprietario,
                       d.id_destinacoes, d.cnpj, d.cliente as cliente_nome, d.data
                FROM ponto_de_coleta p
                LEFT JOIN destinacoes d ON p.estabelecimento = d.cliente
                ORDER BY p.estabelecimento
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
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
                UPDATE ponto_de_coleta
                SET endereco=%s, email=%s, telefone=%s, proprietario=%s
                WHERE id_ponto=%s
            """, (
                dados["endereco"], dados["email"],
                dados["telefone"], dados["proprietario"], idponto
            ))
            if dados.get("cnpj"):
                cursor.execute("""
                    UPDATE destinacoes d
                    JOIN ponto_de_coleta p ON p.estabelecimento = d.cliente
                    SET d.cnpj = %s
                    WHERE p.id_ponto = %s
                """, (dados["cnpj"], idponto))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
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
            cursor.execute("""
                DELETE d FROM destinacoes d
                JOIN ponto_de_coleta p ON p.estabelecimento = d.cliente
                WHERE p.id_ponto = %s
            """, (idponto,))
            cursor.execute("DELETE FROM ponto_de_coleta WHERE id_ponto=%s", (idponto,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()
