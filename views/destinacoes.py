import customtkinter as ctk
from tkinter import messagebox
from controllers.destinacao_controller import DestinacaoController

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
ECOPA_BLUE = "#3498db"
ECOPA_RED = "#e74c3c"


class DestinacoesView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Destinacoes",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencia todas as destinacoes de residuos",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="+ Nova Destinacao", width=160, height=38,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
            command=self._cadastrar
        ).pack(anchor="e")

        # Linha verde
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Tabela
        self._montar_tabela(container)

    def _montar_tabela(self, parent):
        frame_tabela = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        # Cabecalho
        cabecalhos = ["ID", "Cliente", "CNPJ", "Coleta", "Ponto Origem", "Quantidade", "Data", "Acoes"]
        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12)
        header_frame.pack(fill="x", padx=16, pady=(16, 0))

        larguras = [50, 130, 130, 70, 150, 90, 100, 140]
        for coluna, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, width=larguras[coluna]
            ).grid(row=0, column=coluna, padx=6, pady=10, sticky="w")

        # Dados
        dados = DestinacaoController.listar()

        if not dados:
            ctk.CTkLabel(
                frame_tabela, text="Nenhuma destinacao cadastrada",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for linha, d in enumerate(dados, start=1):
            bg = ECOPA_BG if linha % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0)
            row_frame.pack(fill="x", padx=16)

            data_str = d["data_dest"].strftime("%d/%m/%Y") if d["data_dest"] else ""
            qtd_str = f"{float(d['quantidade'] or 0):.1f} Kg"

            valores = [
                str(d["id"]),
                d["cliente"],
                d["cnpj"],
                f"#{d['coleta_id_coleta']}",
                d["ponto"],
                qtd_str,
                data_str,
            ]

            for coluna, valor in enumerate(valores):
                ctk.CTkLabel(
                    row_frame, text=valor,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    width=larguras[coluna], anchor="w"
                ).grid(row=0, column=coluna, padx=6, pady=6, sticky="w")

            acoes_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            acoes_frame.grid(row=0, column=7, padx=4, pady=4)

            id_dest = d["id"]
            ctk.CTkButton(
                acoes_frame, text="Editar", width=60, height=28,
                fg_color=ECOPA_ORANGE, hover_color="#e67e22",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda ide=id_dest: self._editar(ide)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes_frame, text="Excluir", width=60, height=28,
                fg_color=ECOPA_RED, hover_color="#c0392b",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda ide=id_dest: self._excluir(ide)
            ).pack(side="left", padx=2)

    def _cadastrar(self):
        from views.cadastro_destinacao import CadastroDestinacao
        CadastroDestinacao(self, self.content, on_voltar=self.montar_tela)

    def _editar(self, id_dest):
        from views.edicao_destinacao import EdicaoDestinacao
        EdicaoDestinacao(self, self.content, id_dest, on_voltar=self.montar_tela)

    def _excluir(self, id_dest):
        if messagebox.askyesno("Confirmar", "Deseja excluir esta destinacao?"):
            DestinacaoController.deletar(id_dest)
            self.montar_tela()
