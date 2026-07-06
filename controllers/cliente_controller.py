from models.cliente import Cliente
from datetime import datetime


class ClienteController:
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
        if not dados.get("cnpj"):
            erros.append("CNPJ")
        if not dados.get("cliente"):
            erros.append("Cliente")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        dados["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if Cliente.criar(dados):
            return True, "Ponto de coleta cadastrado com sucesso"
        return False, "Falha ao cadastrar ponto de coleta"

    @staticmethod
    def listar():
        return Cliente.listar()

    @staticmethod
    def buscar_por_idponto(idponto):
        if not idponto:
            return None
        return Cliente.buscar_por_idponto(idponto)

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
        if Cliente.atualizar(idponto, dados):
            return True, "Ponto de coleta atualizado com sucesso"
        return False, "Falha ao atualizar ponto de coleta"

    @staticmethod
    def deletar(idponto):
        if not idponto:
            return False, "ID invalido"
        if Cliente.deletar(idponto):
            return True, "Ponto de coleta excluido com sucesso"
        return False, "Falha ao excluir ponto de coleta"
