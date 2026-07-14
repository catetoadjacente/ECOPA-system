from models.coleta import Coleta


class ColetaController:
    @staticmethod
    def listar():
        return Coleta.listar_todas()

    @staticmethod
    def cadastrar(dados):
        if Coleta.criar(dados):
            return True, "Coleta cadastrada com sucesso"
        return False, "Falha ao cadastrar coleta"

    @staticmethod
    def deletar(id_coleta):
        return Coleta.deletar(id_coleta)
