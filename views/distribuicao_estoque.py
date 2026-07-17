import customtkinter as ctk
from tkinter import messagebox
from controllers.pedido_controller import PedidoController
from controllers.lote_controller import LoteController

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


class DistribuicaoEstoque(ctk.CTkFrame):
    def __init__(self, master, content, id_pedido, on_voltar):
        super().__init__(master)
        self.content = content
        self.id_pedido = id_pedido
        self.on_voltar = on_voltar
        self.pedido = PedidoController.obter_por_id(id_pedido)
        if not self.pedido:
            messagebox.showerror("Erro", "Pedido nao encontrado!")
            self.on_voltar()
            return
        self.lotes_entries = {}
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(container, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text=f"Distribuir Estoque - Pedido #{self.id_pedido}",
            font=ctk.CTkFont(size=26, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Selecione os lotes para atender este pedido",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(scroll, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0))

        # Info do pedido
        info_card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        info_card.pack(fill="x", padx=32, pady=(20, 0))

        ctk.CTkLabel(info_card, text=f"Destino: {self.pedido['destinacao']}",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(14, 4))

        ctk.CTkLabel(info_card,
            text=f"Solicitado: {float(self.pedido['quantidade_solicitada']):.1f} Kg | Ja atendido: {float(self.pedido['quantidade_atendida']):.1f} Kg",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(fill="x", padx=20, pady=(0, 14))

        # Lotes disponiveis
        lotes_card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        lotes_card.pack(fill="x", padx=32, pady=(16, 0))

        ctk.CTkLabel(lotes_card, text="Lotes Disponiveis",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 8))

        lotes = LoteController.listar_disponiveis()

        if not lotes:
            ctk.CTkLabel(lotes_card, text="Nenhum lote disponivel no estoque",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=30)
        else:
            cabecalhos = ["Lote", "Fonte", "Data", "Disponivel", "Quantidade"]
            header_frame = ctk.CTkFrame(lotes_card, fg_color=ECOPA_GREEN, corner_radius=10)
            header_frame.pack(fill="x", padx=16, pady=(0, 4))

            larguras = [60, 180, 100, 100, 120]
            for col, texto in enumerate(cabecalhos):
                ctk.CTkLabel(
                    header_frame, text=texto,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=ECOPA_WHITE, width=larguras[col]
                ).grid(row=0, column=col, padx=8, pady=8, sticky="w")

            for lote in lotes:
                row = ctk.CTkFrame(lotes_card, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=2)

                data_str = lote["data_criacao"].strftime("%d/%m/%Y") if lote["data_criacao"] else ""
                qtd_disp = f"{float(lote['quantidade_restante']):.1f} Kg"

                ctk.CTkLabel(row, text=f"#{lote['id']}",
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    width=larguras[0], anchor="w").grid(row=0, column=0, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=lote["ponto"],
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    width=larguras[1], anchor="w").grid(row=0, column=1, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=data_str,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    width=larguras[2], anchor="w").grid(row=0, column=2, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=qtd_disp,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_GREEN,
                    width=larguras[3], anchor="w").grid(row=0, column=3, padx=8, pady=4, sticky="w")

                entry = ctk.CTkEntry(
                    row, width=larguras[4], height=30, placeholder_text="0.0",
                    fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                    corner_radius=8, font=ctk.CTkFont(size=12), border_width=1)
                entry.grid(row=0, column=4, padx=8, pady=4)
                self.lotes_entries[lote["id"]] = (entry, float(lote["quantidade_restante"]))

        # Botoes
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(fill="x", padx=32, pady=(20, 20))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=42,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Confirmar Distribuicao", width=200, height=42,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirmar
        ).pack(side="right")

    def _confirmar(self):
        lotes_para_vincular = []
        for lote_id, (entry, max_qtd) in self.lotes_entries.items():
            texto = entry.get().strip()
            if texto:
                try:
                    qtd = float(texto)
                    if qtd > 0:
                        lotes_para_vincular.append((lote_id, min(qtd, max_qtd)))
                except ValueError:
                    pass

        if not lotes_para_vincular:
            messagebox.showwarning("Aviso", "Selecione ao menos um lote com quantidade!")
            return

        ok, msg = PedidoController.vincular_lotes(self.id_pedido, lotes_para_vincular)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
