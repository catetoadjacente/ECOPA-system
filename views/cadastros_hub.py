import customtkinter as ctk


class CadastrosHub(ctk.CTkFrame):
    def __init__(self, master, on_voltar):
        super().__init__(master)
        self.on_voltar = on_voltar

        self.label_titulo = ctk.CTkLabel(
            self, text="Cadastros",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.label_titulo.pack(pady=50)