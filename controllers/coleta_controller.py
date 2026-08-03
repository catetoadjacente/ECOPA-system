from models.coleta import Coleta
from models.ponto import Ponto
from models.lote import Lote


class ColetaController:
    @staticmethod
    def listar():
        return Coleta.listar_todas()

    @staticmethod
    def cadastrar(dados):
        ponto_dados = Ponto.buscar_por_estabelecimento(dados["ponto"])
        if ponto_dados is None:
            return False, "Ponto de coleta nao encontrado"

        dados["ponto"] = ponto_dados["id_ponto"]

        if Coleta.criar(dados):
            return True, "Coleta cadastrada com sucesso"
        return False, "Falha ao cadastrar coleta"

    @staticmethod
    def atualizar_status(id_coleta, status):
        if status == "Realizada":
            coleta = Coleta.buscar_por_id(id_coleta)
            if not coleta:
                return False
            lote_existente = Lote.buscar_por_coleta(id_coleta)
            if lote_existente is not None:
                return Coleta.atualizar_status(id_coleta, status)
            if float(coleta["quantidade"]) <= 0:
                return False
            if not Lote.criar_por_coleta(id_coleta, coleta["quantidade"]):
                return False
        return Coleta.atualizar_status(id_coleta, status)
