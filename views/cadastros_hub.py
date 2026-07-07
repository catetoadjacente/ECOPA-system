import customtkinter as ctk
from views.cadastro_gerente import CadastroGerente
from views.cadastro_clientes import CadastroCliente


class CadastrosHub(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content

        self.abrir_cadastros()

    def abrir_cadastros(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.2)

        label = ctk.CTkLabel(
            frame, text="Gerente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(side="left", padx=20, pady=20)

        btn_novo = ctk.CTkButton(
            frame, text="Novo",
            width=100,
            command=self.novo_gerente
        )
        btn_novo.pack(side="right", padx=20, pady=20)
        btn_acessar = ctk.CTkButton(
            frame, text="Acessar",
            width=100,
            command=self.acessar_gerentes
        )
        btn_acessar.pack(side="right", padx=20, pady=20)
        
        frame2 = ctk.CTkFrame(self.content)
        frame2.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.8, relheight=0.2)

        label2 = ctk.CTkLabel(
            frame2, text="Cliente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label2.pack(side="left", padx=20, pady=20)

        btn_novo2 = ctk.CTkButton(
            frame2, text="Novo",
            width=100,
            command=self.novo_cliente
        )
        btn_novo2.pack(side="right", padx=20, pady=20)

        btn_listar2 = ctk.CTkButton(
            frame2, text="Acessar",
            width=100,
            command=self.acessar_clientes
        )
        btn_listar2.pack(side="right", padx=(5, 20), pady=20)


    def novo_gerente(self):
        CadastroGerente(self, self.content, on_voltar=self.abrir_cadastros)
    
    def acessar_gerentes(self):
        from views.lista_gerentes import ListaGerentes
        ListaGerentes(self, self.content, on_voltar=self.abrir_cadastros)

    def novo_cliente(self):
        CadastroCliente(self, self.content, on_voltar=self.abrir_cadastros)

    def acessar_clientes(self):
        from views.lista_clientes import ListaClientes
        ListaClientes(self, self.content, on_voltar=self.abrir_cadastros)