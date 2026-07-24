from database.conecta_database import db_connection
from database.cache import get_cached, invalidate_prefix


class Destinacao:

    @staticmethod
    def listar_todas():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return []
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT id_destinacao AS id, nome, tipo, endereco,
                               telefone, email, cnpj
                        FROM destinacao
                        ORDER BY nome ASC
                    """)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar destinacoes: {e}")
                    return []
        return get_cached("destinacoes_listar", 60, _fetch)

    @staticmethod
    def criar(dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO destinacao (nome, tipo, endereco, telefone, email, cnpj) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (dados["nome"], dados["tipo"], dados["endereco"],
                     dados.get("telefone", ""), dados.get("email", ""),
                     dados.get("cnpj", "")))
                conn.commit()
                invalidate_prefix("destinacoes")
                invalidate_prefix("pedidos")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao criar destinacao: {e}")
                conn.rollback()
                return False

    @staticmethod
    def atualizar(id_dest, dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE destinacao SET nome=%s, tipo=%s, endereco=%s, telefone=%s, email=%s, cnpj=%s "
                    "WHERE id_destinacao=%s",
                    (dados["nome"], dados["tipo"], dados["endereco"],
                     dados.get("telefone", ""), dados.get("email", ""),
                     dados.get("cnpj", ""), id_dest))
                conn.commit()
                invalidate_prefix("destinacoes")
                invalidate_prefix("pedidos")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao atualizar destinacao: {e}")
                conn.rollback()
                return False

    @staticmethod
    def deletar(id_dest):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM destinacao WHERE id_destinacao=%s", (id_dest,))
                conn.commit()
                invalidate_prefix("destinacoes")
                invalidate_prefix("pedidos")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao deletar destinacao: {e}")
                conn.rollback()
                return False

    @staticmethod
    def buscar_por_id(id_dest):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT id_destinacao AS id, nome, tipo, endereco,
                           telefone, email, cnpj
                    FROM destinacao
                    WHERE id_destinacao = %s
                """, (id_dest,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar destinacao: {e}")
                return None

    @staticmethod
    def buscar_por_cnpj(cnpj):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT id_destinacao AS id, nome, tipo, endereco,
                           telefone, email, cnpj
                    FROM destinacao
                    WHERE cnpj = %s
                """, (cnpj,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar destinacao por CNPJ: {e}")
                return None
