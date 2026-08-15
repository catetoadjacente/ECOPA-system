import customtkinter as ctk
from tkinter import messagebox
from controllers.gerente_controller import GerenteController
from utils.theme import font, font_small, font_small_bold, ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER


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

        # Card principal
        card = ctk.CTkFrame(
            self.content, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=40, pady=(25, 20))

        # Header
        ctk.CTkLabel(
            card, text="✏️",
            font=font(36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Editar Gerente",
            font=font(22, "bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        # Separador
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(16, 16))

        # Nome (read-only)
        lbl_nome = ctk.CTkLabel(
            card, text="Nome",
            font=font_small_bold(12), text_color=ECOPA_TEXT,
            anchor="w"
        )
        lbl_nome.pack(fill="x", padx=55, pady=(0, 3))
        ctk.CTkLabel(
            card, text=self.gerente["nome"],
            font=font(14, "bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 12))

        # CPF (read-only)
        lbl_cpf = ctk.CTkLabel(
            card, text="CPF",
            font=font_small_bold(12), text_color=ECOPA_TEXT,
            anchor="w"
        )
        lbl_cpf.pack(fill="x", padx=55, pady=(0, 3))
        ctk.CTkLabel(
            card, text=self.cpf,
            font=font(13), text_color=ECOPA_TEXT_LIGHT, anchor="w"
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
                card, text=campo,
                font=font_small_bold(12), text_color=ECOPA_TEXT,
                anchor="w"
            )
            lbl.pack(fill="x", padx=55, pady=(0, 3))
            entry = ctk.CTkEntry(
                card, height=38,
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=10, font=font(13), border_width=1
            )
            entry.pack(fill="x", padx=55, pady=(0, 10))
            entry.insert(0, self.gerente[db_key] or "")
            self.entries[db_key] = entry

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(16, 24))

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font(13, "bold"),
            command=self._on_salvar
        ).pack(side="right", padx=8)

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=font(13, "bold"),
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
