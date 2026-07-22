import customtkinter as ctk
from tkinter import messagebox
from controllers.gerente_controller import GerenteController

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


class ListaGerentes(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self._montar()

    def _montar(self):
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
            left, text="Gerentes Cadastrados",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencie os gerentes do sistema",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        btn_voltar = ctk.CTkButton(
            header, text="← Voltar", width=110, height=36,
            fg_color=ECOPA_TEXT_LIGHT, hover_color="#888888",
            corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
            command=self.on_voltar
        )
        btn_voltar.pack(side="right")

        # Linha verde
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Tabela
        frame_tabela = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        colunas = ["CPF", "Nome", "Celular", "Email", "Setor", "Ações"]
        COL_RELX = [0.01, 0.12, 0.28, 0.44, 0.60, 0.75]

        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12, height=40)
        header_frame.pack(fill="x", padx=16, pady=(16, 4))
        header_frame.pack_propagate(False)

        for i, col in enumerate(colunas):
            ctk.CTkLabel(
                header_frame, text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, anchor="w"
            ).place(relx=COL_RELX[i], rely=0.5, anchor="w")

        gerentes = GerenteController.listar()

        if not gerentes:
            ctk.CTkLabel(
                frame_tabela, text="Nenhum gerente cadastrado",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for row, gerente in enumerate(gerentes):
            bg = ECOPA_BG if row % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0, height=36)
            row_frame.pack(fill="x", padx=16, pady=0)
            row_frame.pack_propagate(False)

            valores = [gerente["cpf"], gerente["nome"], gerente["celular"], gerente["email"], gerente["setor"]]
            for i, valor in enumerate(valores):
                ctk.CTkLabel(
                    row_frame, text=valor,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT, anchor="w"
                ).place(relx=COL_RELX[i], rely=0.5, anchor="w")

            acoes_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            acoes_frame.place(relx=COL_RELX[5], rely=0.5, anchor="w")

            ctk.CTkButton(
                acoes_frame, text="Editar", width=70, height=28,
                fg_color=ECOPA_ORANGE, hover_color="#e67e22",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda cpf=gerente["cpf"]: self._editar(cpf)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes_frame, text="Excluir", width=70, height=28,
                fg_color="#e74c3c", hover_color="#c0392b",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda cpf=gerente["cpf"]: self._excluir(cpf)
            ).pack(side="left", padx=2)

    def _editar(self, cpf):
        from views.edicao_gerente import EdicaoGerente
        EdicaoGerente(self, self.content, cpf, on_voltar=self._montar)

    def _excluir(self, cpf):
        if messagebox.askyesno("Confirmar", "Deseja excluir este gerente?"):
            ok, msg = GerenteController.deletar(cpf)
            if ok:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)
            self._montar()
