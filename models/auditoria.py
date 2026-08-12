import logging

from models.base import BaseModel
from utils.sessao import usuario_atual

logger = logging.getLogger(__name__)


class Auditoria(BaseModel):
    """Registra ações relevantes realizadas por usuários autenticados."""

    @staticmethod
    def registrar(acao, entidade, registro_id, detalhes=None):
        usuario = usuario_atual()
        if not usuario or not usuario.get("cpf"):
            logger.warning("Ação sem usuário autenticado não foi auditada: %s %s", acao, entidade)
            return False

        return BaseModel._execute(
            """
            INSERT INTO auditoria
                (gerente_cpf, acao, entidade, registro_id, detalhes)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (usuario["cpf"], acao, entidade, registro_id, detalhes),
        )

    @staticmethod
    def listar(data_inicio=None, data_fim=None, gerente=None, acao=None,
               entidade=None, limit=500):
        filtros, params = [], []
        if data_inicio:
            filtros.append("a.criado_em >= %s")
            params.append(data_inicio)
        if data_fim:
            filtros.append("a.criado_em <= %s")
            params.append(data_fim)
        if gerente:
            filtros.append("g.nome LIKE %s")
            params.append(f"%{gerente}%")
        if acao and acao != "TODAS":
            filtros.append("a.acao = %s")
            params.append(acao)
        if entidade and entidade != "TODAS":
            filtros.append("a.entidade = %s")
            params.append(entidade)
        where = f"WHERE {' AND '.join(filtros)}" if filtros else ""
        params.append(limit)
        return BaseModel._fetch_all(
            f"""
            SELECT a.id_auditoria, a.acao, a.entidade, a.registro_id,
                   a.detalhes, a.criado_em, g.nome AS gerente
            FROM auditoria a
            LEFT JOIN gerente g ON g.cpf = a.gerente_cpf
            {where}
            ORDER BY a.criado_em DESC
            LIMIT %s
            """,
            tuple(params),
        )
