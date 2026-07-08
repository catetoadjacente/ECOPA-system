import customtkinter as ctk
from views.cadastros_hub import CadastrosHub
from views.coletas import ColetasView
from views.pontos import PontosView


class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#006d12")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="ECOPA",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(30, 40))

        botoes = [
            ("Dashboard",    self.abrir_dashboard),
            ("Gerente",      self.abrir_gerente),
            ("Coletas",      self.abrir_coleta),
            ("Pontos",       self.abrir_pontos),
            ("Destinações",  self.abrir_destinacoes),
            ("Cadastros",    self.abrir_cadastros),
            ("Relatórios",   self.abrir_relatorios),
        ]

        for texto, comando in botoes:
            ctk.CTkButton(
                self.sidebar, text=texto,
                fg_color="transparent", hover_color="#0a8f2c",
                anchor="w", command=comando
            ).pack(fill="x", padx=15, pady=4)

        ctk.CTkButton(
            self.sidebar, text="Sair", fg_color="#c0392b",
            hover_color="#e74c3c", command=self.sair
        ).pack(side="bottom", pady=20, padx=15, fill="x")

        # Área de conteúdo
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="#dcebdc")
        self.content.pack(side="right", fill="both", expand=True)

        self.abrir_dashboard()

    def abrir_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.content, text="Bem-vindo!",
            font=ctk.CTkFont(size=24)
        ).pack(pady=50)

    def abrir_gerente(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        from views.lista_gerentes import ListaGerentes
        ListaGerentes(self, self.content, on_voltar=self.abrir_dashboard)

    def abrir_coleta(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ColetasView(self, self.content)

    def abrir_pontos(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        PontosView(self, self.content)

    def abrir_destinacoes(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.content, text="Destinações",
            font=ctk.CTkFont(size=24)
        ).pack(pady=50)

    def abrir_cadastros(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        CadastrosHub(self, self.content)

    def abrir_relatorios(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.content, text="Relatórios",
            font=ctk.CTkFont(size=24)
        ).pack(pady=50)

    def sair(self):
        self.winfo_toplevel().destroy()
