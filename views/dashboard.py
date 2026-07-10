import customtkinter as ctk
from views.cadastros_hub import CadastrosHub
from views.coletas import ColetasView
from views.pontos import PontosView
from controllers.coleta_controller import ColetaController
from controllers.ponto_controller import PontoController
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams["font.family"] = "sans-serif"


class MainView(ctk.CTkFrame):
    def __init__(self, master, nome_usuario=""):
        super().__init__(master)
        self.nome_usuario = nome_usuario

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

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="#dcebdc")
        self.content.pack(side="right", fill="both", expand=True)

        self.abrir_dashboard()

    def abrir_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.after(100, self._montar_dashboard)

    def _montar_dashboard(self):
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="#dcebdc")
        scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            header,
            text=f"Bem-vindo, {self.nome_usuario or 'Usuário'}!",
            font=ctk.CTkFont(size=24, weight="bold"), anchor="w"
        ).pack(side="left")

        ctk.CTkButton(
            header, text="Atualizar", width=100,
            fg_color="#006d12", hover_color="#0a8f2c",
            command=self.abrir_dashboard
        ).pack(side="right")

        coletas = ColetaController.listar()
        pontos = PontoController.listar()

        total_coletas = len(coletas)
        pendentes = sum(1 for c in coletas if c["status"] == "Pendente")
        em_andamento = sum(1 for c in coletas if c["status"] == "Em andamento")
        finalizadas = sum(1 for c in coletas if c["status"] == "Finalizada")

        frame_cards = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_cards.pack(fill="x", padx=30, pady=10)

        cards = [
            ("Total Coletas", str(total_coletas), "#2c3e50"),
            ("Pendentes", str(pendentes), "#e67e22"),
            ("Em Andamento", str(em_andamento), "#3498db"),
            ("Finalizadas", str(finalizadas), "#27ae60"),
        ]

        for i, (tit, val, cor) in enumerate(cards):
            card = ctk.CTkFrame(
                frame_cards, fg_color="white", corner_radius=10,
                border_width=1, border_color="#ddd", width=200, height=90
            )
            card.grid(row=0, column=i, padx=8, pady=5)
            card.grid_propagate(False)

            ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=0).pack(fill="x")
            ctk.CTkLabel(card, text=tit, font=ctk.CTkFont(size=12),
                         text_color="#666").pack(pady=(12, 0))
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=28, weight="bold"),
                         text_color=cor).pack()

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
        fig.patch.set_facecolor("#dcebdc")

        # 1. Pizza - Status
        status_count = Counter(c["status"] for c in coletas)
        if status_count:
            cores_pizza = {"Pendente": "#e67e22", "Em andamento": "#3498db", "Finalizada": "#27ae60"}
            labels = list(status_count.keys())
            sizes = list(status_count.values())
            colors = [cores_pizza.get(l, "#999") for l in labels]
            axes[0].pie(sizes, labels=labels, autopct="%1.1f%%",
                        colors=colors, startangle=90, textprops={"fontsize": 10})
            axes[0].set_title("Status das Coletas", fontsize=13, fontweight="bold")
        else:
            axes[0].text(0.5, 0.5, "Sem dados", ha="center", va="center")

        # 2. Barras - Top 5 Pontos
        ponto_qtd = defaultdict(float)
        for c in coletas:
            ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
        top = sorted(ponto_qtd.items(), key=lambda x: x[1], reverse=True)[:5]
        if top:
            nomes, qtds = zip(*top)
            axes[1].barh(list(nomes), list(qtds), color="#006d12", height=0.6)
            axes[1].set_title("Top 5 Pontos (Kg)", fontsize=13, fontweight="bold")
            axes[1].tick_params(labelsize=9)
            axes[1].invert_yaxis()
        else:
            axes[1].text(0.5, 0.5, "Sem dados", ha="center", va="center")

        # 3. Linha - Coletas por dia (últimos 7)
        hoje = datetime.now().date()
        dias = [(hoje - timedelta(days=i)) for i in range(6, -1, -1)]
        qtd_por_dia = defaultdict(int)
        for c in coletas:
            if c["data_coleta"]:
                dia = c["data_coleta"].date()
                if (hoje - dia).days <= 6:
                    qtd_por_dia[dia] += 1
        valores = [qtd_por_dia.get(d, 0) for d in dias]
        dias_str = [d.strftime("%d/%m") for d in dias]
        axes[2].plot(dias_str, valores, marker="o", color="#e67e22", linewidth=2)
        axes[2].fill_between(range(len(dias_str)), valores, alpha=0.15, color="#e67e22")
        axes[2].set_title("Coletas por Dia", fontsize=13, fontweight="bold")
        axes[2].tick_params(labelsize=9)
        axes[2].set_ylim(0, max(valores) + 1 if valores else 1)

        plt.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=scroll)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=30, pady=(10, 30))

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