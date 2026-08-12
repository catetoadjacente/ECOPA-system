import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

_pool = None


def _init_pool():
    global _pool
    if _pool is not None:
        return
    try:
        _pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="ecopa_pool",
            pool_size=10,
            pool_reset_session=True,
            **DB_CONFIG
        )
    except Error as e:
        print(f"Erro ao criar pool de conexoes: {e}")
        _pool = None


def get_connection():
    _init_pool()
    if _pool is None:
        return None
    try:
        return _pool.get_connection()
    except Error as e:
        print(f"Erro ao obter conexao do pool: {e}")
        return None


@contextmanager
def db_connection():
    """Context manager que garante fechamento da conexao."""
    conn = get_connection()
    if conn is None:
        yield None
        return
    try:
        yield conn
    finally:
        if conn.is_connected():
            conn.close()
