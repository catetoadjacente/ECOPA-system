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
        cpf = dados.get("cpf", "")
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            erros.append("CPF (11 dígitos)")
        if not dados.get("nome"):
            erros.append("Nome")
        celular = dados.get("celular", "")
        if not celular or not celular.isdigit():
            erros.append("Celular (somente números)")
        email = dados.get("email", "")
        if not email or "@" not in email:
            erros.append("Email inválido")
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
    def obter_por_cpf(cpf):
        if not cpf:
            return None
        return Gerente.buscar_por_cpf(cpf)

    @staticmethod
    def atualizar(cpf, dados):
        erros = []
        celular = dados.get("celular", "")
        if not celular or not celular.isdigit():
            erros.append("Celular (somente números)")
        email = dados.get("email", "")
        if not email or "@" not in email:
            erros.append("Email inválido")
        if not dados.get("setor"):
            erros.append("Setor")
        if erros:
            return False, f"Preencha: {', '.join(erros)}"
        if Gerente.atualizar(cpf, dados):
            return True, "Gerente atualizado com sucesso"
        return False, "Falha ao atualizar gerente"

    @staticmethod
    def deletar(cpf):
        if not cpf:
            return False, "CPF invalido"
        if Gerente.deletar(cpf):
            return True, "Gerente excluido com sucesso"
        return False, "Falha ao excluir gerente"
