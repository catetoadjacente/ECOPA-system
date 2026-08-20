import customtkinter as ctk
from datetime import datetime
from controllers.coleta_controller import ColetaController
from controllers.ponto_controller import PontoController
from controllers.gerente_controller import GerenteController
from utils.theme import font, ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER
from utils.widgets import toast


class CadastroColeta(ctk.CTkFrame):
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

        # Card principal
        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
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

        # Gerente
        ctk.CTkLabel(
            card, text="Gerente responsável",
            font=font(12, "bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        gerentes = GerenteController.listar()
        self.gerentes_lista = gerentes
        nomes_gerentes = [g["nome"] for g in gerentes]
        self.combo_gerente = ctk.CTkComboBox(
            card, values=nomes_gerentes if nomes_gerentes else ["Nenhum gerente disponível"],
            height=38, font=font(13), state="readonly",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10
        )
        if nomes_gerentes:
            self.combo_gerente.set(nomes_gerentes[0])
        self.combo_gerente.pack(fill="x", padx=55, pady=(0, 16))

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
        nome_gerente = self.combo_gerente.get().strip()
        nome_ponto = self.combo_ponto.get().strip()
        data_coleta = self.entry_data.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        observacao = self.text_observacao.get("1.0", "end-1c").strip()

        if not all([nome_gerente, nome_ponto, data_coleta, quantidade]):
            toast("Preencha todos os campos obrigatorios!", tipo="error")
            return

        # Validar se selecionou valores reais (placeholder de combo vazio)
        nomes_pontos = [p["estabelecimento"] for p in self.pontos_lista]
        nomes_gerentes = [g["nome"] for g in self.gerentes_lista]
        if nome_ponto not in nomes_pontos:
            toast("Selecione um ponto de coleta valido!", tipo="error")
            return
        if nome_gerente not in nomes_gerentes:
            messagebox.showerror("Erro", "Selecione um gerente válido!")
            return
        if nome_gerente not in nomes_gerentes:
            messagebox.showerror("Erro", "Selecione um gerente válido!")
            return

        try:
            data_coleta = datetime.strptime(data_coleta, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        except ValueError:
            toast("Data deve estar no formato AAAA-MM-DD HH:MM!", tipo="error")
            return

        try:
            quantidade = float(quantidade)
        except ValueError:
            toast("Quantidade deve ser um numero!", tipo="error")
            return

        if quantidade <= 0:
            toast("Quantidade deve ser maior que zero!", tipo="error")
            return

        gerente_cpf = next(
            (g["cpf"] for g in self.gerentes_lista if g["nome"] == nome_gerente),
            None
        )

        dados = {
            "ponto": nome_ponto,
            "gerente_cpf": gerente_cpf,
            "quantidade": quantidade,
            "data_coleta": data_coleta,
            "observacao": observacao,
        }

        sucesso, mensagem = ColetaController.cadastrar(dados)
        if sucesso:
            toast(mensagem, tipo="success")
            self.on_voltar()
        else:
            toast(mensagem, tipo="error")
