import customtkinter as ctk
from tkinter import ttk
from database.database import get_all_clientes


class ListarClientesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="CLIENTES CADASTRADOS",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        colunas = ("ID Ponto", "Estabelecimento", "Endereço", "Email",
                   "Telefone", "Proprietário", "ID Dest.", "CNPJ")
        self.tabela = ttk.Treeview(
            self, columns=colunas, show="headings", height=18
        )

        larguras = [80, 150, 150, 150, 100, 120, 80, 120]
        for col, larg in zip(colunas, larguras):
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=larg)

        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 10))

        ctk.CTkButton(self, text="Atualizar",
                      command=self.carregar_dados).pack(pady=10)

        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for c in get_all_clientes():
            self.tabela.insert("", "end", values=(
                c["idponto"], c["estabelecimento"], c["endereco"],
                c["email"], c["telefone"], c["propretario"],
                c["iddeatinacoes"] if c["iddeatinacoes"] else "-",
                c["cnpj"] if c["cnpj"] else "-"
            ))
            