from models.destinacao import Destinacao


class DestinacaoController:

    @staticmethod
    def listar():
        return Destinacao.listar_todas()

    @staticmethod
    def cadastrar(dados):
        erros = []
        if not dados.get("nome") or not dados["nome"].strip():
            erros.append("Nome")
        if not dados.get("tipo"):
            erros.append("Tipo")
        if not dados.get("endereco") or not dados["endereco"].strip():
            erros.append("Endereco")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if dados.get("cnpj"):
            existente = Destinacao.buscar_por_cnpj(dados["cnpj"].strip())
            if existente:
                return False, "CNPJ ja cadastrado"
        if Destinacao.criar(dados):
            return True, "Destinacao cadastrada com sucesso"
        return False, "Falha ao cadastrar destinacao"

    @staticmethod
    def atualizar(id_dest, dados):
        erros = []
        if not dados.get("nome") or not dados["nome"].strip():
            erros.append("Nome")
        if not dados.get("tipo"):
            erros.append("Tipo")
        if not dados.get("endereco") or not dados["endereco"].strip():
            erros.append("Endereco")
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
    def obter_por_id(id_dest):
        return Destinacao.buscar_por_id(id_dest)
