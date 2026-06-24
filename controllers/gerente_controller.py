from models.gerente import Gerente


class GerenteController:
    @staticmethod
    def login(nome, senha):
        return Gerente.verificar_login(nome, senha)

    @staticmethod
    def obter_info(nome):
        return Gerente.buscar_por_nome(nome)

    @staticmethod
    def cadastrar(dados):
        return Gerente.criar(dados)
    
    @staticmethod
    def listar():
        return Gerente.listar()
    
    @staticmethod
    def obter_info_por_cpf(cpf):
        return Gerente.buscar_por_cpf(cpf)

    @staticmethod
    def atualizar(cpf, dados):
        return Gerente.atualizar(cpf, dados)

    @staticmethod
    def deletar(cpf):
        return Gerente.deletar(cpf)
