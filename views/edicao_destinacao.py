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

TIPOS = ["Reciclagem", "Biomassa", "Compostagem", "Aterro", "Outro"]


class EdicaoDestinacao(ctk.CTkFrame):
    def __init__(self, master, content, id_dest, on_voltar):
        super().__init__(master)
        self.content = content
        self.id_dest = id_dest
        self.on_voltar = on_voltar
        self.dados = DestinacaoController.obter_por_id(id_dest)
        if not self.dados:
            messagebox.showerror("Erro", "Destinacao nao encontrada!")
            self.on_voltar()
            return
        self.montar_formulario()

    def montar_formulario(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER)
        card.pack(fill="x", padx=40, pady=(25, 20))

        ctk.CTkLabel(card, text="Editar Destinacao",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(28, 0))

        ctk.CTkLabel(card, text=f"Editando destinacao #{self.id_dest}",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(0, 16))

        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

        # Nome
        ctk.CTkLabel(card, text="Nome",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_nome = ctk.CTkEntry(
            card, height=38, fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.entry_nome.insert(0, self.dados["nome"])
        self.entry_nome.pack(fill="x", padx=55, pady=(0, 12))

        # Tipo
        ctk.CTkLabel(card, text="Tipo",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.combo_tipo = ctk.CTkComboBox(
            card, values=TIPOS, height=38, font=ctk.CTkFont(size=13), state="readonly",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT, corner_radius=10)
        self.combo_tipo.set(self.dados["tipo"])
        self.combo_tipo.pack(fill="x", padx=55, pady=(0, 12))

        # Endereco
        ctk.CTkLabel(card, text="Endereco",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_endereco = ctk.CTkEntry(
            card, height=38, fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.entry_endereco.insert(0, self.dados["endereco"])
        self.entry_endereco.pack(fill="x", padx=55, pady=(0, 16))

        # Contato
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))
        ctk.CTkLabel(card, text="Contato",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        # CNPJ
        ctk.CTkLabel(card, text="CNPJ",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_cnpj = ctk.CTkEntry(
            card, height=38, fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.entry_cnpj.insert(0, self.dados.get("cnpj", "") or "")
        self.entry_cnpj.pack(fill="x", padx=55, pady=(0, 12))

        # Telefone
        ctk.CTkLabel(card, text="Telefone",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_telefone = ctk.CTkEntry(
            card, height=38, fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.entry_telefone.insert(0, self.dados.get("telefone", "") or "")
        self.entry_telefone.pack(fill="x", padx=55, pady=(0, 12))

        # Email
        ctk.CTkLabel(card, text="Email",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_email = ctk.CTkEntry(
            card, height=38, fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.entry_email.insert(0, self.dados.get("email", "") or "")
        self.entry_email.pack(fill="x", padx=55, pady=(0, 16))

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(5, 25))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=42,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=42,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._salvar
        ).pack(side="right")

    def _salvar(self):
        dados = {
            "nome": self.entry_nome.get().strip(),
            "tipo": self.combo_tipo.get(),
            "endereco": self.entry_endereco.get().strip(),
            "cnpj": self.entry_cnpj.get().strip(),
            "telefone": self.entry_telefone.get().strip(),
            "email": self.entry_email.get().strip(),
        }

        if not dados["nome"] or not dados["endereco"]:
            messagebox.showerror("Erro", "Preencha nome e endereco!")
            return

        ok, msg = DestinacaoController.atualizar(self.id_dest, dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
