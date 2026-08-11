from models.pedido import Pedido
from models.lote import Lote


class PedidoController:

    @staticmethod
    def listar():
        return Pedido.listar_todos()

    @staticmethod
    def cadastrar(dados):
        erros = []
        if not dados.get("id_destinacao"):
            erros.append("Destinacao")
        if not dados.get("quantidade_solicitada") or float(dados["quantidade_solicitada"]) <= 0:
            erros.append("Quantidade solicitada")
        if erros:
            return False, f"Preencha: {', '.join(erros)}", None
        lotes = Lote.listar_disponiveis()
        if not lotes:
            return False, "Nenhum lote disponivel no estoque", None
        estoque_total = sum(float(l["quantidade_restante"]) for l in lotes)
        qtd_solicitada = float(dados["quantidade_solicitada"])
        if estoque_total < qtd_solicitada:
            return False, f"Estoque insuficiente (disponivel: {estoque_total:.1f}, solicitado: {qtd_solicitada:.1f})", None
        pedido_id = Pedido.criar(dados)
        if pedido_id:
            return True, f"Pedido #{pedido_id} criado com sucesso", pedido_id
        return False, "Falha ao criar pedido", None

    @staticmethod
    def vincular_lotes(id_pedido, lotes):
        if not id_pedido:
            return False, "Pedido invalido"
        total_atendido = Pedido.vincular_lotes_batch(id_pedido, lotes)
        pedido = Pedido.obter_por_id(id_pedido)
        if pedido:
            solicitada = float(pedido["quantidade_solicitada"])
            if total_atendido >= solicitada:
                Pedido.atualizar_status(id_pedido, "Atendido")
            elif total_atendido > 0:
                Pedido.atualizar_status(id_pedido, "Atendido Parcialmente")
        return True, f"Estoque distribuido: {total_atendido:.1f}"

    @staticmethod
    def distribuir_automatico(id_pedido):
        """Distribui estoque automaticamente usando lotes disponiveis.

        Estrategia:
        1. Priorizar lotes 'Parcialmente Consumido' (mais antigos primeiro)
        2. Depois usar lotes 'Disponivel' (FIFO - mais antigos primeiro)
        Isso evita ter muitos lotes pela metade abertos ao mesmo tempo.
        """
        if not id_pedido:
            return False, "Pedido invalido"

        pedido = Pedido.obter_por_id(id_pedido)
        if not pedido:
            return False, "Pedido nao encontrado"

        if pedido["status"] == "Atendido":
            return False, "Pedido ja foi totalmente atendido"

        solicitada = float(pedido["quantidade_solicitada"])
        ja_atendida = float(pedido["quantidade_atendida"])
        falta = solicitada - ja_atendida

        if falta <= 0:
            return False, "Pedido ja totalmente atendido"

        lotes = Lote.listar_disponiveis()
        if not lotes:
            return False, "Nenhum lote disponivel no estoque"

        total_disponivel = sum(float(l["quantidade_restante"]) for l in lotes)
        if total_disponivel <= 0:
            return False, "Nenhum lote disponivel no estoque"

        parciais = [l for l in lotes if l["status"] == "Parcialmente Consumido"]
        novos = [l for l in lotes if l["status"] != "Parcialmente Consumido"]
        parciais.sort(key=lambda l: l["data_criacao"])
        novos.sort(key=lambda l: l["data_criacao"])
        lotes_ordenados = parciais + novos

        lotes_para_vincular = []
        restante = falta
        for lote in lotes_ordenados:
            if restante <= 0:
                break
            disp = float(lote["quantidade_restante"])
            if disp <= 0:
                continue
            qtd = min(disp, restante)
            lotes_para_vincular.append((lote["id"], qtd))
            restante -= qtd

        if not lotes_para_vincular:
            return False, "Nao foi possivel alocar lotes"

        total_atendido = Pedido.vincular_lotes_batch(id_pedido, lotes_para_vincular)

        pedido = Pedido.obter_por_id(id_pedido)
        if pedido:
            nova_total = float(pedido["quantidade_atendida"])
            if nova_total >= solicitada:
                Pedido.atualizar_status(id_pedido, "Atendido")
            elif nova_total > 0:
                Pedido.atualizar_status(id_pedido, "Atendido Parcialmente")

        if total_atendido < falta:
            return True, f"Parcialmente distribuido: {total_atendido:.1f} de {falta:.1f} Kg"
        return True, f"Estoque distribuido: {total_atendido:.1f} Kg"

    @staticmethod
    def deletar(id_pedido):
        if not id_pedido:
            return False, "ID invalido"
        if Pedido.deletar(id_pedido):
            return True, "Pedido excluido com sucesso"
        return False, "Falha ao excluir pedido"

    @staticmethod
    def obter_por_id(id_pedido):
        return Pedido.obter_por_id(id_pedido)

    @staticmethod
    def listar_lotes_do_pedido(id_pedido):
        return Pedido.listar_lotes_do_pedido(id_pedido)
