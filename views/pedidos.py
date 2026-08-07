import customtkinter as ctk
from tkinter import messagebox
from controllers.pedido_controller import PedidoController
from views.loading import LoadingOverlay, carregar_em_bg
from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE,
    ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE, ECOPA_LEAF,
    ECOPA_BLUE, ECOPA_RED, font, font_title, font_small, font_small_bold,
)
from utils.widgets import TabelaPaginada


class PedidosView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Pedidos",
            font=font_title(30), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Remessas de material para destinações",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="+ Novo Pedido", width=160, height=38,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font_small_bold(12),
            command=self._cadastrar
        ).pack(anchor="e")

        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0))

        self._montar_tabela(container)

    def _montar_tabela(self, parent):
        frame_tabela = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))
        self._frame_tabela = frame_tabela

        colunas = ["ID", "Destino", "Tipo", "Qtd Solicitada", "Qtd Atendida", "Status", "Data", "Ações"]
        relx = [0.01, 0.06, 0.22, 0.32, 0.44, 0.56, 0.68, 0.80]

        def _render_row(frame, item, rlx):
            valores = [item["id"], item["destino"], item["tipo"], item["qtd_sol"], item["qtd_atd"]]
            for i, v in enumerate(valores):
                ctk.CTkLabel(frame, text=v, font=font_small(12),
                             text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[i], rely=0.5, anchor="w")

            ctk.CTkLabel(frame, text=item["status"], font=font_small_bold(11),
                         fg_color=item["badge_bg"], text_color=item["badge_cor"],
                         corner_radius=8, height=26).place(relx=rlx[5], rely=0.5, anchor="w")

            ctk.CTkLabel(frame, text=item["data"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[6], rely=0.5, anchor="w")

            acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
            acoes_frame.place(relx=rlx[7], rely=0.5, anchor="w")

            id_pedido = item["id_num"]
            if item["status"] in ("Aberto", "Atendido Parcialmente"):
                ctk.CTkButton(
                    acoes_frame, text="Distribuir", width=72, height=28,
                    fg_color=ECOPA_BLUE, hover_color="#2980b9",
                    corner_radius=8, font=font_small_bold(10),
                    command=lambda ip=id_pedido: self._distribuir(ip)
                ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes_frame, text="Excluir", width=60, height=28,
                fg_color=ECOPA_RED, hover_color="#c0392b",
                corner_radius=8, font=font_small_bold(10),
                command=lambda ip=id_pedido: self._excluir(ip)
            ).pack(side="left", padx=2)

        self._tabela = TabelaPaginada(frame_tabela, colunas=colunas, relx=relx, on_render=_render_row)
        self._tabela.pack(fill="both", expand=True)

        overlay = LoadingOverlay(frame_tabela, text="Carregando pedidos...")
        overlay.start()

        def _carregar():
            return PedidoController.listar()

        def _montar(dados):
            overlay.stop()
            if not dados:
                ctk.CTkLabel(frame_tabela, text="Nenhum pedido cadastrado",
                             font=font(13), text_color=ECOPA_TEXT_LIGHT).pack(pady=40)
                return

            items = []
            for d in dados:
                status = d["status"]
                if status == "Aberto":
                    badge_cor, badge_bg = ECOPA_BLUE, "#e8f0f8"
                elif status == "Atendido Parcialmente":
                    badge_cor, badge_bg = ECOPA_ORANGE, "#fdf5e8"
                elif status == "Atendido":
                    badge_cor, badge_bg = ECOPA_LEAF, "#e8f8e8"
                else:
                    badge_cor, badge_bg = ECOPA_RED, "#fde8e8"

                data_str = d["data_pedido"].strftime("%d/%m/%Y") if d["data_pedido"] else ""

                items.append({
                    "id": f"#{d['id']}",
                    "id_num": d["id"],
                    "destino": d["destinacao"],
                    "tipo": d["tipo_destinacao"],
                    "qtd_sol": f"{float(d['quantidade_solicitada']):.1f} Kg",
                    "qtd_atd": f"{float(d['quantidade_atendida']):.1f} Kg",
                    "status": status,
                    "badge_cor": badge_cor,
                    "badge_bg": badge_bg,
                    "data": data_str,
                })

            self._tabela.carregar(items)

        carregar_em_bg(frame_tabela, _carregar, _montar)

    def _cadastrar(self):
        from views.cadastro_pedido import CadastroPedido
        CadastroPedido(self, self.content, on_voltar=self.montar_tela)

    def _distribuir(self, id_pedido):
        from views.distribuicao_estoque import DistribuicaoEstoque
        DistribuicaoEstoque(self, self.content, id_pedido, on_voltar=self.montar_tela)

    def _excluir(self, id_pedido):
        if messagebox.askyesno("Confirmar", "Deseja excluir este pedido?"):
            ok, msg = PedidoController.deletar(id_pedido)
            if ok:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)
            self.montar_tela()
