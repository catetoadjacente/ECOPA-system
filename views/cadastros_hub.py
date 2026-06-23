import customtkinter as ctk
from views.cadastro_gerente import CadastroGerente


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

    def novo_gerente(self):
        CadastroGerente(self, self.content, on_voltar=self.abrir_cadastros)