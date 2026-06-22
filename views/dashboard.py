import customtkinter as ctk


class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Sidebar (frame à esquerda)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / título na sidebar
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="ECOPA System",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=(20, 40))

        # Botões de navegação
        self.btn_coleta = ctk.CTkButton(
            self.sidebar, text="Coleta",
            command=self.abrir_coleta
        )
        self.btn_coleta.pack(pady=5, padx=20, fill="x")

        self.btn_pontos = ctk.CTkButton(
            self.sidebar, text="Pontos",
            command=self.abrir_pontos
        )
        self.btn_pontos.pack(pady=5, padx=20, fill="x")

        self.btn_destinacoes = ctk.CTkButton(
            self.sidebar, text="Destinações",
            command=self.abrir_destinacoes
        )
        self.btn_destinacoes.pack(pady=5, padx=20, fill="x")

        self.btn_cadastros = ctk.CTkButton(
            self.sidebar, text="Cadastros",
            command=self.abrir_cadastros
        )
        self.btn_cadastros.pack(pady=5, padx=20, fill="x")

        self.btn_relatorios = ctk.CTkButton(
            self.sidebar, text="Relatórios",
            command=self.abrir_relatorios
        )
        self.btn_relatorios.pack(pady=5, padx=20, fill="x")

        # (opcional) botão sair no final
        self.btn_sair = ctk.CTkButton(
            self.sidebar, text="Sair", fg_color="#c0392b",
            hover_color="#e74c3c", command=self.sair
        )
        self.btn_sair.pack(side="bottom", pady=20, padx=20, fill="x")

        # Área de conteúdo principal (direita)
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        self.label_bem_vindo = ctk.CTkLabel(
            self.content, text="Bem-vindo!",
            font=ctk.CTkFont(size=24)
        )
        self.label_bem_vindo.pack(pady=50)

    def abrir_coleta(self):
        self.label_bem_vindo.configure(text="Coleta")

    def abrir_pontos(self):
        self.label_bem_vindo.configure(text="Pontos")

    def abrir_destinacoes(self):
        self.label_bem_vindo.configure(text="Destinações")

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

    def abrir_relatorios(self):
        self.label_bem_vindo.configure(text="Relatórios")

    def sair(self):
        self.master.destroy()


# Teste rápido (executar direto)
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1200x700")
    MainView(app).pack(fill="both", expand=True)
    app.mainloop()