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
        
        # Agora usa `nome` como usuário e `senha` como senha
        query = "SELECT senha FROM gerente WHERE nome = %s AND senha = %s LIMIT 1"
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

def get_all_gerentes():
    """Retorna lista de todos os gerentes cadastrados"""
    connection = get_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT cpf, nome, celular, email, setor FROM gerente ORDER BY nome"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        print(f"Erro ao buscar gerentes: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            

def cadastrar_cliente(dados):
    connection = get_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO ponto (endereco, email, estabelecimento,
                               telefone, propretario)
            VALUES (%s, %s, %s, %s, %s)
        """, (dados["endereco"], dados["email"],
              dados["estabelecimento"], dados["telefone"], dados["proprietario"]))

        cursor.execute("""
            INSERT INTO destinacoes (cnpj, cliente, data, coleta_id_coleta)
            VALUES (%s, %s, %s, %s)
        """, (dados["cnpj"],
              dados["cliente"], dados["data"], dados.get("coleta_id_coleta")))

        connection.commit()
        cursor.close()
        return True
    except Error as e:
        print(f"Erro ao cadastrar cliente: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            connection.close() 

def get_all_clientes():
    connection = get_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT p.id_ponto, p.estabelecimento, p.endereco, p.email,
                   p.telefone, p.propretario,
                   d.id_destinacoes, d.cnpj, d.cliente, d.data
            FROM ponto p
            LEFT JOIN destinacoes d ON p.estabelecimento = d.cliente
            ORDER BY p.estabelecimento
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        print(f"Erro ao buscar clientes: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            