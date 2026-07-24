from database.conecta_database import db_connection
from database.cache import get_cached, invalidate, invalidate_prefix


class Ponto:
    @staticmethod
    def buscar_por_estabelecimento(estabelecimento):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT id_ponto FROM ponto_de_coleta WHERE estabelecimento = %s LIMIT 1",
                    (estabelecimento,)
                )
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar ponto por estabelecimento: {e}")
                return None

    @staticmethod
    def buscar_por_idponto(idponto):
        with db_connection() as conn:
            if conn is None:
                return None
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                           p.telefone, p.proprietario
                    FROM ponto_de_coleta p
                    WHERE p.id_ponto = %s LIMIT 1
                """, (idponto,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Erro ao buscar ponto de coleta: {e}")
                return None

    @staticmethod
    def criar(dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO ponto_de_coleta (endereco, email, estabelecimento,
                                                 telefone, proprietario)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    dados["endereco"], dados["email"],
                    dados["estabelecimento"], dados["telefone"], dados["proprietario"]
                ))
                conn.commit()
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao criar ponto de coleta: {e}")
                conn.rollback()
                return False

    @staticmethod
    def listar():
        def _fetch():
            with db_connection() as conn:
                if conn is None:
                    return []
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT p.id_ponto, p.endereco, p.email, p.estabelecimento,
                               p.telefone, p.proprietario
                        FROM ponto_de_coleta p
                        ORDER BY p.estabelecimento
                    """)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar pontos de coleta: {e}")
                    return []
        return get_cached("pontos_listar", 60, _fetch)

    @staticmethod
    def atualizar(idponto, dados):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE ponto_de_coleta
                    SET endereco=%s, email=%s, telefone=%s, proprietario=%s
                    WHERE id_ponto=%s
                """, (
                    dados["endereco"], dados["email"],
                    dados["telefone"], dados["proprietario"], idponto
                ))
                conn.commit()
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao atualizar ponto de coleta: {e}")
                conn.rollback()
                return False

    @staticmethod
    def deletar(idponto):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ponto_de_coleta WHERE id_ponto=%s", (idponto,))
                conn.commit()
                invalidate_prefix("pontos")
                invalidate_prefix("dashboard")
                invalidate_prefix("relatorio")
                return True
            except Exception as e:
                print(f"Erro ao deletar ponto de coleta: {e}")
                conn.rollback()
                return False

    @staticmethod
    def salvar_horarios(id_ponto, horarios):
        with db_connection() as conn:
            if conn is None:
                return False
            try:
                cursor = conn.cursor()
                cursor.start_transaction()
                cursor.execute(
                    "DELETE FROM horario_ponto WHERE ponto_de_coleta_id_ponto = %s",
                    (id_ponto,)
                )
                for h in horarios:
                    cursor.execute("""
                        INSERT INTO horario_ponto
                        (dia_semana, abertura, fechamento, ativo, ponto_de_coleta_id_ponto)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (h["dia_semana"], h["abertura"], h["fechamento"],
                        h["ativo"], id_ponto))
                conn.commit()
                return True
            except Exception as e:
                print(f"Erro ao salvar horarios: {e}")
                conn.rollback()
                return False

    @staticmethod
    def buscar_horarios(id_ponto):
        with db_connection() as conn:
            if conn is None:
                return []
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM horario_ponto WHERE ponto_de_coleta_id_ponto = %s ORDER BY dia_semana",
                    (id_ponto,)
                )
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao buscar horarios: {e}")
                return []
