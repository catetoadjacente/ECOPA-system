import customtkinter as ctk
from views.cadastros_hub import CadastrosHub


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
        self.cadastros_hub = CadastrosHub(self, self.content)

    def abrir_relatorios(self):
        self.label_bem_vindo.configure(text="Relatórios")

    def sair(self):
        self.winfo_toplevel().destroy()


# Teste rápido (executar direto)
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1200x700")
    MainView(app).pack(fill="both", expand=True)
    app.mainloop()