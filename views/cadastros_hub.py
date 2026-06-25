import customtkinter as ctk
from views.cadastro_gerente import CadastroGerente
from views.cadastro_clientes import CadastroClienteView
from views.listar_clientes import ListarClientesView

class CadastrosHub(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content

        self.abrir_cadastros()

    def abrir_cadastros(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content, width=600, height=400)
        frame.place(relx=0.5, rely=0.5, anchor="center")

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
        
        frame2 = ctk.CTkFrame(self.content, width=600, height=400)
        frame2.place(relx=0.5, rely=0.7, anchor="center")

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
            frame2, text="Listar",
            width=100,
            command=self.listar_clientes
        )
        btn_listar2.pack(side="right", padx=(5, 20), pady=20)

        

    def novo_gerente(self):
        CadastroGerente(self, self.content, on_voltar=self.abrir_cadastros)
    
    def acessar_gerentes(self):
        from views.lista_gerentes import ListaGerentes
        ListaGerentes(self, self.content, on_voltar=self.abrir_cadastros)
        
    def novo_cliente(self):
        CadastroClienteView(self, self.content, on_voltar=self.abrir_cadastros)

    def listar_clientes(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ListarClientesView(self.content).pack(fill="both", expand=True)
 