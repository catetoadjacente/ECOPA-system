import customtkinter as ctk
from tkinter import ttk, messagebox
from database.database import get_all_gerentes


class GerentesView(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Gerentes Cadastrados")
        self.geometry("900x500")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="GERENTES CADASTRADOS",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        colunas = ("CPF", "Nome", "Celular", "Email", "Setor")
        self.tabela = ttk.Treeview(
            self.frame, columns=colunas, show="headings", height=15
        )

        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=150)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical",
                                  command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        botoes = ctk.CTkFrame(self.frame, fg_color="transparent")
        botoes.pack(pady=10)

        ctk.CTkButton(botoes, text="Atualizar",
                      command=self.carregar_dados).pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="Fechar",
                      command=self.destroy).pack(side="left", padx=5)

        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        gerentes = get_all_gerentes()
        for g in gerentes:
            self.tabela.insert("", "end", values=(
                g["idcpf"], g["nome"], g["Celular"],
                g["email"], g["setor"]
            ))
            