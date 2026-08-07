import customtkinter as ctk
from tkinter import messagebox, filedialog
from models.relatorio import Relatorio
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import threading
import queue
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages

plt.rcParams["font.family"] = "sans-serif"

from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE,
    ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE, ECOPA_LEAF,
    ECOPA_BLUE, ECOPA_RED, font, font_title, font_small, font_small_bold,
)


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
            left, text="Relatórios",
            font=font_title(30), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Analise completa de coletas e destinações",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="Gerar PDF", width=120, height=36,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font_small_bold(12),
            command=self._gerar_pdf
        ).pack(anchor="e")

        # Linha verde
        ctk.CTkFrame(scroll, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Filtros
        self._montar_filtros(scroll)

        # Dados iniciais
        self._dados_coletas = Relatorio.coletas_filtradas()
        self._filtro_data_inicio = None
        self._filtro_data_fim = None
        self._montar_conteudo()

    def _montar_filtros(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=32, pady=(20, 0))

        ctk.CTkLabel(
            card, text="Filtros",
            font=font(13, "bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(14, 8))

        filtros = ctk.CTkFrame(card, fg_color="transparent")
        filtros.pack(fill="x", padx=20, pady=(0, 14))

        # Data inicio
        ctk.CTkLabel(
            filtros, text="De:", font=font_small(12),
            text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 4))

        self.entry_data_inicio = ctk.CTkEntry(
            filtros, placeholder_text="DD/MM/AAAA", width=120, height=36,
            corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER
        )
        self.entry_data_inicio.pack(side="left", padx=(0, 12))

        # Data fim
        ctk.CTkLabel(
            filtros, text="Até:", font=font_small(12),
            text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 4))

        self.entry_data_fim = ctk.CTkEntry(
            filtros, placeholder_text="DD/MM/AAAA", width=120, height=36,
            corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER
        )
        self.entry_data_fim.pack(side="left", padx=(0, 12))

        # Ponto de coleta
        ctk.CTkLabel(
            filtros, text="Ponto:", font=font_small(12),
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
            filtros, text="Status:", font=font_small(12),
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
            corner_radius=10, font=font_small_bold(12),
            command=self._aplicar_filtros
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            filtros, text="Limpar", width=80, height=36,
            fg_color="transparent", hover_color=ECOPA_BG,
            corner_radius=10, font=font_small(12),
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
        data_inicio_texto = self.entry_data_inicio.get().strip()
        data_fim_texto = self.entry_data_fim.get().strip()

        data_inicio = self._parse_data(data_inicio_texto)
        if data_inicio_texto and data_inicio is None:
            messagebox.showwarning("Aviso", "Data inicial invalida. Use o formato DD/MM/AAAA.")
            return
        data_fim = self._parse_data(data_fim_texto)
        if data_fim_texto and data_fim is None:
            messagebox.showwarning("Aviso", "Data final invalida. Use o formato DD/MM/AAAA.")
            return
        # Incluir todo o dia final (ate 23:59:59)
        if data_fim:
            data_fim = data_fim + " 23:59:59"

        ponto_nome = self.filtro_ponto.get()
        id_ponto = self._pontos_map.get(ponto_nome) if ponto_nome != "TODOS" else None
        status = self.filtro_status.get()

        self._filtro_data_inicio = data_inicio
        self._filtro_data_fim = data_fim

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
        self._filtro_data_inicio = None
        self._filtro_data_fim = None
        self._dados_coletas = Relatorio.coletas_filtradas()
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

        destino = Relatorio.resumo_destinacoes(
            data_inicio=self._filtro_data_inicio,
            data_fim=self._filtro_data_fim)
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
                font=font_small_bold(10),
                text_color=ECOPA_TEXT_LIGHT, anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                inner, text=valor,
                font=font(24, "bold"),
                text_color=ECOPA_GREEN_DARK, anchor="w"
            ).pack(anchor="w")

        # Graficos
        graficos_frame = ctk.CTkFrame(conteudo, fg_color="transparent")
        graficos_frame.pack(fill="x", pady=(0, 16))
        graficos_frame.grid_columnconfigure((0, 1), weight=1)

        self._grafico_pizza(graficos_frame, coletas)
        self._grafico_barras_pontos(graficos_frame, coletas)
        self._grafico_linha(graficos_frame, coletas)
        self._grafico_destinacoes(graficos_frame, destino)

        # Tabela coletas por ponto
        self._tabela_por_ponto(conteudo, coletas)

        # Tabela destinacoes
        self._tabela_destinacoes(conteudo, destino)

        # Rodape
        ctk.CTkLabel(
            conteudo, text=f"Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
            font=font_small(10), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(20, 10))

    def _grafico_pizza(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Coletas por Status",
            font=font(14, "bold"),
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
        plt.close(fig)

    def _grafico_barras_pontos(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=0, column=1, padx=(8, 0), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Coletas por Ponto (Kg)",
            font=font(14, "bold"),
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
        plt.close(fig)

    def _grafico_linha(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=1, column=0, padx=(0, 8), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Coletas por Dia (ultimos 7)",
            font=font(14, "bold"),
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
        plt.close(fig)

    def _grafico_destinacoes(self, parent, dest):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.grid(row=1, column=1, padx=(8, 0), pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            card, text="Destinações por Cliente",
            font=font(14, "bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 0))

        fig, ax = plt.subplots(figsize=(4.2, 3))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        cliente_qtd = defaultdict(float)
        for d in dest:
            cliente_qtd[d["destinacao"]] += float(d["total_kg"] or 0)
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
            ax.text(0.5, 0.5, "Sem destinações registradas",
                    ha="center", va="center", fontsize=11, color=ECOPA_TEXT_LIGHT)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(4, 8))
        plt.close(fig)

    def _tabela_por_ponto(self, parent, coletas):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            card, text="Coletas por Ponto de Coleta",
            font=font(15, "bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 8))

        # Agregar dados a partir das coletas filtradas
        agg = defaultdict(lambda: {"ponto": "", "total_coletas": 0, "total_kg": 0.0, "pendentes": 0, "realizadas": 0})
        for c in coletas:
            ponto = c["ponto"]
            a = agg[ponto]
            a["ponto"] = ponto
            a["total_coletas"] += 1
            a["total_kg"] += float(c["quantidade"] or 0)
            if c["status"] == "Pendente":
                a["pendentes"] += 1
            elif c["status"] == "Realizada":
                a["realizadas"] += 1
        dados = sorted(agg.values(), key=lambda d: d["total_coletas"], reverse=True)

        # Cabecalho
        cabecalhos = ["Ponto", "Total Coletas", "Total Kg", "Pendentes", "Realizadas"]
        header_frame = ctk.CTkFrame(card, fg_color=ECOPA_GREEN, corner_radius=10)
        header_frame.pack(fill="x", padx=16, pady=(0, 4))

        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=font_small_bold(12),
                text_color=ECOPA_WHITE, width=160
            ).grid(row=0, column=col, padx=12, pady=8, sticky="w")

        if not dados:
            ctk.CTkLabel(
                card, text="Nenhum dado encontrado",
                font=font_small(12), text_color=ECOPA_TEXT_LIGHT
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
                        row, text=val, font=font_small(12),
                        text_color=ECOPA_ORANGE, width=160, anchor="w"
                    ).grid(row=0, column=col, padx=12, pady=6, sticky="w")
                elif col == 4 and int(d["realizadas"] or 0) > 0:
                    ctk.CTkLabel(
                        row, text=val, font=font_small(12),
                        text_color=ECOPA_LEAF, width=160, anchor="w"
                    ).grid(row=0, column=col, padx=12, pady=6, sticky="w")
                else:
                    ctk.CTkLabel(
                        row, text=val, font=font_small(12),
                        text_color=ECOPA_TEXT, width=160, anchor="w"
                    ).grid(row=0, column=col, padx=12, pady=6, sticky="w")

    def _tabela_destinacoes(self, parent, dest):
        card = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            card, text="Resumo de Destinações",
            font=font(15, "bold"),
            text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 8))

        dados = dest

        cabecalhos = ["Destinação", "Tipo", "Total Pedidos", "Total Kg"]
        header_frame = ctk.CTkFrame(card, fg_color=ECOPA_GREEN, corner_radius=10)
        header_frame.pack(fill="x", padx=16, pady=(0, 4))

        for col, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=font_small_bold(12),
                text_color=ECOPA_WHITE, width=180
            ).grid(row=0, column=col, padx=12, pady=8, sticky="w")

        if not dados:
            ctk.CTkLabel(
                card, text="Nenhuma destinação registrada",
                font=font_small(12), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=20)
            return

        for i, d in enumerate(dados):
            bg = ECOPA_BG if i % 2 == 0 else ECOPA_WHITE
            row = ctk.CTkFrame(card, fg_color=bg, corner_radius=0)
            row.pack(fill="x", padx=16)

            qtd_str = f"{float(d['total_kg'] or 0):.1f} Kg"
            valores = [d["destinacao"], d["tipo"], str(d["total_pedidos"] or 0), qtd_str]

            for col, val in enumerate(valores):
                ctk.CTkLabel(
                    row, text=val, font=font_small(12),
                    text_color=ECOPA_TEXT, width=180, anchor="w"
                ).grid(row=0, column=col, padx=12, pady=6, sticky="w")

    def _gerar_pdf(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Salvar Relatório",
            initialfile=f"relatorio_ecopa_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )
        if not caminho:
            return

        coletas = list(self._dados_coletas)
        data_inicio = self._filtro_data_inicio
        data_fim = self._filtro_data_fim

        fila = queue.Queue()

        def _tarefa():
            figs_criadas = []
            try:
                destino = Relatorio.resumo_destinacoes(
                    data_inicio=data_inicio, data_fim=data_fim)
                with PdfPages(caminho) as pdf:
                    # Pagina 1: Titulo e KPIs
                    fig1, ax1 = plt.subplots(figsize=(8.27, 11.69))
                    figs_criadas.append(fig1)
                    fig1.patch.set_facecolor(ECOPA_WHITE)
                    ax1.axis("off")

                    ax1.text(0.5, 0.92, "Relatório ECOPA", fontsize=28, fontweight="bold",
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

                    # Pagina 2: Grafico de status (pizza)
                    if coletas:
                        fig2, ax2 = plt.subplots(figsize=(8.27, 5))
                        figs_criadas.append(fig2)
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

                    # Pagina 3: Grafico por ponto (barras)
                    ponto_qtd = defaultdict(float)
                    for c in coletas:
                        ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
                    if ponto_qtd:
                        fig3, ax3 = plt.subplots(figsize=(8.27, 5))
                        figs_criadas.append(fig3)
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

                fila.put(("ok", caminho))
            except Exception as e:
                fila.put(("erro", str(e)))
            finally:
                for fig in figs_criadas:
                    try:
                        plt.close(fig)
                    except Exception:
                        pass

        def _poll():
            try:
                if not self.winfo_exists():
                    return
                status, payload = fila.get_nowait()
            except queue.Empty:
                try:
                    self.after(100, _poll)
                except Exception:
                    pass
                return
            except Exception:
                return
            if status == "ok":
                messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{payload}")
            else:
                messagebox.showerror("Erro", f"Falha ao gerar PDF:\n{payload}")

        self.after(100, _poll)
        threading.Thread(target=_tarefa, daemon=True).start()
