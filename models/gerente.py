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
            query = "INSERT INTO gerente (idcpf, nome, Celular, email, senha, setor) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (
                dados["idcpf"], dados["nome"], dados["Celular"],
                dados["email"], dados["senha"], dados["setor"]
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
            cursor.execute("SELECT idcpf, nome, Celular, email, setor FROM gerente")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar gerentes: {e}")
            return []
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
<<<<<<< HEAD
    def buscar_por_idcpf(idcpf):
=======
    def buscar_por_email(email):
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM gerente WHERE email = %s LIMIT 1"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar gerente por email: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def buscar_por_cpf(cpf):
>>>>>>> main
        connection = get_connection()
        if connection is None:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM gerente WHERE idcpf = %s LIMIT 1", (idcpf,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar gerente: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def atualizar(idcpf, dados):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE gerente SET Celular = %s, email = %s, setor = %s WHERE idcpf = %s",
                (dados["Celular"], dados["email"], dados["setor"], idcpf)
            )
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar gerente: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def deletar(idcpf):
        connection = get_connection()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM gerente WHERE idcpf = %s", (idcpf,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar gerente: {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()
                