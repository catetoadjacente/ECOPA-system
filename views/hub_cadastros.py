import customtkinter as ctk


class HubCadastros(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastros")
        self.geometry("800x600")

        # Frame centralizado
        self.frame = ctk.CTkFrame(self, width=600, height=400)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título "Gerente" à esquerda do frame
        self.label = ctk.CTkLabel(
            self.frame, text="Gerente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label.pack(side="left", padx=20, pady=20)

        # Botão "Novo" à direita do frame
        self.btn_novo = ctk.CTkButton(
            self.frame, text="Novo",
            width=100
        )
        self.btn_novo.pack(side="right", padx=20, pady=20)
