from database.database import get_connection


class Cliente:
    @staticmethod
    def buscar_por_idponto(idponto):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.propretario as proprietario,
                       d.id_destinacoes, d.cnpj, d.cliente as cliente_nome, d.data
                FROM ponto p
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
            query_ponto = """INSERT INTO ponto (endereco, email, estabelecimento,
                           telefone, propretario)
                           VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query_ponto, (
                dados["endereco"], dados["email"],
                dados["estabelecimento"], dados["telefone"], dados["proprietario"]
            ))
            query_dest = """INSERT INTO destinacoes (cnpj, cliente, data, coleta_id_coleta)
                           VALUES (%s, %s, %s, %s)"""
            cursor.execute(query_dest, (
                dados["cnpj"], dados["cliente"], dados["data"], dados.get("coleta_id_coleta")
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
                       p.telefone, p.propretario as proprietario,
                       d.id_destinacoes, d.cnpj, d.cliente as cliente_nome, d.data
                FROM ponto p
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
            query = """UPDATE ponto SET endereco=%s, email=%s,
                       telefone=%s, propretario=%s WHERE id_ponto=%s"""
            cursor.execute(query, (
                dados["endereco"], dados["email"],
                dados["telefone"], dados["proprietario"], idponto
            ))
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
            cursor.execute("DELETE FROM ponto WHERE id_ponto=%s", (idponto,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()
                