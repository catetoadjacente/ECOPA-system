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


class CadastroGerente(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        # Card principal
        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=40, pady=(25, 20))

        # Header
        ctk.CTkLabel(
            card, text="👤",
            font=ctk.CTkFont(size=36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Novo Gerente",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            card, text="Preencha os dados para cadastrar um novo gerente",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(0, 16))

        # Separador
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 16))

        # Campos
        campos = [
            ("CPF", "cpf", "000.000.000-00"),
            ("Nome", "nome", "Nome completo"),
            ("Celular", "celular", "(00) 00000-0000"),
            ("Email", "email", "email@exemplo.com"),
            ("Senha", "senha", "Senha de acesso"),
            ("Setor", "setor", "Setor de atuação"),
        ]
        self.entries = {}

        for label_text, key, placeholder in campos:
            lbl = ctk.CTkLabel(
                card, text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
                anchor="w"
            )
            lbl.pack(fill="x", padx=55, pady=(0, 3))

            entry = ctk.CTkEntry(
                card, height=38, placeholder_text=placeholder,
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=10, font=ctk.CTkFont(size=13),
                border_width=1
            )
            entry.pack(fill="x", padx=55, pady=(0, 8))
            self.entries[key] = entry

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(12, 20))

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_salvar
        ).pack(side="right", padx=8)

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left", padx=8)

    def _on_salvar(self):
        dados = {campo: entry.get().strip() for campo, entry in self.entries.items()}
        ok, msg = GerenteController.cadastrar(dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
