import logging
import locale

logger = logging.getLogger(__name__)

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
import customtkinter as ctk
import threading
from views.cadastros_hub import CadastrosHub
from views.coletas import ColetasView
from views.pontos import PontosView
from views.destinacoes import DestinacoesView
from views.loading import LoadingOverlay
from views.componentes_dashboard import KPICard, GraficoPizza, GraficoBarras, GraficoLinha, CardMetricas
from controllers.coleta_controller import ColetaController
from controllers.ponto_controller import PontoController
from datetime import datetime, timedelta
from collections import Counter, defaultdict

from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG as ECOPA_GREEN_BG,
    ECOPA_LEAF, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER,
    ECOPA_ORANGE, ECOPA_BLUE, ECOPA_RED,
    ECOPA_SIDEBAR_BG, ECOPA_SIDEBAR_ACTIVE,
    font, font_small, font_small_bold,
)




class MainView(ctk.CTkFrame):
    def __init__(self, master, nome_usuario=""):
        super().__init__(master)
        self.nome_usuario = nome_usuario
        self._navegacao_id = 0
        self.configure(fg_color=ECOPA_GREEN_BG)

        # === SIDEBAR ===
        self.sidebar = ctk.CTkFrame(
            self, width=260, corner_radius=0,
            fg_color=ECOPA_SIDEBAR_BG,
            border_width=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Botao Sair (fixo na parte inferior)
        sair_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=44)
        sair_frame.pack(side="bottom", fill="x", padx=12, pady=8)
        sair_frame.pack_propagate(False)

        sair_emoji = ctk.CTkLabel(
            sair_frame, text="❌",
            font=font(18), text_color=ECOPA_RED,
            width=32
        )
        sair_emoji.pack(side="left", padx=(12, 4))

        ctk.CTkButton(
            sair_frame, text="Sair",
            fg_color="transparent", hover_color="#fde8e8",
            anchor="w", height=40,
            font=font(14),
            text_color=ECOPA_RED,
            command=self.sair
        ).pack(side="left", fill="both", expand=True)

        # Menu scrollavel (vertical)
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self.sidebar, fg_color=ECOPA_SIDEBAR_BG,
            scrollbar_button_color=ECOPA_BORDER,
            scrollbar_button_hover_color=ECOPA_GREEN_LIGHT,
        )
        self.sidebar_scroll.pack(side="top", fill="both", expand=True)

        # Logo ECOPA
        logo_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        logo_frame.pack(fill="x", padx=24, pady=(28, 0))

        leaf_icon = ctk.CTkLabel(
            logo_frame, text="🌿",
            font=font(30), text_color=ECOPA_GREEN
        )
        leaf_icon.pack(side="left", padx=(0, 8))

        ecopa_label = ctk.CTkLabel(
            logo_frame, text="ECOPA",
            font=font(24, "bold"),
            text_color=ECOPA_GREEN_DARK
        )
        ecopa_label.pack(side="left")

        # Linha separadora
        ctk.CTkFrame(self.sidebar_scroll, fg_color=ECOPA_BORDER, height=1).pack(
            fill="x", padx=24, pady=(16, 8)
        )

        # Menu items
        self._botoes_menu = {}
        botoes = [
            ("dashboard",    "Dashboard",    self.abrir_dashboard,    "📊"),
            ("lotes",        "Estoque",      self.abrir_lotes,       "📦"),
            ("pedidos",      "Pedidos",      self.abrir_pedidos,     "📑"),
            ("cadastros",    "Cadastros",    self.abrir_cadastros,   "📋"),
            ("gerente",      "Gerente",      self.abrir_gerente,     "👤"),
            ("coletas",      "Coletas",      self.abrir_coleta,      "🚛"),
            ("pontos",       "Pontos",       self.abrir_pontos,      "📍"),
            ("destinacoes",  "Destinações",  self.abrir_destinacoes,  "♻️"),
            ("relatorios",   "Relatórios",   self.abrir_relatorios,  "📈"),
            ("auditoria", "Auditoria", self.abrir_auditoria, "📝"),
        ]

        for nome_icone, texto, comando, emoji in botoes:
            btn_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent", height=44)
            btn_frame.pack(fill="x", padx=12, pady=2)
            btn_frame.pack_propagate(False)

            emoji_lbl = ctk.CTkLabel(
                btn_frame, text=emoji,
                font=font(18), text_color=ECOPA_GREEN,
                width=32
            )
            emoji_lbl.pack(side="left", padx=(12, 4))

            btn = ctk.CTkButton(
                btn_frame, text=texto,
                fg_color="transparent", hover_color=ECOPA_SIDEBAR_ACTIVE,
                anchor="w", height=40,
                font=font(14),
                text_color=ECOPA_TEXT,
                command=comando
            )
            btn.pack(side="left", fill="both", expand=True)
            self._botoes_menu[nome_icone] = (btn_frame, btn)

        # === AREA PRINCIPAL ===
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=ECOPA_GREEN_BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.abrir_dashboard()

        # Detectar mudanca de estado da janela (maximizada/restaurada)
        self.after(100, self._configurar_listener_estado_janela)

    def _configurar_listener_estado_janela(self):
        root = self.winfo_toplevel()
        root.bind("<Configure>", self._ao_mudar_tamanho_janela)
        self._atualizar_scrollbar_sidebar()

    def _ao_mudar_tamanho_janela(self, event):
        if event.widget is self.winfo_toplevel():
            self._atualizar_scrollbar_sidebar()

    def _atualizar_scrollbar_sidebar(self):
        root = self.winfo_toplevel()
        try:
            state = root.state()
        except Exception:
            return
        if state == "iconic":
            return

        # Garante que o menu volta ao topo e nao cria espaco em branco acima
        try:
            self.sidebar_scroll._parent_canvas.yview_moveto(0)
        except Exception:
            pass

        maximizada = (state == "zoomed")

        if maximizada:
            self.sidebar_scroll._scrollbar.configure(
                button_color=ECOPA_SIDEBAR_BG,
                button_hover_color=ECOPA_SIDEBAR_BG
            )
        else:
            self.sidebar_scroll._scrollbar.configure(
                button_color=ECOPA_BORDER,
                button_hover_color=ECOPA_GREEN_LIGHT
            )

    def _destacar_menu(self, ativo):
        self._navegacao_id += 1
        for nome, (frame, btn) in self._botoes_menu.items():
            if nome == ativo:
                frame.configure(fg_color=ECOPA_SIDEBAR_ACTIVE)
                btn.configure(text_color=ECOPA_GREEN, font=font(14, "bold"))
            else:
                frame.configure(fg_color="transparent")
                btn.configure(text_color=ECOPA_TEXT, font=font(14))

    def _criar_container_scrollavel(self):
        """Cria um container scrollavel horizontal para as telas de conteudo."""
        scroll = ctk.CTkScrollableFrame(
            self.content, fg_color=ECOPA_GREEN_BG,
            scrollbar_button_color=ECOPA_BORDER,
            scrollbar_button_hover_color=ECOPA_GREEN_LIGHT,
        )
        scroll.pack(fill="both", expand=True)
        return scroll

    # ============================================================
    # DASHBOARD
    # ============================================================
    def abrir_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("dashboard")
        navegacao_id = self._navegacao_id

        overlay = LoadingOverlay(self.content, text="Carregando dashboard...")
        overlay.start()

        def _carregar():
            try:
                from models.coleta import Coleta
                from models.lote import Lote
                from controllers.pedido_controller import PedidoController

                coletas = ColetaController.listar()

                resumo_c = Coleta.resumo_dashboard()
                resumo_l = Lote.resumo_estoque_dashboard()
                pedidos = PedidoController.listar()
                pontos = PontoController.listar()

                grafico_data = self._preparar_graficos(coletas)

                self.after(0, lambda: _montar(resumo_c, resumo_l, pedidos, coletas, pontos, grafico_data))
            except Exception as e:
                logger.error("Erro ao carregar dashboard: %s", e)
                self.after(0, lambda: _erro())

        def _montar(resumo_c, resumo_l, pedidos, coletas, pontos, grafico_data):
            if navegacao_id != self._navegacao_id:
                return
            overlay.stop()
            self._montar_dashboard(resumo_c, resumo_l, pedidos, coletas, pontos, grafico_data)

        def _erro():
            if navegacao_id != self._navegacao_id:
                return
            overlay.stop()
            self._mostrar_erro_dashboard()

        threading.Thread(target=_carregar, daemon=True).start()

    def _mostrar_erro_dashboard(self):
        if hasattr(self, '_loading_label'):
            self._loading_label.destroy()
        ctk.CTkLabel(
            self.content, text="Erro ao carregar dashboard. Tente novamente.",
            font=font(14), text_color=ECOPA_RED
        ).pack(expand=True)

    def _preparar_graficos(self, coletas):
        """Prepara dados dos graficos em background (CPU intensivo)."""
        status_count = Counter(c["status"] for c in coletas)

        ponto_qtd = defaultdict(float)
        for c in coletas:
            ponto_qtd[c["ponto"]] += float(c["quantidade"] or 0)
        top_pontos = sorted(ponto_qtd.items(), key=lambda x: x[1], reverse=True)[:5]

        hoje = datetime.now().date()
        dias = [(hoje - timedelta(days=i)) for i in range(6, -1, -1)]
        qtd_por_dia = defaultdict(int)
        for c in coletas:
            if c["data_coleta"]:
                dia = c["data_coleta"].date()
                if (hoje - dia).days <= 6:
                    qtd_por_dia[dia] += 1
        valores_dias = [qtd_por_dia.get(d, 0) for d in dias]
        dias_str = [d.strftime("%d/%m") for d in dias]

        return {
            "status_count": status_count,
            "top_pontos": top_pontos,
            "dias_str": dias_str,
            "valores_dias": valores_dias,
        }

    def _montar_dashboard(self, resumo_c, resumo_l, pedidos, coletas, pontos, grafico_data):
        if hasattr(self, '_loading_label'):
            self._loading_label.destroy()

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
            font=font(26, "bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_header,
            text="Supervisor de resíduos e coletas",
            font=font_small(12), anchor="w",
            text_color=ECOPA_TEXT_LIGHT
        ).pack(anchor="w", pady=(2, 0))

        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.pack(side="right", anchor="ne")

        ctk.CTkLabel(
            right_header,
            text=datetime.now().strftime("%d de %B de %Y"),
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT
        ).pack(anchor="e")

        ctk.CTkLabel(
            right_header,
            text=datetime.now().strftime("%A"),
            font=font_small(11), text_color=ECOPA_TEXT_LIGHT
        ).pack(anchor="e")

        # Botao atualizar
        ctk.CTkButton(
            right_header, text="Atualizar", width=100, height=32,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=8, font=font_small_bold(12),
            command=self.abrir_dashboard
        ).pack(anchor="e", pady=(6, 0))

        # Linha verde
        ctk.CTkFrame(scroll, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # === DADOS ===
        total_coletas = resumo_c["total_coletas"]
        quantidade_total = float(resumo_c["quantidade_total"] or 0)
        pendentes = resumo_c["pendentes"] or 0
        realizadas = resumo_c["realizadas"] or 0

        estoque_total = float(resumo_l["estoque_total"] or 0)

        total_pedidos = len(pedidos)
        total_pontos = len(pontos)

        # === KPI CARDS ===
        frame_cards = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_cards.pack(fill="x", padx=32, pady=(20, 0))
        frame_cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cards_data = [
            ("🚛", "COLETAS",       str(total_coletas),    ECOPA_GREEN, "#e8f5e8"),
            ("📦", "ESTOQUE (Kg)",  f"{estoque_total:.0f}", ECOPA_BLUE,  "#e8f0f8"),
            ("📑", "PEDIDOS",       str(total_pedidos),    ECOPA_ORANGE, "#fdf5e8"),
            ("✅", "REALIZADAS",    str(realizadas),       ECOPA_LEAF,   "#e8f8e8"),
        ]

        for i, (emoji, titulo, valor, cor, bg_cor) in enumerate(cards_data):
            card = KPICard(frame_cards, emoji, titulo, valor, cor, bg_cor)
            card.grid(row=0, column=i, padx=6, pady=5, sticky="ew")

        # === GRAFICOS ===
        graficos_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        graficos_frame.pack(fill="x", padx=32, pady=(20, 0))
        graficos_frame.grid_columnconfigure((0, 1), weight=1)

        card_pizza = GraficoPizza(graficos_frame, "Resumo de Coletas", grafico_data["status_count"])
        card_pizza.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")

        card_barras = GraficoBarras(graficos_frame, "Top 5 Pontos (Kg)", grafico_data["top_pontos"])
        card_barras.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

        # === SEGUNDA ROW GRAFICOS ===
        graficos2_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        graficos2_frame.pack(fill="x", padx=32, pady=(10, 0))
        graficos2_frame.grid_columnconfigure((0, 1), weight=1)

        card_linha = GraficoLinha(
            graficos2_frame, "Coletas por Dia (últimos 7)",
            grafico_data["dias_str"], grafico_data["valores_dias"]
        )
        card_linha.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")

        metricas = [
            ("Total Coletado", f"{quantidade_total:.1f} Kg", ECOPA_GREEN),
            ("Pontos Cadastrados", str(total_pontos), ECOPA_BLUE),
            ("Coletas Pendentes", str(pendentes), ECOPA_ORANGE),
            ("Coletas Realizadas", str(realizadas), ECOPA_LEAF),
        ]
        card_info = CardMetricas(graficos2_frame, "Resumo do Dia", metricas)
        card_info.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")

        # Rodape
        ctk.CTkLabel(
            scroll, text=f"© {datetime.now().year} ECOPA System — Todos os direitos reservados",
            font=font_small(10), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(30, 15))

    # ============================================================
    # NAVEGACAO
    # ============================================================
    def _navegar_com_loading(self, nome_menu, funcao_carregar):
        """Navega para uma tela com loading visual."""
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu(nome_menu)

        overlay = LoadingOverlay(self.content, text=f"Carregando {nome_menu}...")
        overlay.start()

        def _tarefa():
            try:
                funcao_carregar()
            except Exception as e:
                logger.error("Erro ao carregar %s: %s", nome_menu, e)
            finally:
                self.after(0, lambda: overlay.stop())

        threading.Thread(target=_tarefa, daemon=True).start()

    def abrir_gerente(self):
        def _carregar():
            pass
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("gerente")
        scroll = self._criar_container_scrollavel()
        from views.gerente import ListaGerentes
        ListaGerentes(self, scroll, on_voltar=self.abrir_dashboard)

    def abrir_coleta(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("coletas")
        scroll = self._criar_container_scrollavel()
        ColetasView(self, scroll)

    def abrir_pontos(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("pontos")
        scroll = self._criar_container_scrollavel()
        PontosView(self, scroll)

    def abrir_destinacoes(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("destinacoes")
        scroll = self._criar_container_scrollavel()
        DestinacoesView(self, scroll)

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

    def abrir_auditoria(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("auditoria")
        scroll = self._criar_container_scrollavel()
        from views.auditoria import AuditoriaView
        AuditoriaView(self, scroll)

    def abrir_lotes(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("lotes")
        scroll = self._criar_container_scrollavel()
        from views.lotes import LotesView
        LotesView(self, scroll)

    def abrir_pedidos(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self._destacar_menu("pedidos")
        scroll = self._criar_container_scrollavel()
        from views.pedidos import PedidosView
        PedidosView(self, scroll)

    def sair(self):
        from utils.sessao import encerrar
        encerrar()
        self.winfo_toplevel().destroy()
