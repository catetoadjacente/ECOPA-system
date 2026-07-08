from models.coleta import Coleta
from models.cliente import Cliente


class ColetaController:
    @staticmethod
    def listar():
        return Coleta.listar_todas()

    @staticmethod
    def cadastrar(dados):
        ponto_dados = Cliente.buscar_por_estabelecimento(dados["ponto"])
        if ponto_dados is None:
            return False, "Ponto de coleta nao encontrado"

        dados["ponto"] = ponto_dados["id_ponto"]

        if Coleta.criar(dados):
            return True, "Coleta cadastrada com sucesso"
        return False, "Falha ao cadastrar coleta"

    @staticmethod
    def atualizar_status(id_coleta, status):
        return Coleta.atualizar_status(id_coleta, status)
