import customtkinter as ctk
from tkinter import messagebox, filedialog
from controllers.coleta_controller import ColetaController
from controllers.ponto_controller import PontoController
from models.relatorio import Relatorio
from datetime import datetime
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
import os

plt.rcParams["font.family"] = "sans-serif"

ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"
ECOPA_ORANGE = "#f39c12"
ECOPA_LEAF = "#27ae60"
ECOPA_BLUE = "#3498db"
ECOPA_RED = "#e74c3c"


class RelatoriosView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(container, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)
        self._scroll = scroll

        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Relatorios",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Analise completa de coletas e destinacoes",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="Gerar PDF", width=120, height=36,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
            command=self._gerar_pdf
        ).pack(anchor="e")

        # Linha verde
        ctk.CTkFrame(scroll, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Filtros
        self._montar_filtros(scroll)

        # Dados iniciais
        self._dados_coletas = ColetaController.listar()
        self._montar_conteudo()

    def _montar_filtros(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=32, pady=(20, 0))

        ctk.CTkLabel(
            card, text="Filtros",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(14, 8))

        filtros = ctk.CTkFrame(card, fg_color="transparent")
        filtros.pack(fill="x", padx=20, pady=(0, 14))

        # Data inicio
        ctk.CTkLabel(
            filtros, text="De:", font=ctk.CTkFont(size=12),
            text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 4))

        self.entry_data_inicio = ctk.CTkEntry(
            filtros, placeholder_text="DD/MM/AAAA", width=120, height=36,
            corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER
        )
        self.entry_data_inicio.pack(side="left", padx=(0, 12))

        # Data fim
        ctk.CTkLabel(
            filtros, text="Ate:", font=ctk.CTkFont(size=12),
            text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 4))

        self.entry_data_fim = ctk.CTkEntry(
            filtros, placeholder_text="DD/MM/AAAA", width=120, height=36,
            corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER
        )
        self.entry_data_fim.pack(side="left", padx=(0, 12))

        # Ponto de coleta
        ctk.CTkLabel(
            filtros, text="Ponto:", font=ctk.CTkFont(size=12),
            text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 4))

        pontos = Relatorio.listar_pontos()
        nomes_pontos = ["TODOS"] + [p["estabelecimento"] for p in pontos]
        self._pontos_map = {p["estabelecimento"]: p["id_ponto"] for p in pontos}

        self.filtro_ponto = ctk.CTkComboBox(
            filtros, values=nomes_pontos, width=180, height=36,
            corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT
        )
        self.filtro_ponto.pack(side="left", padx=(0, 12))
        self.filtro_ponto.set("TODOS")

        # Status
        ctk.CTkLabel(
            filtros, text="Status:", font=ctk.CTkFont(size=12),
            text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 4))

        self.filtro_status = ctk.CTkComboBox(
            filtros, values=["TODOS", "Pendente", "Realizada"],
            width=130, height=36, corner_radius=10,
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT
        )
        self.filtro_status.pack(side="left", padx=(0, 12))
        self.filtro_status.set("TODOS")

        # Botoes
        ctk.CTkButton(
            filtros, text="Filtrar", width=90, height=36,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
            command=self._aplicar_filtros
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            filtros, text="Limpar", width=80, height=36,
            fg_color="transparent", hover_color=ECOPA_BG,
            corner_radius=10, font=ctk.CTkFont(size=12),
            text_color=ECOPA_GREEN, border_width=1, border_color=ECOPA_GREEN,
            command=self._limpar_filtros
        ).pack(side="left")

    def _parse_data(self, texto):
        if not texto or not texto.strip():
            return None
        try:
            return datetime.strptime(texto.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None

    def _aplicar_filtros(self):
        data_inicio = self._parse_data(self.entry_data_inicio.get())
        data_fim = self._parse_data(self.entry_data_fim.get())
        ponto_nome = self.filtro_ponto.get()
        id_ponto = self._pontos_map.get(ponto_nome) if ponto_nome != "TODOS" else None
        status = self.filtro_status.get()

        self._dados_coletas = Relatorio.coletas_filtradas(
            data_inicio=data_inicio, data_fim=data_fim,
            id_ponto=id_ponto, status=status
        )
        self._montar_conteudo()

    def _limpar_filtros(self):
        self.entry_data_inicio.delete(0, "end")
        self.entry_data_fim.delete(0, "end")
        self.filtro_ponto.set("TODOS")
        self.filtro_status.set("TODOS")
        self._dados_coletas = ColetaController.listar()
        self._montar_conteudo()

    def _montar_conteudo(self):
        # Remover conteudo anterior (apos filtros)
        for widget in self._scroll.winfo_children():
            if hasattr(widget, '_is_conteudo'):
                widget.destroy()

        scroll = self._scroll
        coletas = self._dados_coletas

        # Container de conteudo
        conteudo = ctk.CTkFrame(scroll, fg_color="transparent")
        conteudo._is_conteudo = True
        conteudo.pack(fill="x", padx=32, pady=(20, 0))

        # KPIs
        total = len(coletas)
        quantidade_total = sum(float(c["quantidade"] or 0) for c in coletas)
        pendentes = sum(1 for c in coletas if c["status"] == "Pendente")
        realizadas = sum(1 for c in coletas if c["status"] == "Realizada")

        destino = Relatorio.resumo_destinacoes()
        total_dest = len(destino)

        kpi_frame = ctk.CTkFrame(conteudo, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 16))
        kpi_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        kpis = [
            ("COLETAS", str(total), ECOPA_GREEN, "#e8f5e8"),
            ("TOTAL KG", f"{quantidade_total:.1f}", ECOPA_BLUE, "#e8f0f8"),
            ("PENDENTES", str(pendentes), ECOPA_ORANGE, "#fdf5e8"),
            ("REALIZADAS", str(realizadas), ECOPA_LEAF, "#e8f8e8"),
            ("DESTINACOES", str(total_dest), ECOPA_RED, "#fde8e8"),
        ]

        for i, (titulo, valor, cor, bg_cor) in enumerate(kpis):
            card = ctk.CTkFrame(
                kpi_frame, fg_color=ECOPA_WHITE, corner_radius=14,
                border_width=1, border_color=ECOPA_BORDER, height=90,
            )
            card.grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            card.grid_propagate(False)

            ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=2).pack(fill="x")

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=14, pady=(8, 10))

            ctk.CTkLabel(
                inner, text=titulo,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=ECOPA_TEXT_LIGHT, anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                inner, text=valor,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=ECOPA_GREEN_DARK, anchor="w"
            ).pack(anchor="w")

        # Graficos
        graficos_frame = ctk.CTkFrame(conteudo, fg_color="transparent")
        graficos_frame.pack(fill="x", pady=(0, 16))
        graficos_frame.grid_columnconfigure((0, 1), weight=1)

        self._grafico_pizza(graficos_frame, coletas)
        self._grafico_barras_pontos(graficos_frame, coletas)
        self._grafico_linha(graficos_frame, coletas)
        self._grafico_destinacoes(graficos_frame)

        # Tabela coletas por ponto
        self._tabela_por_ponto(conteudo)

        # Tabela destinacoes
        self._tabela_destinacoes(conteudo)

        # Rodape
        ctk.CTkLabel(
            conteudo, text=f"Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
            font=ctk.CTkFont(size=10), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(20, 10))

    def _grafico_pizza(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Coletas por Status",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 0))

        fig, ax = plt.subplots(figsize=(4.2, 3))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        from collections import Counter
        status_count = Counter(c["status"] for c in coletas)
        if status_count:
            cores = {"Pendente": ECOPA_ORANGE, "Realizada": ECOPA_LEAF}
            labels = list(status_count.keys())
            sizes = list(status_count.values())
            colors = [cores.get(l, "#999") for l in labels]
            ax.pie(
                sizes, labels=labels, autopct="%1.0f%%",
                colors=colors, startangle=90,
                textprops={"fontsize": 10},
                wedgeprops={"linewidth": 2, "edgecolor": ECOPA_WHITE}
            )
        else:
            ax.text(0.5, 0.5, "Sem dados", ha="center", va="center", fontsize=12)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(4, 8))

    def _grafico_barras_pontos(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=0, column=1, padx=(8, 0), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Coletas por Ponto (Kg)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 0))

        fig, ax = plt.subplots(figsize=(4.2, 3))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        ponto_qtd = defaultdict(float)
        for c in coletas:
            ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
        top = sorted(ponto_qtd.items(), key=lambda x: x[1], reverse=True)[:7]

        if top:
            nomes, qtds = zip(*top)
            ax.barh(list(nomes), list(qtds), color=ECOPA_GREEN, height=0.55,
                    edgecolor=ECOPA_GREEN_LIGHT, linewidth=0.5)
            ax.tick_params(labelsize=9)
            ax.invert_yaxis()
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_color(ECOPA_BORDER)
            ax.spines["left"].set_color(ECOPA_BORDER)
        else:
            ax.text(0.5, 0.5, "Sem dados", ha="center", va="center", fontsize=12)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(4, 8))

    def _grafico_linha(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=1, column=0, padx=(0, 8), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Coletas por Dia (ultimos 7)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 0))

        fig, ax = plt.subplots(figsize=(4.2, 3))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        from datetime import timedelta
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

        ax.plot(dias_str, valores, marker="o", color=ECOPA_GREEN, linewidth=2.5,
                markersize=7, markerfacecolor=ECOPA_WHITE,
                markeredgecolor=ECOPA_GREEN, markeredgewidth=2)
        ax.fill_between(range(len(dias_str)), valores, alpha=0.12, color=ECOPA_GREEN)
        ax.set_ylim(0, max(valores) + 2 if max(valores) > 0 else 5)
        ax.tick_params(labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(ECOPA_BORDER)
        ax.spines["left"].set_color(ECOPA_BORDER)
        ax.grid(axis="y", alpha=0.3, color=ECOPA_BORDER)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(4, 8))

    def _grafico_destinacoes(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=1, column=1, padx=(8, 0), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Destinacoes por Cliente",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 0))

        fig, ax = plt.subplots(figsize=(4.2, 3))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        dest = Relatorio.resumo_destinacoes()
        cliente_qtd = defaultdict(float)
        for d in dest:
            cliente_qtd[d["cliente"]] += float(d["quantidade"] or 0)
        top = sorted(cliente_qtd.items(), key=lambda x: x[1], reverse=True)[:7]

        if top:
            nomes, qtds = zip(*top)
            colors = [ECOPA_BLUE, ECOPA_GREEN, ECOPA_ORANGE, ECOPA_LEAF, "#9b59b6", "#e74c3c", "#1abc9c"]
            ax.barh(list(nomes), list(qtds), color=colors[:len(nomes)], height=0.55)
            ax.tick_params(labelsize=9)
            ax.invert_yaxis()
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_color(ECOPA_BORDER)
            ax.spines["left"].set_color(ECOPA_BORDER)
        else:
            ax.text(0.5, 0.5, "Sem destinacoes registradas",
                    ha="center", va="center", fontsize=11, color=ECOPA_TEXT_LIGHT)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(4, 8))

    def _tabela_por_ponto(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            card, text="Coletas por Ponto de Coleta",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 8))

        dados = Relatorio.coletas_por_ponto()

        # Cabecalho
        cabecalhos = ["Ponto", "Total Coletas", "Total Kg", "Pendentes", "Realizadas"]
        header_frame = ctk.CTkFrame(card, fg_color=ECOPA_GREEN, corner_radius=10)
        header_frame.pack(fill="x", padx=16, pady=(0, 4))

        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, width=160
            ).grid(row=0, column=col, padx=12, pady=8, sticky="w")

        if not dados:
            ctk.CTkLabel(
                card, text="Nenhum dado encontrado",
                font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=20)
            return

        for i, d in enumerate(dados):
            bg = ECOPA_BG if i % 2 == 0 else ECOPA_WHITE
            row = ctk.CTkFrame(card, fg_color=bg, corner_radius=0)
            row.pack(fill="x", padx=16)

            valores = [
                d["ponto"],
                str(d["total_coletas"] or 0),
                f"{float(d['total_kg'] or 0):.1f} Kg",
                str(d["pendentes"] or 0),
                str(d["realizadas"] or 0),
            ]

            for col, val in enumerate(valores):
                if col == 3 and int(d["pendentes"] or 0) > 0:
                    ctk.CTkLabel(
                        row, text=val, font=ctk.CTkFont(size=12),
                        text_color=ECOPA_ORANGE, width=160, anchor="w"
                    ).grid(row=0, column=col, padx=12, pady=6, sticky="w")
                elif col == 4 and int(d["realizadas"] or 0) > 0:
                    ctk.CTkLabel(
                        row, text=val, font=ctk.CTkFont(size=12),
                        text_color=ECOPA_LEAF, width=160, anchor="w"
                    ).grid(row=0, column=col, padx=12, pady=6, sticky="w")
                else:
                    ctk.CTkLabel(
                        row, text=val, font=ctk.CTkFont(size=12),
                        text_color=ECOPA_TEXT, width=160, anchor="w"
                    ).grid(row=0, column=col, padx=12, pady=6, sticky="w")

    def _tabela_destinacoes(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            card, text="Resumo de Destinacoes",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 8))

        dados = Relatorio.resumo_destinacoes()

        cabecalhos = ["Cliente", "CNPJ", "Ponto Origem", "Quantidade", "Data"]
        header_frame = ctk.CTkFrame(card, fg_color=ECOPA_GREEN, corner_radius=10)
        header_frame.pack(fill="x", padx=16, pady=(0, 4))

        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, width=150
            ).grid(row=0, column=col, padx=12, pady=8, sticky="w")

        if not dados:
            ctk.CTkLabel(
                card, text="Nenhuma destinacao registrada",
                font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=20)
            return

        for i, d in enumerate(dados):
            bg = ECOPA_BG if i % 2 == 0 else ECOPA_WHITE
            row = ctk.CTkFrame(card, fg_color=bg, corner_radius=0)
            row.pack(fill="x", padx=16)

            data_str = d["data_dest"].strftime("%d/%m/%Y") if d["data_dest"] else ""
            qtd_str = f"{float(d['quantidade'] or 0):.1f} Kg"
            valores = [d["cliente"], d["cnpj"], d["ponto"], qtd_str, data_str]

            for col, val in enumerate(valores):
                ctk.CTkLabel(
                    row, text=val, font=ctk.CTkFont(size=12),
                    text_color=ECOPA_TEXT, width=150, anchor="w"
                ).grid(row=0, column=col, padx=12, pady=6, sticky="w")

    def _gerar_pdf(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Salvar Relatorio",
            initialfile=f"relatorio_ecopa_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )
        if not caminho:
            return

        try:
            coletas = self._dados_coletas
            with PdfPages(caminho) as pdf:
                # Pagina 1: Titulo e KPIs
                fig1, ax1 = plt.subplots(figsize=(8.27, 11.69))
                fig1.patch.set_facecolor(ECOPA_WHITE)
                ax1.axis("off")

                ax1.text(0.5, 0.92, "Relatorio ECOPA", fontsize=28, fontweight="bold",
                         ha="center", va="top", color=ECOPA_GREEN_DARK)
                ax1.text(0.5, 0.88, f"Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
                         fontsize=11, ha="center", va="top", color=ECOPA_TEXT_LIGHT)

                total = len(coletas)
                qtd_total = sum(float(c["quantidade"] or 0) for c in coletas)
                pendentes = sum(1 for c in coletas if c["status"] == "Pendente")
                realizadas = sum(1 for c in coletas if c["status"] == "Realizada")

                y = 0.80
                ax1.text(0.1, y, "Resumo Geral", fontsize=16, fontweight="bold",
                         color=ECOPA_GREEN_DARK)
                y -= 0.05
                ax1.text(0.1, y, f"Total de Coletas: {total}", fontsize=12)
                y -= 0.04
                ax1.text(0.1, y, f"Quantidade Total: {qtd_total:.1f} Kg", fontsize=12)
                y -= 0.04
                ax1.text(0.1, y, f"Pendentes: {pendentes}", fontsize=12, color=ECOPA_ORANGE)
                y -= 0.04
                ax1.text(0.1, y, f"Realizadas: {realizadas}", fontsize=12, color=ECOPA_LEAF)

                plt.tight_layout()
                pdf.savefig(fig1)
                plt.close(fig1)

                # Pagina 2: Grafico de status (pizza)
                if coletas:
                    fig2, ax2 = plt.subplots(figsize=(8.27, 5))
                    from collections import Counter
                    status_count = Counter(c["status"] for c in coletas)
                    cores = {"Pendente": ECOPA_ORANGE, "Realizada": ECOPA_LEAF}
                    labels = list(status_count.keys())
                    sizes = list(status_count.values())
                    colors = [cores.get(l, "#999") for l in labels]
                    ax2.pie(sizes, labels=labels, autopct="%1.0f%%", colors=colors,
                            startangle=90, textprops={"fontsize": 14},
                            wedgeprops={"linewidth": 2, "edgecolor": ECOPA_WHITE})
                    ax2.set_title("Coletas por Status", fontsize=16, fontweight="bold",
                                  color=ECOPA_GREEN_DARK, pad=20)
                    plt.tight_layout()
                    pdf.savefig(fig2)
                    plt.close(fig2)

                # Pagina 3: Grafico por ponto (barras)
                ponto_qtd = defaultdict(float)
                for c in coletas:
                    ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
                if ponto_qtd:
                    fig3, ax3 = plt.subplots(figsize=(8.27, 5))
                    top = sorted(ponto_qtd.items(), key=lambda x: x[1], reverse=True)[:10]
                    nomes, qtds = zip(*top)
                    ax3.barh(list(nomes), list(qtds), color=ECOPA_GREEN, height=0.6)
                    ax3.invert_yaxis()
                    ax3.set_title("Coletas por Ponto (Kg)", fontsize=16, fontweight="bold",
                                  color=ECOPA_GREEN_DARK, pad=20)
                    ax3.spines["top"].set_visible(False)
                    ax3.spines["right"].set_visible(False)
                    plt.tight_layout()
                    pdf.savefig(fig3)
                    plt.close(fig3)

            messagebox.showinfo("Sucesso", f"Relatorio salvo em:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar PDF:\n{e}")
