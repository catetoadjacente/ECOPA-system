from database.database import get_connection


class Cliente:
    @staticmethod
    def listar():
        connection = get_connection()
        if connection is None:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.idponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.propretario as proprietario,
                       d.iddeatinacoes, d.cnpj, d.cliente as cliente_nome, d.data
                FROM ponto p
                LEFT JOIN deatinacoes d ON p.estabelecimento = d.cliente
                ORDER BY p.estabelecimento
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
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
                INSERT INTO ponto (idponto, endereco, email, estabelecimento,
                                   telefone, propretario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (dados["idponto"], dados["endereco"], dados["email"],
                  dados["estabelecimento"], dados["telefone"], dados["proprietario"]))
            cursor.execute("""
                INSERT INTO deatinacoes (iddeatinacoes, cnpj, cliente, data)
                VALUES (%s, %s, %s, %s)
            """, (dados["iddeatinacoes"], dados["cnpj"], dados["cliente"], dados["data"]))
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
    def buscar_por_idponto(idponto):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.idponto, p.endereco, p.email, p.estabelecimento,
                       p.telefone, p.propretario as proprietario,
                       d.iddeatinacoes, d.cnpj, d.cliente as cliente_nome, d.data
                FROM ponto p
                LEFT JOIN deatinacoes d ON p.estabelecimento = d.cliente
                WHERE p.idponto = %s LIMIT 1
            """, (idponto,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
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
                UPDATE ponto SET endereco=%s, email=%s,
                       telefone=%s, propretario=%s WHERE idponto=%s
            """, (dados["endereco"], dados["email"],
                  dados["telefone"], dados["proprietario"], idponto))
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
            cursor.execute("DELETE FROM ponto WHERE idponto=%s", (idponto,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                connection.close()