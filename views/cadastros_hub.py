import customtkinter as ctk


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
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content, width=500, height=450)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            frame, text="Novo Gerente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=(20, 15))

        campos = ["CPF", "Nome", "Celular", "Email", "Senha", "Setor"]
        self.entries_gerente = {}

        for campo in campos:
            lbl = ctk.CTkLabel(frame, text=campo + ":")
            lbl.pack(anchor="w", padx=20)
            entry = ctk.CTkEntry(frame, width=350)
            entry.pack(padx=20, pady=(0, 10))
            self.entries_gerente[campo] = entry

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        btn_salvar = ctk.CTkButton(
            btn_frame, text="Salvar", width=120,
            fg_color="#27ae60", hover_color="#2ecc71"
        )
        btn_salvar.pack(side="left", padx=10)

        btn_voltar = ctk.CTkButton(
            btn_frame, text="Voltar", width=120,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            command=self.abrir_cadastros
        )
        btn_voltar.pack(side="left", padx=10)
