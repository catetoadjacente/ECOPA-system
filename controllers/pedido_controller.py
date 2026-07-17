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
        estoque_total = sum(float(l["quantidade_restante"]) for l in lotes)
        if estoque_total < float(dados["quantidade_solicitada"]):
            return False, f"Estoque insuficiente (disponivel: {estoque_total:.1f})", None
        pedido_id = Pedido.criar(dados)
        if pedido_id:
            return True, f"Pedido #{pedido_id} criado com sucesso", pedido_id
        return False, "Falha ao criar pedido", None

    @staticmethod
    def vincular_lotes(id_pedido, lotes):
        if not id_pedido:
            return False, "Pedido invalido"
        total_atendido = 0
        for id_lote, quantidade in lotes:
            if float(quantidade) > 0:
                ok = Pedido.vincular_lote(id_pedido, id_lote, quantidade)
                if ok:
                    Lote.consumir(id_lote, quantidade)
                    total_atendido += float(quantidade)
        pedido = Pedido.obter_por_id(id_pedido)
        if pedido:
            solicitada = float(pedido["quantidade_solicitada"])
            if total_atendido >= solicitada:
                Pedido.atualizar_status(id_pedido, "Atendido")
            elif total_atendido > 0:
                Pedido.atualizar_status(id_pedido, "Atendido Parcialmente")
        return True, f"Estoque distribuido: {total_atendido:.1f}"

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
