from models.ponto import Ponto


class PontoController:
    @staticmethod
    def cadastrar(dados, horarios=None):
        erros = []
        if not dados.get("endereco"):
            erros.append("Endereco")
        if not dados.get("estabelecimento"):
            erros.append("Estabelecimento")
        telefone = dados.get("telefone", "")
        if not telefone or not telefone.isdigit():
            erros.append("Telefone (somente números)")
        if not dados.get("proprietario"):
            erros.append("Proprietario")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Ponto.criar(dados):
            ponto = Ponto.buscar_por_estabelecimento(dados["estabelecimento"])
            if ponto and horarios:
                Ponto.salvar_horarios(ponto["id_ponto"], horarios)
            return True, "Ponto de coleta cadastrado com sucesso"
        return False, "Falha ao cadastrar ponto de coleta"

    @staticmethod
    def listar():
        return Ponto.listar()

    @staticmethod
    def buscar_por_idponto(idponto):
        if not idponto:
            return None
        return Ponto.buscar_por_idponto(idponto)

    @staticmethod
    def atualizar(idponto, dados, horarios=None):
        erros = []
        if not dados.get("endereco"):
            erros.append("Endereco")
        if not dados.get("email"):
            erros.append("Email")
        telefone = dados.get("telefone", "")
        if not telefone or not telefone.isdigit():
            erros.append("Telefone (somente números)")
        if not dados.get("proprietario"):
            erros.append("Proprietario")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Ponto.atualizar(idponto, dados):
            if horarios:
                Ponto.salvar_horarios(idponto, horarios)
            return True, "Ponto de coleta atualizado com sucesso"
        return False, "Falha ao atualizar ponto de coleta"

    @staticmethod
    def deletar(idponto):
        if not idponto:
            return False, "ID invalido"
        if Ponto.deletar(idponto):
            return True, "Ponto de coleta excluido com sucesso"
        return False, "Falha ao excluir ponto de coleta"
