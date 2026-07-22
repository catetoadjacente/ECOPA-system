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
            