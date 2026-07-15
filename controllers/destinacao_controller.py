from models.destinacao import Destinacao


class DestinacaoController:
    @staticmethod
    def listar():
        return Destinacao.listar_todas()

    @staticmethod
    def cadastrar(dados):
        erros = []
        if not dados.get("cnpj") or not dados["cnpj"].strip():
            erros.append("CNPJ")
        if not dados.get("cliente") or not dados["cliente"].strip():
            erros.append("Cliente")
        if not dados.get("data") or not dados["data"].strip():
            erros.append("Data")
        if not dados.get("coleta_id_coleta"):
            erros.append("Coleta vinculada")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Destinacao.criar(dados):
            return True, "Destinacao cadastrada com sucesso"
        return False, "Falha ao cadastrar destinacao"

    @staticmethod
    def atualizar(id_dest, dados):
        erros = []
        if not dados.get("cnpj") or not dados["cnpj"].strip():
            erros.append("CNPJ")
        if not dados.get("cliente") or not dados["cliente"].strip():
            erros.append("Cliente")
        if not dados.get("data") or not dados["data"].strip():
            erros.append("Data")
        if not dados.get("coleta_id_coleta"):
            erros.append("Coleta vinculada")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Destinacao.atualizar(id_dest, dados):
            return True, "Destinacao atualizada com sucesso"
        return False, "Falha ao atualizar destinacao"

    @staticmethod
    def deletar(id_dest):
        if not id_dest:
            return False, "ID invalido"
        if Destinacao.deletar(id_dest):
            return True, "Destinacao excluida com sucesso"
        return False, "Falha ao excluir destinacao"

    @staticmethod
    def coletas_disponiveis():
        return Destinacao.listar_coletas_disponiveis()
