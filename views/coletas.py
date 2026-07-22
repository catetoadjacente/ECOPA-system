import customtkinter as ctk
from tkinter import messagebox
from controllers.coleta_controller import ColetaController

# Paleta ECOPA
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
ECOPA_YELLOW = "#f1c40f"


class ColetasView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Container principal
        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Coletas",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencia todas as coletas do sistema",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Linha verde
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Card de filtros
        card_filtros = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card_filtros.pack(fill="x", padx=32, pady=(20, 0))

        ctk.CTkLabel(
            card_filtros, text="🔍 Filtros",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(14, 8))

        filtros = ctk.CTkFrame(card_filtros, fg_color="transparent")
        filtros.pack(fill="x", padx=20, pady=(0, 14))

        ctk.CTkLabel(
            filtros, text="Status:", font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 8))

        filtro_status = ctk.CTkComboBox(
            filtros, values=["TODOS", "Pendente", "Realizada"],
            width=160, height=36, corner_radius=10,
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT,
            command=self._filtrar
        )
        filtro_status.pack(side="left")
        filtro_status.set("TODOS")
        self.filtro_status = filtro_status

        btn_limpar = ctk.CTkButton(
            filtros, text="Limpar Filtros", width=130, height=36,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
            command=self.montar_tela
        )
        btn_limpar.pack(side="right")

        self._montar_tabela()

    def _montar_tabela(self, filtro=None):
        for widget in self.content.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, '_is_tabela'):
                widget.destroy()

        # Tabela
        frame_tabela = ctk.CTkFrame(
            self.content, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        frame_tabela._is_tabela = True
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        # Cabecalho da tabela
        cabecalhos = ["ID", "Ponto", "Observação", "Quantidade", "Data", "Status", "Ações"]
        COL_RELX = [0.01, 0.06, 0.20, 0.38, 0.50, 0.60, 0.72]

        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12, height=40)
        header_frame.pack(fill="x", padx=16, pady=(16, 4))
        header_frame.pack_propagate(False)

        for coluna, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, anchor="w"
            ).place(relx=COL_RELX[coluna], rely=0.5, anchor="w")

        # Dados
        coletas = ColetaController.listar()
        if filtro and filtro != "TODOS":
            coletas = [c for c in coletas if c["status"] == filtro]

        if not coletas:
            ctk.CTkLabel(
                frame_tabela, text="Nenhuma coleta encontrada",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for linha, c in enumerate(coletas):
            bg = ECOPA_BG if linha % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0, height=36)
            row_frame.pack(fill="x", padx=16, pady=0)
            row_frame.pack_propagate(False)

            id_str = f"#{int(c['id'])}"
            data_str = c["data_coleta"].strftime("%d/%m/%Y") if c["data_coleta"] else ""
            qtd_str = f"{float(c['quantidade']):.1f} Kg" if c["quantidade"] else ""
            registro = [id_str, c["ponto"], c["observacao"], qtd_str, data_str, c["status"]]

            for coluna, valor in enumerate(registro):
                if coluna == 5:
                    badge_cor = ECOPA_LEAF if valor == "Realizada" else ECOPA_ORANGE
                    badge_bg = "#e8f8e8" if valor == "Realizada" else "#fdf5e8"
                    badge = ctk.CTkLabel(
                        row_frame, text=valor, font=ctk.CTkFont(size=11, weight="bold"),
                        fg_color=badge_bg, text_color=badge_cor,
                        corner_radius=8, height=26
                    )
                    badge.place(relx=COL_RELX[coluna], rely=0.5, anchor="w")
                else:
                    ctk.CTkLabel(
                        row_frame, text=valor,
                        font=ctk.CTkFont(size=12),
                        text_color=ECOPA_TEXT, anchor="w"
                    ).place(relx=COL_RELX[coluna], rely=0.5, anchor="w")

            id_coleta = c["id"]
            if c["status"] == "Pendente":
                ctk.CTkButton(
                    row_frame, text="Realizar", width=80, height=28,
                    fg_color=ECOPA_LEAF, hover_color="#2ecc71",
                    corner_radius=8, font=ctk.CTkFont(size=11, weight="bold"),
                    command=lambda idc=id_coleta: self._marcar_realizada(idc)
                ).place(relx=COL_RELX[6], rely=0.5, anchor="w")

    def _filtrar(self, valor):
        self._montar_tabela(filtro=valor)

    def _marcar_realizada(self, id_coleta):
        if messagebox.askyesno("Confirmar", "Marcar esta coleta como realizada?"):
            if ColetaController.atualizar_status(id_coleta, "Realizada"):
                self.montar_tela()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar status!")
