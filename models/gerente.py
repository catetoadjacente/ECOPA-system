from database.database import get_connection


class Gerente:
    @staticmethod
    def verificar_login(nome, senha):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            query = "SELECT senha FROM gerente WHERE nome = %s AND senha = %s LIMIT 1"
            cursor.execute(query, (nome, senha))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Erro ao verificar login: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def buscar_por_nome(nome):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM gerente WHERE nome = %s LIMIT 1"
            cursor.execute(query, (nome,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar gerente: {e}")
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
            query = """INSERT INTO gerente (idcpf, nome, Celular, email, senha, setor)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                dados["CPF"], dados["Nome"], dados["Celular"],
                dados["Email"], dados["Senha"], dados["Setor"]
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar gerente: {e}")
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
            query = "SELECT idcpf, nome, Celular, email, setor FROM gerente"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar gerentes: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()
    @staticmethod
    def buscar_por_cpf(cpf):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM gerente WHERE idcpf = %s LIMIT 1"
            cursor.execute(query, (cpf,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar gerente: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()            

    @staticmethod
    def atualizar(cpf, dados):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            query = """UPDATE gerente 
                       SET Celular = %s, email = %s, setor = %s
                       WHERE idcpf = %s"""
            cursor.execute(query, (
                dados["Celular"], dados["Email"],
                dados["Setor"], cpf
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar gerente: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def deletar(cpf):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            query = "DELETE FROM gerente WHERE idcpf = %s"
            cursor.execute(query, (cpf,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar gerente: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()
