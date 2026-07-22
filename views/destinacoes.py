import customtkinter as ctk
from tkinter import messagebox
from controllers.destinacao_controller import DestinacaoController

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

TIPO_CORES = {
    "Reciclagem": (ECOPA_BLUE, "#e8f0f8"),
    "Biomassa": (ECOPA_GREEN, "#e8f5e8"),
    "Compostagem": (ECOPA_LEAF, "#e8f8e8"),
    "Aterro": (ECOPA_ORANGE, "#fdf5e8"),
    "Outro": (ECOPA_TEXT_LIGHT, "#f0f0f0"),
}


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

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Destinações",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Locais de destino dos materiais coletados",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="+ Nova Destinacao", width=180, height=38,
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

        cabecalhos = ["ID", "Nome", "Tipo", "Endereco", "CNPJ", "Telefone", "Acoes"]
        COL_RELX = [0.01, 0.06, 0.18, 0.28, 0.48, 0.62, 0.75]

        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12, height=40)
        header_frame.pack(fill="x", padx=16, pady=(16, 4))
        header_frame.pack_propagate(False)

        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, anchor="w"
            ).place(relx=COL_RELX[col], rely=0.5, anchor="w")

        dados = DestinacaoController.listar()

        if not dados:
            ctk.CTkLabel(
                frame_tabela, text="Nenhuma destinacao cadastrada",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for linha, d in enumerate(dados):
            bg = ECOPA_BG if linha % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0, height=36)
            row_frame.pack(fill="x", padx=16, pady=0)
            row_frame.pack_propagate(False)

            tipo = d.get("tipo", "Outro")
            badge_cor, badge_bg = TIPO_CORES.get(tipo, (ECOPA_TEXT_LIGHT, "#f0f0f0"))

            valores = [
                str(d["id"]),
                d["nome"],
                "",
                d.get("endereco", ""),
                d.get("cnpj", "") or "",
                d.get("telefone", "") or "",
            ]

            for col, valor in enumerate(valores):
                ctk.CTkLabel(
                    row_frame, text=valor,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT, anchor="w"
                ).place(relx=COL_RELX[col], rely=0.5, anchor="w")

            badge = ctk.CTkLabel(
                row_frame, text=tipo, font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=badge_bg, text_color=badge_cor,
                corner_radius=8, height=26)
            badge.place(relx=COL_RELX[2], rely=0.5, anchor="w")

            acoes_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            acoes_frame.place(relx=COL_RELX[6], rely=0.5, anchor="w")

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
