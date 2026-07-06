from models.coleta import Coleta


class ColetaController:
    @staticmethod
    def listar():
        return Coleta.listar_todas()

    @staticmethod
    def cadastrar(dados):
        return Coleta.criar(dados)

    @staticmethod
    def atualizar_status(id_coleta, status):
        return Coleta.atualizar_status(id_coleta, status)