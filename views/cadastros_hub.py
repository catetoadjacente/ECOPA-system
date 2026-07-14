import customtkinter as ctk
from views.cadastro_gerente import CadastroGerente
from views.cadastro_pontos import CadastroPonto
from views.cadastro_coleta import CadastroColeta


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

        label = ctk.CTkLabel(frame, text="Gerente",font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(side="left", padx=20, pady=20)

        btn_novo = ctk.CTkButton(
            frame, text="Novo",
            width=100,
            command=self.novo_gerente
        )
        btn_novo.pack(side="right", padx=20, pady=20)
        
        
        frame2 = ctk.CTkFrame(self.content)
        frame2.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.8, relheight=0.2)

        label2 = ctk.CTkLabel(
            frame2, text="Ponto de Coleta",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label2.pack(side="left", padx=20, pady=20)

        btn_novo2 = ctk.CTkButton(
            frame2, text="Novo",
            width=100,
            command=self.novo_ponto
        )
        btn_novo2.pack(side="right", padx=20, pady=20)


        frame3 = ctk.CTkFrame(self.content)
        frame3.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.8, relheight=0.2)

        label3 = ctk.CTkLabel(
            frame3, text="Coleta",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label3.pack(side="left", padx=20, pady=20)

        btn_novo3 = ctk.CTkButton(
            frame3, text="Novo",
            width=100,
            command=self.nova_coleta
        )
        btn_novo3.pack(side="right", padx=20, pady=20)

        


    def novo_gerente(self):
        CadastroGerente(self, self.content, on_voltar=self.abrir_cadastros)
    

    def novo_ponto(self):
        CadastroPonto(self, self.content, on_voltar=self.abrir_cadastros)

    def nova_coleta(self):
        CadastroColeta(self, self.content, on_voltar=self.abrir_cadastros)