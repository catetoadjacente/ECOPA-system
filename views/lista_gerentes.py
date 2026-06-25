import customtkinter as ctk
from tkinter import messagebox
from controllers.gerente_controller import GerenteController


class ListaGerentes(ctk.CTkFrame):
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
            header, text="Gerentes Cadastrados",
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
        colunas = ["CPF", "Nome", "Celular", "Email", "Setor", "Ações"]
        frame_tabela = ctk.CTkFrame(self.content)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        for i, col in enumerate(colunas):
            lbl = ctk.CTkLabel(
                frame_tabela, text=col,
                font=ctk.CTkFont(weight="bold"),
                width=120
            )
            lbl.grid(row=0, column=i, padx=5, pady=8, sticky="w")

        gerentes = GerenteController.listar()
        for row, gerente in enumerate(gerentes, start=1):
            ctk.CTkLabel(frame_tabela, text=gerente["idcpf"], width=120).grid(row=row, column=0, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=gerente["nome"], width=120).grid(row=row, column=1, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=gerente["Celular"], width=120).grid(row=row, column=2, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=gerente["email"], width=120).grid(row=row, column=3, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=gerente["setor"], width=120).grid(row=row, column=4, padx=5, pady=4, sticky="w")

            btn_editar = ctk.CTkButton(
                frame_tabela, text="Editar", width=70,
                fg_color="#f39c12", hover_color="#e67e22",
                command=lambda cpf=gerente["idcpf"]: self.editar_gerente(cpf)
            )
            btn_editar.grid(row=row, column=5, padx=2)

            btn_excluir = ctk.CTkButton(
                frame_tabela, text="Excluir", width=70,
                fg_color="#e74c3c", hover_color="#c0392b",
                command=lambda cpf=gerente["idcpf"]: self.excluir_gerente(cpf)
            )
            btn_excluir.grid(row=row, column=6, padx=2)

    def editar_gerente(self, cpf):
        from views.edicao_gerente import EdicaoGerente
        EdicaoGerente(self, self.content, cpf, on_voltar=self.montar_tela)

    def excluir_gerente(self, cpf):
        if messagebox.askyesno("Confirmar", "Deseja excluir este gerente?"):
            GerenteController.deletar(cpf)
            self.montar_tela()
