from models.cliente import Cliente


class ClienteController:
    @staticmethod
    def listar():
        return Cliente.listar()

    @staticmethod
    def cadastrar(dados):
        return Cliente.criar(dados)

    @staticmethod
    def buscar_por_idponto(idponto):
        return Cliente.buscar_por_idponto(idponto)

    @staticmethod
    def atualizar(idponto, dados):
        return Cliente.atualizar(idponto, dados)

    @staticmethod
    def deletar(idponto):
        return Cliente.deletar(idponto)