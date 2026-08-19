from models.coleta import Coleta
from models.ponto import Ponto
from models.lote import Lote
from models.auditoria import Auditoria
from utils.sessao import usuario_atual


class ColetaController:
    @staticmethod
    def listar():
        return Coleta.listar_todas()

    @staticmethod
    def cadastrar(dados):
        usuario = usuario_atual()
        if not usuario or not usuario.get("cpf"):
            return False, "Nenhum gerente autenticado"

        ponto_dados = Ponto.buscar_por_estabelecimento(dados["ponto"])
        if ponto_dados is None:
            return False, "Ponto de coleta nao encontrado"

        dados["ponto"] = ponto_dados["id_ponto"]
        dados["gerente_cpf"] = usuario["cpf"]

        coleta_id = Coleta.criar(dados)
        if coleta_id:
            Auditoria.registrar("CRIAR", "coleta", coleta_id, f"Coleta cadastrada no ponto {dados['ponto']}")
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
                atualizado = Coleta.atualizar_status(id_coleta, status)
                if atualizado:
                    Auditoria.registrar("ATUALIZAR_STATUS", "coleta", id_coleta, f"Status alterado para {status}")
                return atualizado
            if float(coleta["quantidade"]) <= 0:
                return False
            if not Lote.criar_por_coleta(id_coleta, coleta["quantidade"]):
                return False
        atualizado = Coleta.atualizar_status(id_coleta, status)
        if atualizado:
            Auditoria.registrar("ATUALIZAR_STATUS", "coleta", id_coleta, f"Status alterado para {status}")
        return atualizado
