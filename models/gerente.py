from database.conecta_database import db_connection


class Gerente:
    @staticmethod
    def verificar_login(nome, senha):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT senha FROM gerente WHERE nome = %s AND senha = %s LIMIT 1",
                    (nome, senha))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Erro ao verificar login: {e}")
                return False

    @staticmethod
    def autenticar_e_buscar(nome, senha):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT cpf, nome, celular, email, setor FROM gerente WHERE nome = %s AND senha = %s LIMIT 1",
                    (nome, senha)
                )
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao autenticar: {e}")
                return None

    @staticmethod
    def buscar_por_nome(nome):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM gerente WHERE nome = %s LIMIT 1", (nome,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar gerente: {e}")
                return None

    @staticmethod
    def criar(dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO gerente (cpf, nome, celular, email, senha, setor) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (dados["cpf"], dados["nome"], dados["celular"],
                     dados["email"], dados["senha"], dados["setor"]))
                conn.commit()
                return True
            except Exception as e:
                print(f"Erro ao criar gerente: {e}")
                return False

    @staticmethod
    def listar():
        with db_connection() as conn:
            if conn is None:
                return []
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT cpf, nome, celular, email, setor FROM gerente")
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao listar gerentes: {e}")
                return []

    @staticmethod
    def buscar_por_email(email):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM gerente WHERE email = %s LIMIT 1", (email,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar gerente por email: {e}")
                return None

    @staticmethod
    def buscar_por_cpf(cpf):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM gerente WHERE cpf = %s LIMIT 1", (cpf,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar gerente: {e}")
                return None

    @staticmethod
    def atualizar(cpf, dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE gerente SET celular = %s, email = %s, setor = %s WHERE cpf = %s",
                    (dados["celular"], dados["email"], dados["setor"], cpf))
                conn.commit()
                return True
            except Exception as e:
                print(f"Erro ao atualizar gerente: {e}")
                return False

    @staticmethod
    def deletar(cpf):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE coleta SET gerente_cpf = NULL WHERE gerente_cpf = %s", (cpf,))
                cursor.execute("DELETE FROM gerente WHERE cpf = %s", (cpf,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Erro ao deletar gerente: {e}")
                return False
