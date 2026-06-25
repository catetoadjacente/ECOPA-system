import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database.database import cadastrar_cliente


class CadastroClienteView(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar

        self.montar_formulario()

    def montar_formulario(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content, width=500, height=550)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            frame, text="Novo Cliente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=(20, 15))

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

        for label_text, key in campos:
            lbl = ctk.CTkLabel(frame, text=label_text + ":")
            lbl.pack(anchor="w", padx=20)
            entry = ctk.CTkEntry(frame, width=350)
            entry.pack(padx=20, pady=(0, 10))
            self.entries[key] = entry

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
        dados = {key: entry.get().strip() for key, entry in self.entries.items()}
        dados["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if cadastrar_cliente(dados):
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            self.on_voltar()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar. Verifique se os IDs já existem.")
            