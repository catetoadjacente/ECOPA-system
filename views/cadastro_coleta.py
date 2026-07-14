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

        frame = ctk.CTkFrame(self.content, width=500, height=450)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            frame, text="Nova Coleta",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=(20, 15))

        # Data
        lbl = ctk.CTkLabel(frame, text="Data:")
        lbl.pack(anchor="w", padx=20)
        self.entry_data = ctk.CTkEntry(frame, width=350, placeholder_text="AAAA-MM-DD HH:MM")
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.entry_data.pack(padx=20, pady=(0, 10))

        # Quantidade
        lbl = ctk.CTkLabel(frame, text="Quantidade (Kg):")
        lbl.pack(anchor="w", padx=20)
        self.entry_quantidade = ctk.CTkEntry(frame, width=350)
        self.entry_quantidade.pack(padx=20, pady=(0, 10))

        # Observação
        lbl = ctk.CTkLabel(frame, text="Observação:")
        lbl.pack(anchor="w", padx=20)
        self.entry_observacao = ctk.CTkEntry(frame, width=350)
        self.entry_observacao.pack(padx=20, pady=(0, 10))

        # Gerente
        lbl = ctk.CTkLabel(frame, text="Gerente responsavel:")
        lbl.pack(anchor="w", padx=20)
        gerentes = GerenteController.listar()
        self.gerentes_lista = gerentes
        nomes_gerentes = [g["nome"] for g in gerentes]
        self.combo_gerente = ctk.CTkComboBox(
            frame, values=nomes_gerentes if nomes_gerentes else ["Nenhum gerente disponivel"],
            width=350, state="readonly"
        )
        if nomes_gerentes:
            self.combo_gerente.set(nomes_gerentes[0])
        self.combo_gerente.pack(padx=20, pady=(0, 10))

        # Ponto
        lbl = ctk.CTkLabel(frame, text="Ponto de Coleta:")
        lbl.pack(anchor="w", padx=20)
        pontos = PontoController.listar()
        self.pontos_lista = pontos
        nomes_pontos = [p["estabelecimento"] for p in pontos]
        self.combo_ponto = ctk.CTkComboBox(
            frame, values=nomes_pontos if nomes_pontos else ["Nenhum ponto disponivel"],
            width=350, state="readonly"
        )
        if nomes_pontos:
            self.combo_ponto.set(nomes_pontos[0])
        self.combo_ponto.pack(padx=20, pady=(0, 10))

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        btn_salvar = ctk.CTkButton(
            btn_frame, text="Salvar", width=120,
            fg_color="#27ae60", hover_color="#2ecc71",
            command=self.salvar
        )
        btn_salvar.pack(side="left", padx=10)

        btn_voltar = ctk.CTkButton(
            btn_frame, text="Voltar", width=120,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            command=self.on_voltar
        )
        btn_voltar.pack(side="left", padx=10)

    def salvar(self):
        nome_gerente = self.combo_gerente.get().strip()
        nome_ponto = self.combo_ponto.get().strip()
        data_coleta = self.entry_data.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        observacao = self.entry_observacao.get().strip()

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
