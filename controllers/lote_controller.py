from models.lote import Lote


class LoteController:

    @staticmethod
    def criar_por_coleta(id_coleta, quantidade):
        if not id_coleta:
            return False, "Coleta invalida"
        if not quantidade or float(quantidade) <= 0:
            return False, "Quantidade invalida"
        if Lote.criar_por_coleta(id_coleta, quantidade):
            return True, "Lote criado com sucesso"
        return False, "Falha ao criar lote"

    @staticmethod
    def listar_disponiveis():
        return Lote.listar_disponiveis()

    @staticmethod
    def listar_todos():
        return Lote.listar_todos()

    @staticmethod
    def consumir(id_lote, quantidade):
        if not id_lote:
            return False, "Lote invalido"
        if not quantidade or float(quantidade) <= 0:
            return False, "Quantidade invalida"
        if Lote.consumir(id_lote, quantidade):
            return True, "Estoque atualizado"
        return False, "Falha ao consumir lote (estoque insuficiente)"

    @staticmethod
    def obter_por_id(id_lote):
        return Lote.obter_por_id(id_lote)

    @staticmethod
    def buscar_por_coleta(id_coleta):
        return Lote.buscar_por_coleta(id_coleta)
