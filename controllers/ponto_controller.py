from models.ponto import Ponto


class PontoController:
    @staticmethod
    def cadastrar(dados):
        erros = []
        if not dados.get("endereco"):
            erros.append("Endereco")
        if not dados.get("estabelecimento"):
            erros.append("Estabelecimento")
        if not dados.get("telefone"):
            erros.append("Telefone")
        if not dados.get("proprietario"):
            erros.append("Proprietario")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Ponto.criar(dados):
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
    def atualizar(idponto, dados):
        erros = []
        if not dados.get("endereco"):
            erros.append("Endereco")
        if not dados.get("email"):
            erros.append("Email")
        if not dados.get("telefone"):
            erros.append("Telefone")
        if not dados.get("proprietario"):
            erros.append("Proprietario")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Ponto.atualizar(idponto, dados):
            return True, "Ponto de coleta atualizado com sucesso"
        return False, "Falha ao atualizar ponto de coleta"

    @staticmethod
    def deletar(idponto):
        if not idponto:
            return False, "ID invalido"
        if Ponto.deletar(idponto):
            return True, "Ponto de coleta excluido com sucesso"
        return False, "Falha ao excluir ponto de coleta"
