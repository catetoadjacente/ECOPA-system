import customtkinter as ctk
from tkinter import messagebox
from controllers.cliente_controller import ClienteController


class ListaClientes(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar

        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Header
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        label = ctk.CTkLabel(
            header, text="Clientes Cadastrados",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(side="left")

        btn_voltar = ctk.CTkButton(
            header, text="Voltar", width=100,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            command=self.on_voltar
        )
        btn_voltar.pack(side="right")

        # Tabela
        colunas = ["ID Ponto", "Estabelecimento", "Endereço", "Email", "Telefone", "Proprietário", "CNPJ", "Ações"]
        frame_tabela = ctk.CTkFrame(self.content)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        for i, col in enumerate(colunas):
            lbl = ctk.CTkLabel(
                frame_tabela, text=col,
                font=ctk.CTkFont(weight="bold"),
                width=120
            )
            lbl.grid(row=0, column=i, padx=5, pady=8, sticky="w")

        clientes = ClienteController.listar()
        for row, cliente in enumerate(clientes, start=1):
            ctk.CTkLabel(frame_tabela, text=str(cliente.get("id_ponto", "")), width=120).grid(row=row, column=0, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=cliente.get("estabelecimento", "") or "", width=150).grid(row=row, column=1, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=cliente.get("endereco", "") or "", width=150).grid(row=row, column=2, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=cliente.get("email", "") or "", width=150).grid(row=row, column=3, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=cliente.get("telefone", "") or "", width=120).grid(row=row, column=4, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=cliente.get("proprietario", "") or "", width=120).grid(row=row, column=5, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=cliente.get("cnpj", "") or "-", width=120).grid(row=row, column=6, padx=5, pady=4, sticky="w")

            btn_editar = ctk.CTkButton(
                frame_tabela, text="Editar", width=70,
                fg_color="#f39c12", hover_color="#e67e22",
                command=lambda idp=cliente["id_ponto"]: self.editar_cliente(idp)
            )
            btn_editar.grid(row=row, column=7, padx=2)

            btn_excluir = ctk.CTkButton(
                frame_tabela, text="Excluir", width=70,
                fg_color="#e74c3c", hover_color="#c0392b",
                command=lambda idp=cliente["id_ponto"]: self.excluir_cliente(idp)
            )
            btn_excluir.grid(row=row, column=8, padx=2)

    def editar_cliente(self, idponto):
        from views.edicao_cliente import EdicaoCliente
        EdicaoCliente(self, self.content, idponto, on_voltar=self.montar_tela)

    def excluir_cliente(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
            ClienteController.deletar(idponto)
            self.montar_tela()