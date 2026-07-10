from models.gerente import Gerente


class GerenteController:
    @staticmethod
    def login(nome, senha):
        if not nome or not senha:
            return None, "Preencha usuario e senha"
        if Gerente.verificar_login(nome, senha):
            info = Gerente.buscar_por_nome(nome)
            return info, None
        return None, "Usuario ou senha invalidos"

    @staticmethod
    def cadastrar(dados):
        erros = []
        if not dados.get("idcpf"):
            erros.append("CPF")
        if not dados.get("nome"):
            erros.append("Nome")
        if not dados.get("Celular"):
            erros.append("Celular")
        if not dados.get("email"):
            erros.append("Email")
        if not dados.get("senha"):
            erros.append("Senha")
        if not dados.get("setor"):
            erros.append("Setor")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Gerente.criar(dados):
            return True, "Gerente cadastrado com sucesso"
        return False, "Falha ao cadastrar gerente"

    @staticmethod
    def listar():
        return Gerente.listar()

    @staticmethod
    def obter_por_idcpf(idcpf):
        if not idcpf:
            return None
        return Gerente.buscar_por_idcpf(idcpf)

    @staticmethod
    def atualizar(idcpf, dados):
        erros = []
        if not dados.get("Celular"):
            erros.append("Celular")
        if not dados.get("email"):
            erros.append("Email")
        if not dados.get("setor"):
            erros.append("Setor")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Gerente.atualizar(idcpf, dados):
            return True, "Gerente atualizado com sucesso"
        return False, "Falha ao atualizar gerente"

    @staticmethod
    def deletar(idcpf):
        if not idcpf:
            return False, "CPF invalido"
        if Gerente.deletar(idcpf):
            return True, "Gerente excluido com sucesso"
        return False, "Falha ao excluir gerente"
    