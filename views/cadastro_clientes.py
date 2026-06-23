import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database.database import cadastrar_cliente


class CadastroClienteView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Cliente")
        self.geometry("500x650")

        ctk.CTkLabel(self, text="CADASTRO DE CLIENTE",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        campos = [
            ("ID Ponto", "idponto"),
            ("Endereço", "endereco"),
            ("Email", "email"),
            ("Estabelecimento", "estabelecimento"),
            ("Telefone", "telefone"),
            ("Proprietário", "proprietario"),
            ("ID Destinação", "iddeatinacoes"),
            ("CNPJ", "cnpj"),
            ("Cliente", "cliente"),
        ]

        self.entries = {}
        for label, key in campos:
            ctk.CTkLabel(self, text=label, anchor="w").pack(
                padx=40, pady=(10, 0), fill="x")
            entry = ctk.CTkEntry(self)
            entry.pack(padx=40, fill="x")
            self.entries[key] = entry

        ctk.CTkButton(self, text="Salvar",
                      command=self.salvar).pack(pady=25)

    def salvar(self):
        dados = {key: entry.get().strip() for key, entry in self.entries.items()}
        dados["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if cadastrar_cliente(dados):
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.destroy()
        else:
            messagebox.showerror("Erro",
                                 "Falha ao cadastrar. Verifique se os IDs já existem.")
            