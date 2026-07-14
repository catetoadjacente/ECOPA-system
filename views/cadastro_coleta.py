import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.coleta_controller import ColetaController
from controllers.ponto_controller import PontoController
from controllers.gerente_controller import GerenteController


class CadastroColeta(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self.montar_formulario()

    def montar_formulario(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="#dcebdc")
        scroll.pack(fill="both", expand=True)

        # Titulo
        ctk.CTkLabel(
            scroll, text="Coleta",
            font=ctk.CTkFont(size=26, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(25, 0))

        ctk.CTkLabel(
            scroll, text="preencha os dados para cadastrar uma nova coleta.",
            font=ctk.CTkFont(size=13), text_color="#555", anchor="w"
        ).pack(fill="x", padx=40, pady=(0, 15))

        # Secao Dados
        ctk.CTkLabel(
            scroll, text="Dados",
            font=ctk.CTkFont(size=20, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(10, 0))

        ctk.CTkFrame(scroll, fg_color="#ccc", height=1).pack(fill="x", padx=40, pady=(5, 15))

        # Data
        ctk.CTkLabel(
            scroll, text="Data da coleta",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(0, 2))
        self.entry_data = ctk.CTkEntry(scroll, height=35, font=ctk.CTkFont(size=13))
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.entry_data.pack(fill="x", padx=40, pady=(0, 12))

        # Ponto
        ctk.CTkLabel(
            scroll, text="Ponto da coleta",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(0, 2))
        pontos = PontoController.listar()
        self.pontos_lista = pontos
        nomes_pontos = [p["estabelecimento"] for p in pontos]
        self.combo_ponto = ctk.CTkComboBox(
            scroll, values=nomes_pontos if nomes_pontos else ["Nenhum ponto disponivel"],
            height=35, font=ctk.CTkFont(size=13), state="readonly"
        )
        if nomes_pontos:
            self.combo_ponto.set(nomes_pontos[0])
        self.combo_ponto.pack(fill="x", padx=40, pady=(0, 12))

        # Quantidade
        ctk.CTkLabel(
            scroll, text="Quantidade coletada",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(0, 2))
        self.entry_quantidade = ctk.CTkEntry(scroll, height=35, font=ctk.CTkFont(size=13))
        self.entry_quantidade.pack(fill="x", padx=40, pady=(0, 12))

        # Gerente
        ctk.CTkLabel(
            scroll, text="Gerente responsável",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(0, 2))
        gerentes = GerenteController.listar()
        self.gerentes_lista = gerentes
        nomes_gerentes = [g["nome"] for g in gerentes]
        self.combo_gerente = ctk.CTkComboBox(
            scroll, values=nomes_gerentes if nomes_gerentes else ["Nenhum gerente disponivel"],
            height=35, font=ctk.CTkFont(size=13), state="readonly"
        )
        if nomes_gerentes:
            self.combo_gerente.set(nomes_gerentes[0])
        self.combo_gerente.pack(fill="x", padx=40, pady=(0, 12))

        # Secao Observacoes
        ctk.CTkLabel(
            scroll, text="observações:",
            font=ctk.CTkFont(size=20, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 0))

        ctk.CTkFrame(scroll, fg_color="#ccc", height=1).pack(fill="x", padx=40, pady=(5, 10))

        self.text_observacao = ctk.CTkTextbox(scroll, height=150, font=ctk.CTkFont(size=13))
        self.text_observacao.pack(fill="x", padx=40, pady=(0, 12))

        # Botoes
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=(25, 20))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=120, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            font=ctk.CTkFont(size=14),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Salvar", width=120, height=40,
            fg_color="#006d12", hover_color="#0a8f2c",
            font=ctk.CTkFont(size=14),
            command=self.salvar
        ).pack(side="right")

    def salvar(self):
        nome_gerente = self.combo_gerente.get().strip()
        nome_ponto = self.combo_ponto.get().strip()
        data_coleta = self.entry_data.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        observacao = self.text_observacao.get("1.0", "end-1c").strip()

        if not all([nome_gerente, nome_ponto, data_coleta, quantidade]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        try:
            datetime.strptime(data_coleta, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Data deve estar no formato AAAA-MM-DD HH:MM!")
            return

        try:
            quantidade = float(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número!")
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
            messagebox.showinfo("Sucesso", mensagem)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", mensagem)
