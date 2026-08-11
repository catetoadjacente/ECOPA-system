import logging
from database.conecta_database import db_connection

logger = logging.getLogger(__name__)


class BaseModel:
    """Classe base para models com helpers de acesso ao banco."""

    @staticmethod
    def _fetch_one(query, params=None):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                return cursor.fetchone()
            except Exception as e:
                logger.error("Erro ao buscar registro: %s", e)
                return None

    @staticmethod
    def _fetch_all(query, params=None):
        with db_connection() as conn:
            if conn is None:
                return []
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                return cursor.fetchall()
            except Exception as e:
                logger.error("Erro ao buscar registros: %s", e)
                return []

    @staticmethod
    def _execute(query, params=None):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                return True
            except Exception as e:
                logger.error("Erro ao executar query: %s", e)
                conn.rollback()
                return False

    @staticmethod
    def _execute_returning_id(query, params=None):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                logger.error("Erro ao executar query: %s", e)
                conn.rollback()
                return None
