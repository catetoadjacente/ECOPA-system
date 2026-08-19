import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.coleta_controller import ColetaController
from controllers.ponto_controller import PontoController
from utils.theme import font, ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER


class CadastroColeta(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self.montar_formulario()

    def montar_formulario(self):
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
            card, text="🚛",
            font=font(36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Nova Coleta",
            font=font(22, "bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            card, text="Preencha os dados para cadastrar uma nova coleta",
            font=font(12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(0, 16))

        # Secao Dados
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

        ctk.CTkLabel(
            card, text="Dados da Coleta",
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        # Data
        ctk.CTkLabel(
            card, text="Data da coleta",
            font=font(12, "bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_data = ctk.CTkEntry(
            card, height=38,
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=font(13), border_width=1
        )
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.entry_data.pack(fill="x", padx=55, pady=(0, 12))

        # Ponto
        ctk.CTkLabel(
            card, text="Ponto da coleta",
            font=font(12, "bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        pontos = PontoController.listar()
        self.pontos_lista = pontos
        nomes_pontos = [p["estabelecimento"] for p in pontos]
        self.combo_ponto = ctk.CTkComboBox(
            card, values=nomes_pontos if nomes_pontos else ["Nenhum ponto disponível"],
            height=38, font=font(13), state="readonly",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10
        )
        if nomes_pontos:
            self.combo_ponto.set(nomes_pontos[0])
        self.combo_ponto.pack(fill="x", padx=55, pady=(0, 12))

        # Quantidade
        ctk.CTkLabel(
            card, text="Quantidade coletada (Kg)",
            font=font(12, "bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_quantidade = ctk.CTkEntry(
            card, height=38, placeholder_text="Ex: 120.5",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=font(13), border_width=1
        )
        self.entry_quantidade.pack(fill="x", padx=55, pady=(0, 12))

        # Secao Observacoes
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

        ctk.CTkLabel(
            card, text="Observações",
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        self.text_observacao = ctk.CTkTextbox(
            card, height=120, font=font(13),
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, border_width=1
        )
        self.text_observacao.pack(fill="x", padx=55, pady=(0, 16))

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(5, 25))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=42,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=font(13, "bold"),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=42,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font(13, "bold"),
            command=self.salvar
        ).pack(side="right")

    def salvar(self):
        nome_ponto = self.combo_ponto.get().strip()
        data_coleta = self.entry_data.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        observacao = self.text_observacao.get("1.0", "end-1c").strip()

        if not all([nome_ponto, data_coleta, quantidade]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        # Validar se selecionou valores reais (placeholder de combo vazio)
        nomes_pontos = [p["estabelecimento"] for p in self.pontos_lista]
        if nome_ponto not in nomes_pontos:
            messagebox.showerror("Erro", "Selecione um ponto de coleta válido!")
            return

        try:
            data_coleta = datetime.strptime(data_coleta, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Data deve estar no formato AAAA-MM-DD HH:MM!")
            return

        try:
            quantidade = float(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número!")
            return

        if quantidade <= 0:
            messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
            return

        dados = {
            "ponto": nome_ponto,
            "quantidade": quantidade,
            "data_coleta": data_coleta,
            "observacao": observacao,
        }

        sucesso, mensagem = ColetaController.cadastrar(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", mensagem)
