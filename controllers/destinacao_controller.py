from models.destinacao import Destinacao
from models.auditoria import Auditoria


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
        destinacao_id = Destinacao.criar(dados)
        if destinacao_id:
            Auditoria.registrar("CRIAR", "destinacao", destinacao_id, dados["nome"])
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
            Auditoria.registrar("ATUALIZAR", "destinacao", id_dest, "Dados da destinação atualizados")
            return True, "Destinacao atualizada com sucesso"
        return False, "Falha ao atualizar destinacao"

    @staticmethod
    def deletar(id_dest):
        if not id_dest:
            return False, "ID invalido"
        if Destinacao.deletar(id_dest):
            Auditoria.registrar("EXCLUIR", "destinacao", id_dest, "Destinação excluída")
            return True, "Destinacao excluida com sucesso"
        return False, "Falha ao excluir destinacao"

    @staticmethod
    def obter_por_id(id_dest):
        return Destinacao.buscar_por_id(id_dest)
