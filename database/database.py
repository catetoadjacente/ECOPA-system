import mysql.connector
from mysql.connector import Error

# Configuração do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Adicione a senha se houver
    'database': 'ecopa_system'
}


def get_connection():
    """Estabelece conexão com o banco de dados"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def verify_login(user, password):
    """
    Verifica se o usuário e senha estão corretos
    Retorna True se válido, False caso contrário
    """
    connection = get_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Agora usa `nome` como usuário e `cpf` como senha
        query = "SELECT cpf FROM gerente WHERE nome = %s AND cpf = %s LIMIT 1"
        cursor.execute(query, (user, password))
        
        result = cursor.fetchone()
        cursor.close()
        
        return result is not None
        
    except Error as e:
        print(f"Erro ao verificar login: {e}")
        return False
    finally:
        if connection.is_connected():
            connection.close()


def register_user(nome, cpf, email, senha, telefone=""):
    """Cadastra um novo gerente no banco de dados"""
    connection = get_connection()
    if connection is None:
        return False, "Erro de conexão com o banco de dados!"

    try:
        cursor = connection.cursor()

        query_check = "SELECT id FROM gerente WHERE cpf = %s OR email = %s LIMIT 1"
        cursor.execute(query_check, (cpf, email))
        if cursor.fetchone():
            cursor.close()
            return False, "CPF ou Email já cadastrados!"

        query_insert = """INSERT INTO gerente (nome, cpf, email, senha, telefone)
                          VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query_insert, (nome, cpf, email, senha, telefone))
        connection.commit()
        cursor.close()
        return True, "Cadastro realizado com sucesso!"

    except Error as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False, f"Erro ao cadastrar: {e}"
    finally:
        if connection.is_connected():
            connection.close()


def get_user_info(user):
    """Obtém informações do usuário logado"""
    connection = get_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        # Busca pelo nome, já que o campo usuário agora é `nome`
        query = "SELECT * FROM gerente WHERE nome = %s LIMIT 1"
        cursor.execute(query, (user,))
        
        result = cursor.fetchone()
        cursor.close()
        
        return result
        
    except Error as e:
        print(f"Erro ao obter informações do usuário: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
