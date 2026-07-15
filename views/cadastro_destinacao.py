import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
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


class CadastroDestinacao(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self.montar_formulario()

    def montar_formulario(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=40, pady=(25, 20))

        ctk.CTkLabel(
            card, text="♻",
            font=ctk.CTkFont(size=36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Nova Destinacao",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            card, text="Preencha os dados para cadastrar uma nova destinacao",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(0, 16))

        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

        ctk.CTkLabel(
            card, text="Dados da Destinacao",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=ECOPA_GREEN_DARK,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        # Cliente
        ctk.CTkLabel(
            card, text="Nome do cliente",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_cliente = ctk.CTkEntry(
            card, height=38, placeholder_text="Ex: ReciclaMais LTDA",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1
        )
        self.entry_cliente.pack(fill="x", padx=55, pady=(0, 12))

        # CNPJ
        ctk.CTkLabel(
            card, text="CNPJ",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_cnpj = ctk.CTkEntry(
            card, height=38, placeholder_text="Ex: 12345678000199",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1
        )
        self.entry_cnpj.pack(fill="x", padx=55, pady=(0, 12))

        # Data
        ctk.CTkLabel(
            card, text="Data da destinacao",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_data = ctk.CTkEntry(
            card, height=38,
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1
        )
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.entry_data.pack(fill="x", padx=55, pady=(0, 12))

        # Coleta vinculada
        ctk.CTkLabel(
            card, text="Coleta vinculada",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))

        coletas = DestinacaoController.coletas_disponiveis()
        self.coletas_lista = coletas
        if coletas:
            nomes_coletas = [
                f"#{c['id']} - {c['ponto']} ({c['quantidade']} Kg)"
                for c in coletas
            ]
        else:
            nomes_coletas = ["Nenhuma coleta disponivel"]

        self.combo_coleta = ctk.CTkComboBox(
            card, values=nomes_coletas,
            height=38, font=ctk.CTkFont(size=13), state="readonly",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10
        )
        if nomes_coletas and nomes_coletas[0] != "Nenhuma coleta disponivel":
            self.combo_coleta.set(nomes_coletas[0])
        self.combo_coleta.pack(fill="x", padx=55, pady=(0, 16))

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
            command=self.salvar
        ).pack(side="right")

    def salvar(self):
        cliente = self.entry_cliente.get().strip()
        cnpj = self.entry_cnpj.get().strip()
        data = self.entry_data.get().strip()

        if not all([cliente, cnpj, data]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatorios!")
            return

        try:
            datetime.strptime(data, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Data deve estar no formato AAAA-MM-DD HH:MM!")
            return

        # Pegar coleta selecionada
        idx = self.combo_coleta.current()
        if idx < 0 or idx >= len(self.coletas_lista):
            messagebox.showerror("Erro", "Selecione uma coleta valida!")
            return

        coleta_id = self.coletas_lista[idx]["id"]

        dados = {
            "cliente": cliente,
            "cnpj": cnpj,
            "data": data,
            "coleta_id_coleta": coleta_id,
        }

        sucesso, mensagem = DestinacaoController.cadastrar(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", mensagem)
