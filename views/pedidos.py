import customtkinter as ctk
from tkinter import messagebox
from controllers.pedido_controller import PedidoController

ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"
ECOPA_ORANGE = "#f39c12"
ECOPA_LEAF = "#27ae60"
ECOPA_BLUE = "#3498db"
ECOPA_RED = "#e74c3c"


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
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Remessas de material para destinações",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="+ Novo Pedido", width=160, height=38,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
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

        cabecalhos = ["ID", "Destino", "Tipo", "Qtd Solicitada", "Qtd Atendida", "Status", "Data", "Acoes"]
        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12)
        header_frame.pack(fill="x", padx=16, pady=(16, 0))

        larguras = [50, 150, 100, 110, 110, 120, 100, 130]
        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, width=larguras[col]
            ).grid(row=0, column=col, padx=6, pady=10, sticky="w")

        dados = PedidoController.listar()

        if not dados:
            ctk.CTkLabel(
                frame_tabela, text="Nenhum pedido cadastrado",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for linha, d in enumerate(dados, start=1):
            bg = ECOPA_BG if linha % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0)
            row_frame.pack(fill="x", padx=16)

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
            qtd_sol = f"{float(d['quantidade_solicitada']):.1f} Kg"
            qtd_atd = f"{float(d['quantidade_atendida']):.1f} Kg"

            valores = [f"#{d['id']}", d["destinacao"], d["tipo_destinacao"], qtd_sol, qtd_atd]
            for col, valor in enumerate(valores):
                ctk.CTkLabel(
                    row_frame, text=valor,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    width=larguras[col], anchor="w"
                ).grid(row=0, column=col, padx=6, pady=6, sticky="w")

            badge = ctk.CTkLabel(
                row_frame, text=status, font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=badge_bg, text_color=badge_cor,
                corner_radius=8, width=100, height=26)
            badge.grid(row=0, column=5, padx=6, pady=6, sticky="w")

            ctk.CTkLabel(
                row_frame, text=data_str,
                font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                width=larguras[6], anchor="w"
            ).grid(row=0, column=6, padx=6, pady=6, sticky="w")

            acoes_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            acoes_frame.grid(row=0, column=7, padx=4, pady=4)

            id_pedido = d["id"]
            if d["status"] in ("Aberto", "Atendido Parcialmente"):
                ctk.CTkButton(
                    acoes_frame, text="Distribuir", width=72, height=28,
                    fg_color=ECOPA_BLUE, hover_color="#2980b9",
                    corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                    command=lambda ip=id_pedido: self._distribuir(ip)
                ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes_frame, text="Excluir", width=60, height=28,
                fg_color=ECOPA_RED, hover_color="#c0392b",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda ip=id_pedido: self._excluir(ip)
            ).pack(side="left", padx=2)

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
