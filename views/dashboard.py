import customtkinter as ctk
from views.cadastros_hub import CadastrosHub
from views.coletas import ColetasView
from views.pontos import PontosView
from controllers.cliente_controller import ClienteController
from controllers.coleta_controller import ColetaController


class MainView(ctk.CTkFrame):
    def __init__(self, master, nome_usuario=""):
        super().__init__(master)
        self.nome_usuario = nome_usuario

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

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(35, 0))

        ctk.CTkLabel(
            header,
            text=f"Bem-vindo, {self.nome_usuario or 'Usuário'}!",
            font=ctk.CTkFont(size=26, weight="bold"), anchor="w"
        ).pack(side="left")

        ctk.CTkButton(
            header, text="🔄 Atualizar", width=100,
            fg_color="#006d12", hover_color="#0a8f2c",
            command=self.abrir_dashboard
        ).pack(side="right")

        ctk.CTkLabel(
            self.content,
            text="Resumo geral do sistema",
            font=ctk.CTkFont(size=14), anchor="w",
            text_color="#555555"
        ).pack(anchor="w", padx=35, pady=(2, 25))

        frame_cards = ctk.CTkFrame(self.content, fg_color="transparent")
        frame_cards.pack(fill="x", padx=35, pady=5)

       
        coletas = ColetaController.listar()

        
        total_coletas = len(coletas)
        pendentes = sum(1 for c in coletas if c["status"] == "Pendente")
        em_andamento = sum(1 for c in coletas if c["status"] == "Em andamento")
        finalizadas = sum(1 for c in coletas if c["status"] == "Finalizada")

        cards = [
            ("📦", "Total de Coletas", str(total_coletas), "#2c3e50"),
            ("⏳", "Pendentes", str(pendentes), "#e67e22"),
            ("🔄", "Em Andamento", str(em_andamento), "#3498db"),
            ("✅", "Finalizadas", str(finalizadas), "#27ae60"),
        ]

        for i, (icone, titulo, valor, cor) in enumerate(cards):
            card = ctk.CTkFrame(
                frame_cards, fg_color="white", corner_radius=12,
                border_width=1, border_color="#e0e0e0",
                width=180, height=130
            )
            card.grid(row=0, column=i, padx=8, pady=5)
            card.grid_propagate(False)

            barra = ctk.CTkFrame(card, fg_color=cor, height=5, corner_radius=0)
            barra.pack(fill="x")

            ctk.CTkLabel(card, text=icone, font=ctk.CTkFont(size=22),
                         text_color=cor).pack(pady=(18, 2))

            ctk.CTkLabel(
                card, text=titulo,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#666666"
            ).pack()

            ctk.CTkLabel(
                card, text=valor,
                font=ctk.CTkFont(size=30, weight="bold"),
                text_color=cor
            ).pack(pady=(5, 0))

        ctk.CTkFrame(self.content, fg_color="#cccccc", height=1).pack(
            fill="x", padx=35, pady=(30, 15)
        )

        header_tabela = ctk.CTkFrame(self.content, fg_color="transparent")
        header_tabela.pack(fill="x", padx=35, pady=(0, 10))

        ctk.CTkLabel(
            header_tabela, text="Todas as Coletas",
            font=ctk.CTkFont(size=16, weight="bold"), anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            header_tabela, text=f"{total_coletas} registros",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="e"
        ).pack(side="right")

        frame_tabela = ctk.CTkFrame(
            self.content, fg_color="white", corner_radius=12,
            border_width=1, border_color="#e0e0e0"
        )
        frame_tabela.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        cabecalhos = ["ID", "Ponto", "Motorista", "Quantidade", "Data", "Status"]
        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                frame_tabela, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#888888"
            ).grid(row=0, column=col, padx=18, pady=(12, 6), sticky="w")

        status_cores = {
            "Finalizada": ("#27ae60", "#eafaf1"),
            "Pendente": ("#e67e22", "#fef5e7"),
            "Em andamento": ("#3498db", "#ebf5fb"),
        }

        for linha, c in enumerate(coletas, start=1):
            id_str = f"#{int(c['id']):06d}"
            data_str = c["data_coleta"].strftime("%d/%m/%Y") if c["data_coleta"] else "-"
            qtd_str = f"{float(c['quantidade']):.1f} Kg" if c["quantidade"] else "-"
            st = c["status"]
            cor_texto, cor_fundo = status_cores.get(st, ("#666666", "#f5f5f5"))

            registro = [id_str, c["ponto"], c["motorista"], qtd_str, data_str]
            for col, valor in enumerate(registro):
                ctk.CTkLabel(
                    frame_tabela, text=valor,
                    font=ctk.CTkFont(size=13),
                    text_color="#444444", anchor="w"
                ).grid(row=linha, column=col, padx=18, pady=5, sticky="w")

            ctk.CTkLabel(
                frame_tabela, text=f"  {st}  ",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=cor_texto, fg_color=cor_fundo,
                corner_radius=6
            ).grid(row=linha, column=5, padx=18, pady=5, sticky="w")

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