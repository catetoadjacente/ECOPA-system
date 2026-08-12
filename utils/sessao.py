"""Contexto do usuário autenticado na execução atual do aplicativo."""

_usuario_logado = None


def iniciar(usuario):
    """Armazena os dados mínimos do gerente autenticado."""
    global _usuario_logado
    _usuario_logado = usuario.copy() if usuario else None


def usuario_atual():
    return _usuario_logado


def encerrar():
    global _usuario_logado
    _usuario_logado = None
