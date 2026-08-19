import logging
from database.conecta_database import db_connection

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Erro generico de banco de dados."""
    pass


class ConnectionError(DatabaseError):
    """Falha ao obter conexao com o banco."""
    pass


class QueryError(DatabaseError):
    """Erro ao executar query SQL."""
    pass


class BaseModel:
    """Classe base para models com helpers de acesso ao banco.

    Comportamento:
      - _fetch_one: retorna dict (registro) ou None (sem resultado). Erro de BD -> QueryError.
      - _fetch_all: retorna list[dict] ([] se vazio). Erro de BD -> QueryError.
      - _execute: retorna True (sucesso). Erro de BD -> QueryError.
      - _execute_returning_id: retorna int (lastrowid). Erro de BD -> QueryError.
      - Conexao indisponivel -> ConnectionError.
    """

    @staticmethod
    def _fetch_one(query, params=None):
        with db_connection() as conn:
            if conn is None:
                raise ConnectionError("Sem conexao com o banco de dados")
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                return cursor.fetchone()
            except Exception as e:
                logger.error("Erro ao buscar registro: %s", e)
                raise QueryError(str(e)) from e

    @staticmethod
    def _fetch_all(query, params=None):
        with db_connection() as conn:
            if conn is None:
                raise ConnectionError("Sem conexao com o banco de dados")
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                return cursor.fetchall()
            except Exception as e:
                logger.error("Erro ao buscar registros: %s", e)
                raise QueryError(str(e)) from e

    @staticmethod
    def _execute(query, params=None):
        with db_connection() as conn:
            if conn is None:
                raise ConnectionError("Sem conexao com o banco de dados")
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                return True
            except Exception as e:
                logger.error("Erro ao executar query: %s", e)
                conn.rollback()
                raise QueryError(str(e)) from e

    @staticmethod
    def _execute_returning_id(query, params=None):
        with db_connection() as conn:
            if conn is None:
                raise ConnectionError("Sem conexao com o banco de dados")
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                logger.error("Erro ao executar query: %s", e)
                conn.rollback()
                raise QueryError(str(e)) from e
