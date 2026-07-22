from models.coleta import Coleta
from models.ponto import Ponto
from models.lote import Lote


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
    def atualizar_status(id_coleta, status):
        if status == "Realizada":
            lote_existente = Lote.buscar_por_coleta(id_coleta)
            if lote_existente is None:
                coletas = Coleta.listar_todas()
                coleta = next((c for c in coletas if c["id"] == id_coleta), None)
                if coleta:
                    Lote.criar_por_coleta(id_coleta, coleta["quantidade"])
        return Coleta.atualizar_status(id_coleta, status)
    
    def deletar(id_coleta):
        return Coleta.deletar(id_coleta)
