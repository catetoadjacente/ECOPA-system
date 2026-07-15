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


class EdicaoGerente(ctk.CTkFrame):
    def __init__(self, master, content, cpf, on_voltar):
        super().__init__(master)
        self.content = content
        self.cpf = cpf
        self.on_voltar = on_voltar
        self.gerente = GerenteController.obter_por_cpf(cpf)
        if not self.gerente:
            messagebox.showerror("Erro", "Gerente não encontrado")
            self.on_voltar()
            return
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        frame = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER,
            width=520, height=480
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)

        # Header
        ctk.CTkLabel(
            frame, text="✏️",
            font=ctk.CTkFont(size=36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            frame, text="Editar Gerente",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        # Separador
        ctk.CTkFrame(frame, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(16, 16))

        # Nome (read-only)
        lbl_nome = ctk.CTkLabel(
            frame, text="Nome",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        )
        lbl_nome.pack(fill="x", padx=55, pady=(0, 3))
        ctk.CTkLabel(
            frame, text=self.gerente["nome"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w", width=380
        ).pack(fill="x", padx=55, pady=(0, 12))

        # CPF (read-only)
        lbl_cpf = ctk.CTkLabel(
            frame, text="CPF",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        )
        lbl_cpf.pack(fill="x", padx=55, pady=(0, 3))
        ctk.CTkLabel(
            frame, text=self.cpf,
            font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 12))

        # Campos editaveis
        campos = {
            "Celular": "celular",
            "Email": "email",
            "Setor": "setor",
        }
        self.entries = {}

        for campo, db_key in campos.items():
            lbl = ctk.CTkLabel(
                frame, text=campo,
                font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
                anchor="w"
            )
            lbl.pack(fill="x", padx=55, pady=(0, 3))
            entry = ctk.CTkEntry(
                frame, width=380, height=38,
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=10, font=ctk.CTkFont(size=13), border_width=1
            )
            entry.pack(padx=55, pady=(0, 10))
            entry.insert(0, self.gerente[db_key] or "")
            self.entries[campo] = entry

        # Botoes
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=(16, 24))

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_salvar
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left", padx=8)

    def _on_salvar(self):
        dados = {campo: entry.get().strip() for campo, entry in self.entries.items()}
        ok, msg = GerenteController.atualizar(self.cpf, dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
