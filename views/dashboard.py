import customtkinter as ctk
from PIL import Image
import os
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

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons")

# Paleta ECOPA Moderna
ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_GREEN_BG = "#f0f7f0"
ECOPA_LEAF = "#27ae60"
ECOPA_WHITE = "#ffffff"
ECOPA_CARD_BG = "#ffffff"
ECOPA_SIDEBAR_BG = "#ffffff"
ECOPA_SIDEBAR_ACTIVE = "#e8f5e8"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"
ECOPA_SHADOW = "#00000010"
ECOPA_ORANGE = "#f39c12"
ECOPA_BLUE = "#3498db"
ECOPA_RED = "#e74c3c"
ECOPA_YELLOW = "#f1c40f"


def carregar_icone(nome, tamanho=20):
    """Carrega icone de assets/icons/{nome}.png. Retorna None se nao existir."""
    caminho = os.path.join(ICONS_DIR, f"{nome}.png")
    if os.path.exists(caminho):
        img = Image.open(caminho).resize((tamanho, tamanho), Image.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(tamanho, tamanho))
    return None


class MainView(ctk.CTkFrame):
    def __init__(self, master, nome_usuario=""):
        super().__init__(master)
        self.nome_usuario = nome_usuario
        self.configure(fg_color=ECOPA_GREEN_BG)

        # === SIDEBAR ===
        self.sidebar = ctk.CTkFrame(
            self, width=260, corner_radius=0,
            fg_color=ECOPA_SIDEBAR_BG,
            border_width=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo ECOPA
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=24, pady=(28, 0))

        leaf_icon = ctk.CTkLabel(
            logo_frame, text="🌿",
            font=ctk.CTkFont(size=30), text_color=ECOPA_GREEN
        )
        leaf_icon.pack(side="left", padx=(0, 8))

        ecopa_label = ctk.CTkLabel(
            logo_frame, text="ECOPA",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ECOPA_GREEN_DARK
        )
        ecopa_label.pack(side="left")

        # Linha separadora
        ctk.CTkFrame(self.sidebar, fg_color=ECOPA_BORDER, height=1).pack(
            fill="x", padx=24, pady=(16, 8)
        )

        # Menu items
        self._botoes_menu = {}
        botoes = [
            ("dashboard",    "Dashboard",    self.abrir_dashboard,    "📊"),
            ("coletas",      "Coletas",      self.abrir_coleta,      "🚛"),
            ("destinacoes",  "Destinações",  self.abrir_destinacoes,  "♻️"),
            ("cadastros",    "Cadastros",    self.abrir_cadastros,   "📋"),
            ("relatorios",   "Relatórios",   self.abrir_relatorios,  "📈"),
            ("pontos",       "Pontos",       self.abrir_pontos,      "📍"),
            ("gerente",      "Gerente",      self.abrir_gerente,     "👤"),
        ]

        for nome_icone, texto, comando, emoji in botoes:
            btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=44)
            btn_frame.pack(fill="x", padx=12, pady=2)
            btn_frame.pack_propagate(False)

            emoji_lbl = ctk.CTkLabel(
                btn_frame, text=emoji,
                font=ctk.CTkFont(size=18), text_color=ECOPA_GREEN,
                width=32
            )
            emoji_lbl.pack(side="left", padx=(12, 4))

            btn = ctk.CTkButton(
                btn_frame, text=texto,
                fg_color="transparent", hover_color=ECOPA_SIDEBAR_ACTIVE,
                anchor="w", height=40,
                font=ctk.CTkFont(size=14, weight="normal"),
                text_color=ECOPA_TEXT,
                command=comando
            )
            btn.pack(side="left", fill="both", expand=True)
            self._botoes_menu[nome_icone] = (btn_frame, btn)

        # Botao Sair
        sair_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=44)
        sair_frame.pack(fill="x", padx=12, pady=2, side="bottom", before=None)
        sair_frame.pack_propagate(False)

        sair_emoji = ctk.CTkLabel(
            sair_frame, text="🚪",
            font=ctk.CTkFont(size=18), text_color=ECOPA_RED,
            width=32
        )
        sair_emoji.pack(side="left", padx=(12, 4))

        ctk.CTkButton(
            sair_frame, text="Sair",
            fg_color="transparent", hover_color="#fde8e8",
            anchor="w", height=40,
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color=ECOPA_RED,
            command=self.sair
        ).pack(side="left", fill="both", expand=True)

        # === AREA PRINCIPAL ===
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=ECOPA_GREEN_BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.abrir_dashboard()
        self._destacar_menu("dashboard")

    def _destacar_menu(self, ativo):
        for nome, (frame, btn) in self._botoes_menu.items():
            if nome == ativo:
                frame.configure(fg_color=ECOPA_SIDEBAR_ACTIVE)
                btn.configure(text_color=ECOPA_GREEN, font=ctk.CTkFont(size=14, weight="bold"))
            else:
                frame.configure(fg_color="transparent")
                btn.configure(text_color=ECOPA_TEXT, font=ctk.CTkFont(size=14, weight="normal"))

    # ============================================================
    # DASHBOARD
    # ============================================================
    def abrir_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("dashboard")
        self.after(100, self._montar_dashboard)

    def _montar_dashboard(self):
        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_GREEN_BG)
        scroll.pack(fill="both", expand=True)

        # === HEADER ===
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")

        ctk.CTkLabel(
            left_header,
            text=f"Olá, {self.nome_usuario or 'Usuário'}!",
            font=ctk.CTkFont(size=26, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_header,
            text="Supervisor de residuos e coleta",
            font=ctk.CTkFont(size=12), anchor="w",
            text_color=ECOPA_TEXT_LIGHT
        ).pack(anchor="w", pady=(2, 0))

        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.pack(side="right", anchor="ne")

        ctk.CTkLabel(
            right_header,
            text=datetime.now().strftime("%d de %B de %Y"),
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(anchor="e")

        ctk.CTkLabel(
            right_header,
            text=datetime.now().strftime("%A"),
            font=ctk.CTkFont(size=11), text_color=ECOPA_TEXT_LIGHT
        ).pack(anchor="e")

        # Botao atualizar
        ctk.CTkButton(
            right_header, text="Atualizar", width=100, height=32,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            command=self.abrir_dashboard
        ).pack(anchor="e", pady=(6, 0))

        # Linha verde
        ctk.CTkFrame(scroll, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # === DADOS ===
        coletas = ColetaController.listar()
        pontos = PontoController.listar()

        total_coletas = len(coletas)
        total_pontos = len(pontos)
        quantidade_total = sum(float(c["quantidade"] or 0) for c in coletas)
        pendentes = sum(1 for c in coletas if c["status"] == "Pendente")
        realizadas = sum(1 for c in coletas if c["status"] == "Realizada")

        # === KPI CARDS ===
        frame_cards = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_cards.pack(fill="x", padx=32, pady=(20, 0))
        frame_cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cards_data = [
            ("🚛", "COLETAS HOJE", str(total_coletas), ECOPA_GREEN, "#e8f5e8"),
            ("📍", "PONTOS ATIVOS", str(total_pontos), ECOPA_BLUE, "#e8f0f8"),
            ("⏳", "PENDENTES", str(pendentes), ECOPA_ORANGE, "#fdf5e8"),
            ("✅", "REALIZADAS", str(realizadas), ECOPA_LEAF, "#e8f8e8"),
        ]

        for i, (emoji, titulo, valor, cor, bg_cor) in enumerate(cards_data):
            card = ctk.CTkFrame(
                frame_cards, fg_color=ECOPA_WHITE, corner_radius=16,
                border_width=1, border_color=ECOPA_BORDER, height=100,
            )
            card.grid(row=0, column=i, padx=6, pady=5, sticky="ew")
            card.grid_propagate(False)

            # Top accent bar
            ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=2).pack(fill="x")

            # Conteudo
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=16, pady=(10, 12))

            # Icone
            icon_frame = ctk.CTkFrame(inner, fg_color=bg_cor, corner_radius=10, width=44, height=44)
            icon_frame.pack(anchor="w", pady=(0, 8))
            icon_frame.pack_propagate(False)

            ctk.CTkLabel(
                icon_frame, text=emoji, font=ctk.CTkFont(size=22)
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                inner, text=titulo,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=ECOPA_TEXT_LIGHT, anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                inner, text=valor,
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=ECOPA_GREEN_DARK, anchor="w"
            ).pack(anchor="w")

        # === GRAFICOS ===
        graficos_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        graficos_frame.pack(fill="x", padx=32, pady=(20, 0))
        graficos_frame.grid_columnconfigure((0, 1), weight=1)

        # Grafico 1 - Pizza Status
        card_pizza = ctk.CTkFrame(
            graficos_frame, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card_pizza.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")

        ctk.CTkLabel(
            card_pizza, text="Resumo de Coletas",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        fig1, ax1 = plt.subplots(figsize=(4.5, 3.2))
        fig1.patch.set_facecolor(ECOPA_WHITE)
        ax1.set_facecolor(ECOPA_WHITE)

        status_count = Counter(c["status"] for c in coletas)
        if status_count:
            cores_pizza = {"Pendente": ECOPA_ORANGE, "Realizada": ECOPA_LEAF}
            labels = list(status_count.keys())
            sizes = list(status_count.values())
            colors = [cores_pizza.get(l, "#999") for l in labels]
            wedges, texts, autotexts = ax1.pie(
                sizes, labels=labels, autopct="%1.0f%%",
                colors=colors, startangle=90,
                textprops={"fontsize": 10},
                wedgeprops={"linewidth": 2, "edgecolor": ECOPA_WHITE}
            )
            for t in autotexts:
                t.set_fontweight("bold")
        else:
            ax1.text(0.5, 0.5, "Sem dados", ha="center", va="center", fontsize=12)

        plt.tight_layout(pad=1)
        canvas1 = FigureCanvasTkAgg(fig1, master=card_pizza)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Grafico 2 - Barras Top Pontos
        card_barras = ctk.CTkFrame(
            graficos_frame, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card_barras.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

        ctk.CTkLabel(
            card_barras, text="Top 5 Pontos (Kg)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        fig2, ax2 = plt.subplots(figsize=(4.5, 3.2))
        fig2.patch.set_facecolor(ECOPA_WHITE)
        ax2.set_facecolor(ECOPA_WHITE)

        ponto_qtd = defaultdict(float)
        for c in coletas:
            ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
        top = sorted(ponto_qtd.items(), key=lambda x: x[1], reverse=True)[:5]
        if top:
            nomes, qtds = zip(*top)
            bars = ax2.barh(list(nomes), list(qtds), color=ECOPA_GREEN, height=0.55,
                           edgecolor=ECOPA_GREEN_LIGHT, linewidth=0.5)
            ax2.tick_params(labelsize=9)
            ax2.invert_yaxis()
            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            ax2.spines["bottom"].set_color(ECOPA_BORDER)
            ax2.spines["left"].set_color(ECOPA_BORDER)
        else:
            ax2.text(0.5, 0.5, "Sem dados", ha="center", va="center", fontsize=12)

        plt.tight_layout(pad=1)
        canvas2 = FigureCanvasTkAgg(fig2, master=card_barras)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # === SEGUNDA ROW GRAFICOS ===
        graficos2_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        graficos2_frame.pack(fill="x", padx=32, pady=(10, 0))
        graficos2_frame.grid_columnconfigure((0, 1), weight=1)

        # Grafico 3 - Linha Coletas por Dia
        card_linha = ctk.CTkFrame(
            graficos2_frame, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card_linha.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")

        ctk.CTkLabel(
            card_linha, text="Coletas por Dia (últimos 7)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        fig3, ax3 = plt.subplots(figsize=(4.5, 3.2))
        fig3.patch.set_facecolor(ECOPA_WHITE)
        ax3.set_facecolor(ECOPA_WHITE)

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

        ax3.plot(dias_str, valores, marker="o", color=ECOPA_GREEN, linewidth=2.5,
                markersize=7, markerfacecolor=ECOPA_WHITE, markeredgecolor=ECOPA_GREEN, markeredgewidth=2)
        ax3.fill_between(range(len(dias_str)), valores, alpha=0.12, color=ECOPA_GREEN)
        ax3.set_ylim(0, max(valores) + 2 if max(valores) > 0 else 5)
        ax3.tick_params(labelsize=9)
        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)
        ax3.spines["bottom"].set_color(ECOPA_BORDER)
        ax3.spines["left"].set_color(ECOPA_BORDER)
        ax3.grid(axis="y", alpha=0.3, color=ECOPA_BORDER)

        plt.tight_layout(pad=1)
        canvas3 = FigureCanvasTkAgg(fig3, master=card_linha)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Card informativo ao lado
        card_info = ctk.CTkFrame(
            graficos2_frame, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card_info.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

        ctk.CTkLabel(
            card_info, text="Resumo do Dia",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        # Metricas resumo
        metricas = [
            ("Total Coletado", f"{quantidade_total:.1f} Kg", ECOPA_GREEN),
            ("Pontos Cadastrados", str(total_pontos), ECOPA_BLUE),
            ("Coletas Pendentes", str(pendentes), ECOPA_ORANGE),
            ("Coletas Realizadas", str(realizadas), ECOPA_LEAF),
        ]

        for titulo, valor, cor in metricas:
            met_frame = ctk.CTkFrame(card_info, fg_color="transparent")
            met_frame.pack(fill="x", padx=20, pady=8)

            ctk.CTkFrame(met_frame, fg_color=cor, width=4, corner_radius=2).pack(
                side="left", fill="y", padx=(0, 12), pady=2
            )

            left_met = ctk.CTkFrame(met_frame, fg_color="transparent")
            left_met.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                left_met, text=titulo,
                font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT,
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                left_met, text=valor,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=ECOPA_GREEN_DARK, anchor="w"
            ).pack(anchor="w")

        # Rodape
        ctk.CTkLabel(
            scroll, text=f"© {datetime.now().year} ECOPA System — Todos os direitos reservados",
            font=ctk.CTkFont(size=10), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(30, 15))

    # ============================================================
    # NAVEGACAO
    # ============================================================
    def abrir_gerente(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("gerente")
        from views.gerente import ListaGerentes
        ListaGerentes(self, self.content, on_voltar=self.abrir_dashboard)

    def abrir_coleta(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("coletas")
        ColetasView(self, self.content)

    def abrir_pontos(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("pontos")
        PontosView(self, self.content)

    def abrir_destinacoes(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("destinacoes")
        from views.destinacoes import DestinacoesView
        DestinacoesView(self, self.content)

    def abrir_cadastros(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("cadastros")
        CadastrosHub(self, self.content)

    def abrir_relatorios(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("relatorios")
        from views.relatorios import RelatoriosView
        RelatoriosView(self, self.content)

    def sair(self):
        self.winfo_toplevel().destroy()
