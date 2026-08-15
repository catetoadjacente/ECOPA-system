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

                total = len(coletas)
                qtd_total = sum(float(c["quantidade"] or 0) for c in coletas)
                pendentes = sum(1 for c in coletas if c["status"] == "Pendente")
                realizadas = sum(1 for c in coletas if c["status"] == "Realizada")
                total_dest = len(destino)
                total_kg_dest = sum(float(d["total_kg"] or 0) for d in destino)

                periodo_texto = "Periodo: Todos os registros"
                if data_inicio and data_fim:
                    di = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
                    df = data_fim.split(" ")[0]
                    df = datetime.strptime(df, "%Y-%m-%d").strftime("%d/%m/%Y")
                    periodo_texto = f"Periodo: {di} a {df}"
                elif data_inicio:
                    di = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
                    periodo_texto = f"Periodo: {di} ate a presente data"
                elif data_fim:
                    df = data_fim.split(" ")[0]
                    df = datetime.strptime(df, "%Y-%m-%d").strftime("%d/%m/%Y")
                    periodo_texto = f"Periodo: Ate {df}"

                def _desenhar_rodape(fig, num_pag, total_pag):
                    fig.text(0.5, 0.02, f"ECOPA  |  Relatorio de Coletas  |  Pagina {num_pag}/{total_pag}",
                             ha="center", fontsize=8, color=ECOPA_TEXT_LIGHT, style="italic")
                    fig.text(0.05, 0.02, f"Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
                             fontsize=7, color=ECOPA_TEXT_LIGHT)
                    fig.text(0.95, 0.02, "sistema-ecopa.com.br", ha="right",
                             fontsize=7, color=ECOPA_TEXT_LIGHT)

                def _desenhar_header(fig, titulo):
                    ax_h = fig.add_axes([0, 0.92, 1, 0.08])
                    ax_h.set_xlim(0, 1)
                    ax_h.set_ylim(0, 1)
                    ax_h.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax_h.transAxes,
                                                  facecolor=ECOPA_GREEN, edgecolor="none"))
                    ax_h.text(0.05, 0.55, "ECOPA", fontsize=22, fontweight="bold",
                              color=ECOPA_WHITE, va="center", transform=ax_h.transAxes)
                    ax_h.text(0.95, 0.55, titulo, fontsize=11, color=ECOPA_WHITE,
                              va="center", ha="right", transform=ax_h.transAxes)
                    ax_h.axis("off")

                dados_tabela_ponto = self._agregar_dados_ponto(coletas)

                total_paginas = 1
                if coletas:
                    total_paginas += 3
                if dados_tabela_ponto:
                    total_paginas += 1
                if destino:
                    total_paginas += 1

                with PdfPages(caminho) as pdf:
                    # === PAGINA 1: CAPA COM KPIs ===
                    fig1 = plt.figure(figsize=(8.27, 11.69))
                    figs_criadas.append(fig1)
                    fig1.patch.set_facecolor(ECOPA_WHITE)
                    ax1 = fig1.add_axes([0, 0, 1, 1])
                    ax1.set_xlim(0, 1)
                    ax1.set_ylim(0, 1)
                    ax1.axis("off")

                    # Header verde
                    ax1.add_patch(plt.Rectangle((0, 0.88), 1, 0.12,
                                                facecolor=ECOPA_GREEN, edgecolor="none",
                                                transform=ax1.transAxes))
                    ax1.text(0.05, 0.95, "ECOPA", fontsize=32, fontweight="bold",
                             color=ECOPA_WHITE, va="center", transform=ax1.transAxes)
                    ax1.text(0.05, 0.90, "Sistema de Gestao de Coletas", fontsize=11,
                             color="#c8e6c9", va="center", transform=ax1.transAxes)
                    ax1.text(0.95, 0.95, "RELATORIO", fontsize=14, fontweight="bold",
                             color=ECOPA_WHITE, va="center", ha="right", transform=ax1.transAxes)

                    # Titulo do relatorio
                    ax1.text(0.5, 0.82, "Relatorio de Coletas e Destinacoes",
                             fontsize=20, fontweight="bold", color=ECOPA_GREEN_DARK,
                             ha="center", va="center", transform=ax1.transAxes)
                    ax1.text(0.5, 0.79, f"Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
                             fontsize=10, color=ECOPA_TEXT_LIGHT, ha="center",
                             va="center", transform=ax1.transAxes)
                    ax1.text(0.5, 0.765, periodo_texto,
                             fontsize=10, color=ECOPA_TEXT_LIGHT, ha="center",
                             va="center", transform=ax1.transAxes)

                    # Linha separadora
                    ax1.plot([0.05, 0.95], [0.74, 0.74], color=ECOPA_GREEN,
                             linewidth=1.5, transform=ax1.transAxes, clip_on=False)

                    # KPI Cards
                    kpi_data = [
                        ("COLETAS TOTAIS", str(total), ECOPA_GREEN),
                        ("TOTAL KG", f"{qtd_total:.1f}", ECOPA_BLUE),
                        ("PENDENTES", str(pendentes), ECOPA_ORANGE),
                        ("REALIZADAS", str(realizadas), ECOPA_LEAF),
                        ("DESTINACOES", str(total_dest), ECOPA_RED),
                    ]

                    card_w = 0.16
                    card_h = 0.14
                    start_x = 0.05
                    gap = 0.025

                    for i, (titulo, valor, cor) in enumerate(kpi_data):
                        x = start_x + i * (card_w + gap)
                        y = 0.56

                        # Fundo do card
                        ax1.add_patch(plt.Rectangle((x, y), card_w, card_h,
                                                     facecolor="#f8f9fa", edgecolor=ECOPA_BORDER,
                                                     linewidth=1, transform=ax1.transAxes,
                                                     zorder=1))
                        # Barra colorida no topo
                        ax1.add_patch(plt.Rectangle((x, y + card_h - 0.008), card_w, 0.008,
                                                     facecolor=cor, edgecolor="none",
                                                     transform=ax1.transAxes, zorder=2))
                        # Valor
                        ax1.text(x + card_w / 2, y + card_h / 2 + 0.015, valor,
                                 fontsize=18, fontweight="bold", color=ECOPA_GREEN_DARK,
                                 ha="center", va="center", transform=ax1.transAxes, zorder=3)
                        # Titulo
                        ax1.text(x + card_w / 2, y + 0.02, titulo,
                                 fontsize=7, fontweight="bold", color=ECOPA_TEXT_LIGHT,
                                 ha="center", va="center", transform=ax1.transAxes, zorder=3)

                    # Metricas adicionais
                    ax1.text(0.05, 0.48, "Metricas Complementares",
                             fontsize=13, fontweight="bold", color=ECOPA_GREEN_DARK,
                             transform=ax1.transAxes)
                    ax1.plot([0.05, 0.95], [0.465, 0.465], color=ECOPA_BORDER,
                             linewidth=0.5, transform=ax1.transAxes, clip_on=False)

                    metricas_y = 0.44
                    ax1.text(0.08, metricas_y, f"Total de Destinacoes Registradas:  {total_dest}",
                             fontsize=11, color=ECOPA_TEXT, transform=ax1.transAxes)
                    ax1.text(0.08, metricas_y - 0.035, f"Total de Kg Destinados:  {total_kg_dest:.1f} Kg",
                             fontsize=11, color=ECOPA_TEXT, transform=ax1.transAxes)
                    if total > 0:
                        taxa = (realizadas / total) * 100
                        ax1.text(0.08, metricas_y - 0.07, f"Taxa de Conclusao:  {taxa:.1f}%",
                                 fontsize=11, color=ECOPA_GREEN_DARK if taxa >= 50 else ECOPA_ORANGE,
                                 transform=ax1.transAxes)
                    ax1.text(0.08, metricas_y - 0.105, f"Media de Kg por Coleta:  {(qtd_total / total):.1f} Kg" if total > 0 else "Media de Kg por Coleta:  0 Kg",
                             fontsize=11, color=ECOPA_TEXT, transform=ax1.transAxes)

                    # Rodape pagina 1
                    _desenhar_rodape(fig1, 1, total_paginas)
                    pdf.savefig(fig1)

                    if coletas:
                        # === PAGINA 2: GRAFICO DE PIZZA ===
                        fig2 = plt.figure(figsize=(8.27, 11.69))
                        figs_criadas.append(fig2)
                        fig2.patch.set_facecolor(ECOPA_WHITE)
                        _desenhar_header(fig2, "Distribuicao por Status")

                        ax2 = fig2.add_axes([0.1, 0.15, 0.8, 0.72])
                        ax2.set_facecolor(ECOPA_WHITE)

                        status_count = Counter(c["status"] for c in coletas)
                        cores = {"Pendente": ECOPA_ORANGE, "Realizada": ECOPA_LEAF}
                        labels = list(status_count.keys())
                        sizes = list(status_count.values())
                        colors = [cores.get(l, "#999") for l in labels]

                        wedges, texts, autotexts = ax2.pie(
                            sizes, labels=None, autopct=lambda p: f'{p:.1f}%\n({int(round(p*sum(sizes)/100))})',
                            colors=colors, startangle=90, pctdistance=0.75,
                            wedgeprops={"linewidth": 2, "edgecolor": ECOPA_WHITE, "width": 0.5},
                            textprops={"fontsize": 10}
                        )
                        for autotext in autotexts:
                            autotext.set_fontsize(9)
                            autotext.set_fontweight("bold")

                        # Legenda
                        legend_labels = [f"{l}  ({v})" for l, v in zip(labels, sizes)]
                        ax2.legend(wedges, legend_labels, loc="center left",
                                   bbox_to_anchor=(0.85, 0.5), fontsize=11,
                                   frameon=False)

                        ax2.set_title("Coletas por Status", fontsize=16, fontweight="bold",
                                       color=ECOPA_GREEN_DARK, pad=20)

                        # KPI boxes no rodape do grafico
                        kpi_y = 0.08
                        kpi_box_w = 0.18
                        for i, (titulo, valor, cor) in enumerate([
                            ("Total", str(total), ECOPA_GREEN),
                            ("Pendentes", str(pendentes), ECOPA_ORANGE),
                            ("Realizadas", str(realizadas), ECOPA_LEAF),
                        ]):
                            x = 0.15 + i * (kpi_box_w + 0.05)
                            fig2.text(x + kpi_box_w / 2, kpi_y + 0.02, valor,
                                      fontsize=16, fontweight="bold", color=cor,
                                      ha="center", va="center")
                            fig2.text(x + kpi_box_w / 2, kpi_y - 0.015, titulo,
                                      fontsize=8, color=ECOPA_TEXT_LIGHT, ha="center")

                        _desenhar_rodape(fig2, 2, total_paginas)
                        pdf.savefig(fig2)

                        # === PAGINA 3: BARRAS POR PONTO ===
                        fig3 = plt.figure(figsize=(8.27, 11.69))
                        figs_criadas.append(fig3)
                        fig3.patch.set_facecolor(ECOPA_WHITE)
                        _desenhar_header(fig3, "Coletas por Ponto de Coleta")

                        ax3 = fig3.add_axes([0.12, 0.15, 0.82, 0.72])
                        ax3.set_facecolor(ECOPA_WHITE)

                        ponto_qtd = defaultdict(float)
                        for c in coletas:
                            ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
                        top = sorted(ponto_qtd.items(), key=lambda x: x[1], reverse=True)[:10]

                        if top:
                            nomes, qtds = zip(*top)
                            cores_barras = [ECOPA_GREEN if i < 3 else ECOPA_GREEN_LIGHT
                                            for i in range(len(nomes))]
                            bars = ax3.barh(list(nomes), list(qtds), color=cores_barras,
                                            height=0.6, edgecolor=ECOPA_WHITE, linewidth=0.5)
                            ax3.invert_yaxis()
                            ax3.set_xlabel("Quantidade (Kg)", fontsize=10, color=ECOPA_TEXT_LIGHT)

                            # Valores nas barras
                            for bar, val in zip(bars, qtds):
                                ax3.text(bar.get_width() + max(qtds) * 0.01, bar.get_y() + bar.get_height() / 2,
                                         f"{val:.1f} Kg", va="center", fontsize=9, color=ECOPA_TEXT)

                            ax3.spines["top"].set_visible(False)
                            ax3.spines["right"].set_visible(False)
                            ax3.spines["bottom"].set_color(ECOPA_BORDER)
                            ax3.spines["left"].set_color(ECOPA_BORDER)
                            ax3.tick_params(axis="y", labelsize=10)
                            ax3.tick_params(axis="x", labelsize=9)
                            ax3.grid(axis="x", alpha=0.2, color=ECOPA_BORDER)

                        ax3.set_title("Top 10 Pontos por Quantidade Coletada",
                                       fontsize=14, fontweight="bold", color=ECOPA_GREEN_DARK, pad=15)

                        _desenhar_rodape(fig3, 3, total_paginas)
                        pdf.savefig(fig3)

                        # === PAGINA 4: GRAFICO DE LINHA ===
                        fig4 = plt.figure(figsize=(8.27, 11.69))
                        figs_criadas.append(fig4)
                        fig4.patch.set_facecolor(ECOPA_WHITE)
                        _desenhar_header(fig4, "Evolucao Diaria")

                        ax4 = fig4.add_axes([0.1, 0.15, 0.82, 0.72])
                        ax4.set_facecolor(ECOPA_WHITE)

                        hoje = datetime.now().date()
                        dias = [(hoje - timedelta(days=i)) for i in range(6, -1, -1)]
                        qtd_por_dia = defaultdict(int)
                        kg_por_dia = defaultdict(float)
                        for c in coletas:
                            if c["data_coleta"]:
                                dia = c["data_coleta"].date()
                                if (hoje - dia).days <= 6:
                                    qtd_por_dia[dia] += 1
                                    kg_por_dia[dia] += float(c["quantidade"] or 0)
                        valores_qtd = [qtd_por_dia.get(d, 0) for d in dias]
                        valores_kg = [kg_por_dia.get(d, 0) for d in dias]
                        dias_str = [d.strftime("%d/%m") for d in dias]

                        # Eixo duplo
                        ax4_twin = ax4.twinx()

                        l1, = ax4.plot(dias_str, valores_qtd, marker="o", color=ECOPA_GREEN,
                                       linewidth=2.5, markersize=8, markerfacecolor=ECOPA_WHITE,
                                       markeredgecolor=ECOPA_GREEN, markeredgewidth=2, label="Coletas")
                        ax4.fill_between(range(len(dias_str)), valores_qtd, alpha=0.1, color=ECOPA_GREEN)
                        ax4.set_ylabel("Numero de Coletas", fontsize=10, color=ECOPA_GREEN)

                        l2, = ax4_twin.plot(dias_str, valores_kg, marker="s", color=ECOPA_BLUE,
                                            linewidth=2, markersize=7, markerfacecolor=ECOPA_WHITE,
                                            markeredgecolor=ECOPA_BLUE, markeredgewidth=2,
                                            linestyle="--", label="Kg Total")
                        ax4_twin.set_ylabel("Quantidade (Kg)", fontsize=10, color=ECOPA_BLUE)

                        ax4.set_ylim(0, max(valores_qtd) + 2 if max(valores_qtd) > 0 else 5)
                        max_kg = max(valores_kg) if valores_kg else 0
                        ax4_twin.set_ylim(0, max_kg * 1.2 if max_kg > 0 else 10)

                        ax4.spines["top"].set_visible(False)
                        ax4_twin.spines["top"].set_visible(False)
                        ax4.spines["bottom"].set_color(ECOPA_BORDER)
                        ax4.spines["left"].set_color(ECOPA_BORDER)
                        ax4_twin.spines["right"].set_color(ECOPA_BORDER)
                        ax4.tick_params(labelsize=9)
                        ax4_twin.tick_params(labelsize=9)
                        ax4.grid(axis="y", alpha=0.2, color=ECOPA_BORDER)

                        lines = [l1, l2]
                        labels_leg = [l.get_label() for l in lines]
                        ax4.legend(lines, labels_leg, loc="upper left", frameon=True,
                                   facecolor=ECOPA_WHITE, edgecolor=ECOPA_BORDER, fontsize=9)

                        ax4.set_title("Coletas nos Ultimos 7 Dias",
                                       fontsize=14, fontweight="bold", color=ECOPA_GREEN_DARK, pad=15)

                        _desenhar_rodape(fig4, 4, total_paginas)
                        pdf.savefig(fig4)

                    # === TABELA: COLETAS POR PONTO ===
                    if dados_tabela_ponto:
                        fig_tab1 = plt.figure(figsize=(8.27, 11.69))
                        figs_criadas.append(fig_tab1)
                        fig_tab1.patch.set_facecolor(ECOPA_WHITE)
                        _desenhar_header(fig_tab1, "Tabela - Coletas por Ponto")

                        ax_tab1 = fig_tab1.add_axes([0.05, 0.12, 0.9, 0.78])
                        ax_tab1.axis("off")
                        ax_tab1.set_title("")

                        colunas = ["Ponto de Coleta", "Total Coletas", "Total Kg", "Pendentes", "Realizadas"]
                        cell_text = []
                        cell_colors = []
                        for d in dados_tabela_ponto:
                            row = [
                                d["ponto"],
                                str(d["total_coletas"]),
                                f"{d['total_kg']:.1f} Kg",
                                str(d["pendentes"]),
                                str(d["realizadas"]),
                            ]
                            cell_text.append(row)
                            cell_colors.append([
                                ECOPA_WHITE,
                                ECOPA_WHITE,
                                ECOPA_WHITE,
                                "#fff3e0" if d["pendentes"] > 0 else ECOPA_WHITE,
                                "#e8f5e9" if d["realizadas"] > 0 else ECOPA_WHITE,
                            ])

                        if cell_text:
                            table = ax_tab1.table(
                                cellText=cell_text, colLabels=colunas,
                                cellColours=cell_colors,
                                colColours=[ECOPA_GREEN] * len(colunas),
                                loc="upper center", cellLoc="center",
                                colWidths=[0.30, 0.15, 0.15, 0.15, 0.15]
                            )
                            table.auto_set_font_size(False)
                            table.set_fontsize(10)
                            table.scale(1, 1.8)

                            for (row, col), cell in table.get_celld().items():
                                cell.set_edgecolor(ECOPA_BORDER)
                                if row == 0:
                                    cell.set_text_props(color=ECOPA_WHITE, fontweight="bold")
                                    cell.set_height(0.08)
                                else:
                                    cell.set_height(0.06)

                        num_tab_pag = total_paginas - (1 if destino else 0) + (1 if dados_tabela_ponto else 0)
                        _desenhar_rodape(fig_tab1, num_tab_pag, total_paginas)
                        pdf.savefig(fig_tab1)

                    # === TABELA: DESTINACOES ===
                    if destino:
                        fig_tab2 = plt.figure(figsize=(8.27, 11.69))
                        figs_criadas.append(fig_tab2)
                        fig_tab2.patch.set_facecolor(ECOPA_WHITE)
                        _desenhar_header(fig_tab2, "Tabela - Destinacoes")

                        ax_tab2 = fig_tab2.add_axes([0.05, 0.12, 0.9, 0.78])
                        ax_tab2.axis("off")

                        colunas_dest = ["Destinacao", "Tipo", "Total Pedidos", "Total Kg"]
                        cell_text_dest = []
                        cell_colors_dest = []
                        for d in destino:
                            row = [
                                d["destinacao"],
                                d["tipo"],
                                str(d["total_pedidos"]),
                                f"{float(d['total_kg'] or 0):.1f} Kg",
                            ]
                            cell_text_dest.append(row)
                            cell_colors_dest.append([ECOPA_WHITE] * 4)

                        if cell_text_dest:
                            table2 = ax_tab2.table(
                                cellText=cell_text_dest, colLabels=colunas_dest,
                                cellColours=cell_colors_dest,
                                colColours=[ECOPA_GREEN] * len(colunas_dest),
                                loc="upper center", cellLoc="center",
                                colWidths=[0.30, 0.20, 0.20, 0.20]
                            )
                            table2.auto_set_font_size(False)
                            table2.set_fontsize(10)
                            table2.scale(1, 1.8)

                            for (row, col), cell in table2.get_celld().items():
                                cell.set_edgecolor(ECOPA_BORDER)
                                if row == 0:
                                    cell.set_text_props(color=ECOPA_WHITE, fontweight="bold")
                                    cell.set_height(0.08)
                                else:
                                    cell.set_height(0.06)

                        _desenhar_rodape(fig_tab2, total_paginas, total_paginas)
                        pdf.savefig(fig_tab2)

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

    def _agregar_dados_ponto(self, coletas):
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
        return sorted(agg.values(), key=lambda d: d["total_coletas"], reverse=True)
