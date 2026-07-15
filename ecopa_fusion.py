import customtkinter as ctk
import pywinstyles
import tkinter as tk
import random
import time
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ============================================================
# PALETA VERDE FUTURISTA (ECOPA BIO-DIGITAL)
# ============================================================
BG_DARK        = "#031c12"
BG_PANEL       = "#062e1e"
NEON_GREEN     = "#00ff88"
CYAN_GREEN     = "#00e5ff"
TEXT_MAIN      = "#ecfdf5"
BORDER_COLOR   = "#0f4d36"
BG_CARD        = "#0a2a1a"
RED_ALERT      = "#441111"
RED_TEXT       = "#ffaaaa"
RED_BORDER     = "#aa4444"
YELLOW_STATUS  = "#ffcc00"

COORDS = [
    (-1.4558, -48.4902, "Belém"),
    (-1.3617, -48.3725, "Ananindeua"),
    (-1.3000, -48.3333, "Marituba"),
    (-1.2000, -48.3000, "Benevides"),
    (-1.4500, -48.4667, "Icoaraci"),
]

class EcopaFusionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECOPA - Sistema de Rastreamento Bio-Digital v2.0")
        self.geometry("1100x700")
        self.minsize(950, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.rastreamento_ativo = False
        self._after_id = None
        self._timer_id = None
        self._tempo_inicio = 0
        self.current_frame = None

        # --- pywinstyles ---
        try:
            pywinstyles.apply_style(self, "acrylic")
            pywinstyles.change_header_color(self, color=BG_DARK)
            pywinstyles.change_border_color(self, color=NEON_GREEN)
        except Exception:
            pass

        # --- Fundo degradê radial ---
        self.canvas_bg = tk.Canvas(self, highlightthickness=0)
        self.canvas_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._desenhar_degrade)

        # --- Layout principal ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self, width=240, corner_radius=20,
            fg_color=BG_PANEL, border_color=BORDER_COLOR, border_width=1
        )
        self.sidebar.grid(row=0, column=0, rowspan=4, padx=(20, 10), pady=20, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        self._criar_sidebar()

        # Área principal
        self.main_container = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        self.mostrar_acompanhamento()

    # ============================================================
    # DEGRADÊ RADIAL
    # ============================================================
    def _desenhar_degrade(self, event=None):
        self.canvas_bg.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
        steps = 60
        r1, g1, b1 = self.winfo_rgb(BG_DARK)
        r2, g2, b2 = self.winfo_rgb("#042618")
        cx, cy = w / 2, h / 2
        max_r = max(w, h) * 1.6
        for i in range(steps):
            t = i / steps
            nr = int(r1 + (r2 - r1) * t) >> 8
            ng = int(g1 + (g2 - g1) * t) >> 8
            nb = int(b1 + (b2 - b1) * t) >> 8
            cor = f"#{nr:02x}{ng:02x}{nb:02x}"
            raio = max_r * (1 - t * 0.85)
            self.canvas_bg.create_oval(
                cx - raio, cy - raio, cx + raio, cy + raio,
                fill=cor, outline=cor
            )

    # ============================================================
    # SIDEBAR
    # ============================================================
    def _criar_sidebar(self):
        ctk.CTkLabel(
            self.sidebar, text="ECOPA",
            font=("Segoe UI", 32, "bold"), text_color=NEON_GREEN
        ).grid(row=0, column=0, padx=20, pady=(30, 5))

        ctk.CTkLabel(
            self.sidebar, text="BIO-DIGITAL NAVEGAÇÃO",
            font=("Segoe UI", 10), text_color=TEXT_MAIN
        ).grid(row=1, column=0, padx=20, pady=(0, 30))

        estilo_btn = {
            "corner_radius": 10, "height": 45,
            "fg_color": "transparent", "text_color": TEXT_MAIN,
            "hover_color": BORDER_COLOR, "border_color": CYAN_GREEN,
            "border_width": 1, "font": ("Segoe UI Semibold", 13),
            "anchor": "w"
        }

        self._btn_nav = ctk.CTkButton(
            self.sidebar, text="🛸  Navegação Orbital",
            command=self.mostrar_navegacao, **estilo_btn
        )
        self._btn_nav.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        self._btn_acomp = ctk.CTkButton(
            self.sidebar, text="📡  Telemetria Real",
            command=self.mostrar_acompanhamento, **estilo_btn
        )
        self._btn_acomp.grid(row=3, column=0, padx=20, pady=8, sticky="ew")

        self._btn_busca = ctk.CTkButton(
            self.sidebar, text="🔍  Bio-Busca Coleta",
            command=self.mostrar_busca, **estilo_btn
        )
        self._btn_busca.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        ctk.CTkLabel(
            self.sidebar, text="v2.0.1 | Belém-PA Core",
            font=("Consolas", 9), text_color=BORDER_COLOR
        ).grid(row=7, column=0, pady=15)

    def _destacar_sidebar(self, ativo):
        for nome, btn in [("Navegação", self._btn_nav),
                          ("Acompanhamento", self._btn_acomp),
                          ("Busca", self._btn_busca)]:
            if nome == ativo:
                btn.configure(fg_color=BORDER_COLOR, text_color=NEON_GREEN)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_MAIN)

    # ============================================================
    # PAINEL DE CONTEÚDO
    # ============================================================
    def _limpar_main(self):
        if self.current_frame is not None:
            try:
                self.current_frame.destroy()
            except Exception:
                pass
            self.current_frame = None

    def _criar_painel(self, titulo, icone="📊"):
        self._limpar_main()
        frame = ctk.CTkFrame(
            self.main_container, corner_radius=20,
            fg_color=BG_PANEL, border_color=BORDER_COLOR, border_width=1
        )
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.current_frame = frame

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(25, 10))

        ctk.CTkLabel(
            header, text=f"{icone}  {titulo}",
            font=("Segoe UI", 22, "bold"), text_color=NEON_GREEN
        ).pack(side="left")

        sep = ctk.CTkFrame(frame, height=2, fg_color=CYAN_GREEN)
        sep.pack(fill="x", padx=25, pady=(0, 20))

        return frame

    # ============================================================
    # TELA: NAVEGAÇÃO
    # ============================================================
    def mostrar_navegacao(self):
        self._parar_rastreamento()
        self._destacar_sidebar("Navegação")
        pane = self._criar_painel("Módulo de Navegação Orbital", "🛸")

        content = ctk.CTkFrame(pane, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=25, pady=5)

        # Mapa canvas
        mapa_frame = ctk.CTkFrame(
            content, corner_radius=15,
            fg_color=BG_DARK, border_color=CYAN_GREEN, border_width=1
        )
        mapa_frame.pack(expand=True, fill="both")

        self._canvas_mapa = tk.Canvas(
            mapa_frame, highlightthickness=0, bd=0, bg=BG_DARK
        )
        self._canvas_mapa.pack(fill="both", expand=True, padx=2, pady=2)
        self._canvas_mapa.bind("<Configure>", self._render_mapa_navegacao)

        # Info cards
        info_row = ctk.CTkFrame(content, fg_color="transparent")
        info_row.pack(fill="x", pady=(15, 0))
        info_row.grid_columnconfigure((0, 1, 2), weight=1)

        for i, (ico, val, lbl) in enumerate([
            ("🚚", "12 Entregas", "Hoje"),
            ("⏱️", "45 min médio", "Tempo de rota"),
            ("✅", "98%", "Taxa de sucesso"),
        ]):
            card = ctk.CTkFrame(info_row, fg_color=BG_CARD, corner_radius=12)
            card.grid(row=0, column=i, sticky="ew", padx=5)
            ctk.CTkLabel(card, text=ico, font=("Segoe UI", 22)).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=val, font=("Segoe UI", 15, "bold"),
                         text_color=NEON_GREEN).pack()
            ctk.CTkLabel(card, text=lbl, font=("Segoe UI", 10),
                         text_color=TEXT_MAIN).pack(pady=(0, 8))

    def _render_mapa_navegacao(self, event=None):
        c = self._canvas_mapa
        c.delete("mapa")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 50 or h < 50:
            return

        margem = 50
        min_lat, max_lat = -1.48, -1.15
        min_lon, max_lon = -48.55, -48.25

        def to_screen(lat, lon):
            x = margem + (lon - min_lon) / (max_lon - min_lon) * (w - 2 * margem)
            y = h - margem - (lat - min_lat) / (max_lat - min_lat) * (h - 2 * margem)
            return x, y

        c.create_rectangle(0, 0, w, h, fill=BG_DARK, outline="", tags="mapa")

        # Grid
        for i in range(5):
            t = i / 4
            lat_ = min_lat + (max_lat - min_lat) * t
            lon_ = min_lon + (max_lon - min_lon) * t
            _, y = to_screen(lat_, min_lon)
            x, _ = to_screen(min_lat, lon_)
            c.create_line(margem, y, w - margem, y, fill=BORDER_COLOR, width=1, tags="mapa")
            c.create_text(margem - 5, y, text=f"{lat_:.2f}", anchor="e",
                          fill=TEXT_MAIN, font=("Consolas", 7), tags="mapa")
            c.create_line(x, margem, x, h - margem, fill=BORDER_COLOR, width=1, tags="mapa")
            c.create_text(x, h - margem + 12, text=f"{lon_:.2f}", anchor="n",
                          fill=TEXT_MAIN, font=("Consolas", 7), tags="mapa")

        # Conexões
        pts = [(lat, lon) for lat, lon, _ in COORDS]
        for i in range(len(pts) - 1):
            x1, y1 = to_screen(*pts[i])
            x2, y2 = to_screen(*pts[i + 1])
            c.create_line(x1, y1, x2, y2, fill=CYAN_GREEN, width=1.5,
                          dash=(4, 4), tags="mapa")

        # Cidades
        for lat, lon, nome in COORDS:
            x, y = to_screen(lat, lon)
            r = 6
            c.create_oval(x - r, y - r, x + r, y + r,
                          fill=NEON_GREEN, outline=CYAN_GREEN, width=1.5, tags="mapa")
            c.create_text(x, y - 14, text=nome, fill=TEXT_MAIN,
                          font=("Segoe UI", 9, "bold"), tags="mapa")

    # ============================================================
    # TELA: ACOMPANHAMENTO (TEMPO REAL)
    # ============================================================
    def mostrar_acompanhamento(self):
        self._parar_rastreamento()
        self._destacar_sidebar("Acompanhamento")
        pane = self._criar_painel("Telemetria de Coleta em Tempo Real", "📡")

        content = ctk.CTkFrame(pane, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=25, pady=5)

        # === HUD de Status ===
        self._status_hud = ctk.CTkFrame(
            content, corner_radius=15,
            fg_color=BG_DARK, border_color=BORDER_COLOR, border_width=1
        )
        self._status_hud.pack(fill="x", pady=(0, 20), ipady=15)
        self._status_hud.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self._status_hud, text="🛰️",
            font=("Segoe UI", 48), text_color=CYAN_GREEN
        ).grid(row=0, column=0, rowspan=4, padx=(25, 10))

        ctk.CTkLabel(
            self._status_hud, text="STATUS DO LINK:",
            font=("Consolas", 11), text_color=BORDER_COLOR, anchor="w"
        ).grid(row=0, column=1, sticky="w", pady=(10, 0))

        self._label_link = ctk.CTkLabel(
            self._status_hud, text="AGUARDANDO SINAL...",
            font=("Segoe UI", 16, "bold"), text_color=YELLOW_STATUS, anchor="w"
        )
        self._label_link.grid(row=1, column=1, sticky="w")

        ctk.CTkLabel(
            self._status_hud, text="COORDENADAS (LAT, LON):",
            font=("Consolas", 10), text_color=BORDER_COLOR, anchor="w"
        ).grid(row=2, column=1, sticky="w")

        self._label_coords = ctk.CTkLabel(
            self._status_hud, text="--.---- , --.----",
            font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN, anchor="w"
        )
        self._label_coords.grid(row=3, column=1, sticky="w", pady=(0, 5))

        self._label_cidade = ctk.CTkLabel(
            self._status_hud, text="Localização: ---",
            font=("Segoe UI", 12), text_color=TEXT_MAIN, anchor="w"
        )
        self._label_cidade.grid(row=0, column=2, sticky="w", padx=(20, 0))

        self._label_velocidade = ctk.CTkLabel(
            self._status_hud, text="Velocidade: -- km/h",
            font=("Segoe UI", 12), text_color=TEXT_MAIN, anchor="w"
        )
        self._label_velocidade.grid(row=1, column=2, sticky="w", padx=(20, 0))

        self._label_tempo = ctk.CTkLabel(
            self._status_hud, text="Tempo ativo: 00:00",
            font=("Consolas", 11), text_color=CYAN_GREEN, anchor="w"
        )
        self._label_tempo.grid(row=2, column=2, sticky="w", padx=(20, 0))

        # Mini-mapa
        self._mini_canvas = tk.Canvas(
            self._status_hud, height=90, highlightthickness=0, bd=0, bg=BG_DARK
        )
        self._mini_canvas.grid(row=4, column=0, columnspan=3, sticky="ew",
                               padx=15, pady=(5, 10))

        # === Botões ===
        botoes = ctk.CTkFrame(content, fg_color="transparent")
        botoes.pack(fill="x", pady=5)

        self._btn_start = ctk.CTkButton(
            botoes, text="▶  INICIAR RASTREAMENTO NEON",
            command=self.iniciar_rastreamento,
            fg_color=NEON_GREEN, text_color=BG_DARK,
            font=("Segoe UI", 13, "bold"), height=48, corner_radius=10
        )
        self._btn_start.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self._btn_stop = ctk.CTkButton(
            botoes, text="⏹  CESSAR TELEMETRIA",
            command=self._parar_rastreamento,
            fg_color=RED_ALERT, text_color=RED_TEXT,
            border_color=RED_BORDER, border_width=1,
            font=("Segoe UI", 13, "bold"), height=48, corner_radius=10
        )
        self._btn_stop.pack(side="left", expand=True, fill="x", padx=(10, 0))

        # === Tabela de registros ===
        tabela = ctk.CTkFrame(
            content, corner_radius=15,
            fg_color=BG_DARK, border_color=BORDER_COLOR, border_width=1
        )
        tabela.pack(expand=True, fill="both", pady=(20, 0))

        ctk.CTkLabel(
            tabela, text="📋  REGISTRO DE FLUXO DE BIO-MATÉRIA",
            font=("Consolas", 11), text_color=CYAN_GREEN
        ).pack(pady=(10, 5), padx=15, anchor="w")

        headers = ["ID Ciber", "Ponto de Coleta", "Bio-Motorista", "Quantidade", "Status"]
        cab = ctk.CTkFrame(tabela, fg_color=BG_PANEL, height=28)
        cab.pack(fill="x", padx=10)
        for i, h in enumerate(headers):
            ctk.CTkLabel(cab, text=h, font=("Segoe UI Semibold", 10),
                         text_color=TEXT_MAIN).place(relx=i / len(headers) + 0.02,
                                                     rely=0.5, anchor="w")

        dados = [
            ("#EC0125", "Ver-o-Peso", "João Ciber", "120 kg", "♻️ PROCESSADO"),
            ("#EC0124", "Nazaré Bio", "Maria Eco", "85 kg",  "♻️ PROCESSADO"),
            ("#EC0123", "Batista Campos", "Carlos Tech", "110 kg", "⚠️ ATRASADO"),
        ]
        for row_data in dados:
            linha = ctk.CTkFrame(tabela, fg_color="transparent", height=30)
            linha.pack(fill="x", padx=10, pady=1)
            for i, val in enumerate(row_data):
                cor = NEON_GREEN if "♻️" in val else (
                    RED_TEXT if "⚠️" in val else TEXT_MAIN)
                ctk.CTkLabel(linha, text=val, font=("Consolas", 9),
                             text_color=cor).place(relx=i / len(headers) + 0.02,
                                                   rely=0.5, anchor="w")

    # ============================================================
    # TELA: BUSCA DE COLETA
    # ============================================================
    def mostrar_busca(self):
        self._parar_rastreamento()
        self._destacar_sidebar("Busca")
        pane = self._criar_painel("Motor de Bio-Busca de Coleta", "🔍")

        content = ctk.CTkFrame(pane, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=25, pady=5)

        # Zona de busca
        busca = ctk.CTkFrame(
            content, corner_radius=15,
            fg_color=BG_DARK, border_color=BORDER_COLOR, border_width=1
        )
        busca.pack(fill="x", ipady=15)

        ctk.CTkLabel(
            busca, text="Digite a Geo-Localização para Bio-Escaneamento:",
            font=("Segoe UI", 13), text_color=TEXT_MAIN
        ).pack(pady=(15, 8))

        linha = ctk.CTkFrame(busca, fg_color="transparent")
        linha.pack(pady=5)

        self._entry_busca = ctk.CTkEntry(
            linha,
            placeholder_text="Ex: Av. Governador José Malcher, Belém",
            width=450, height=40,
            fg_color=BG_DARK, border_color=CYAN_GREEN,
            font=("Segoe UI", 12)
        )
        self._entry_busca.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            linha, text="🌀  Escanear",
            command=self._executar_busca,
            fg_color=CYAN_GREEN, text_color=BG_DARK,
            font=("Segoe UI", 12, "bold"), height=40, corner_radius=8
        ).pack(side="left")

        # Resultados
        self._resultados_frame = ctk.CTkFrame(content, fg_color="transparent")
        self._resultados_frame.pack(expand=True, fill="both", pady=(15, 0))
        self._resultados_frame.grid_columnconfigure(0, weight=1)

        self._mostrar_resultados()

    def _executar_busca(self):
        self._mostrar_resultados()

    def _mostrar_resultados(self):
        for w in self._resultados_frame.winfo_children():
            w.destroy()

        resultados = [
            ("🟢", "Ecoponto Belém Centro", "Av. Presidente Vargas, 500", "2.3 km"),
            ("🟢", "Coleta Ananindeua", "BR-316, Km 4", "5.1 km"),
            ("🟡", "Ponto Marituba", "Rua dos Maguary, 120", "8.7 km"),
            ("🔵", "Coleta Benevides", "Rod. BR-408, s/n", "15.2 km"),
        ]

        for ico, nome, end, dist in resultados:
            card = ctk.CTkFrame(
                self._resultados_frame, fg_color=BG_CARD, corner_radius=10
            )
            card.grid(row=0, column=0, sticky="ew", pady=4)
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(card, text=ico, font=("Segoe UI", 18)
                         ).grid(row=0, column=0, rowspan=2, padx=(10, 5))
            ctk.CTkLabel(card, text=nome,
                         font=("Segoe UI", 12, "bold"), text_color=TEXT_MAIN
                         ).grid(row=0, column=1, sticky="w", pady=(6, 0))
            ctk.CTkLabel(card, text=f"{end}  •  {dist}",
                         font=("Segoe UI", 10), text_color=TEXT_MAIN
                         ).grid(row=1, column=1, sticky="w", pady=(0, 6))
            ctk.CTkButton(card, text="Rota", width=55, height=26,
                          font=("Segoe UI", 10),
                          fg_color=BORDER_COLOR, hover_color=NEON_GREEN,
                          text_color=TEXT_MAIN, corner_radius=6
                          ).grid(row=0, column=2, rowspan=2, padx=(0, 8))

    # ============================================================
    # RASTREAMENTO (after)
    # ============================================================
    def iniciar_rastreamento(self):
        if not self.rastreamento_ativo:
            self.rastreamento_ativo = True
            self._tempo_inicio = time.time()
            try:
                self._label_link.configure(text="🛰️  LINK ATIVO (ORBITAL CORE)",
                                           text_color=NEON_GREEN)
                self._btn_start.configure(state="disabled", fg_color=BORDER_COLOR)
            except Exception:
                pass
            self._simular_rastreamento()
            self._atualizar_timer()

    def _parar_rastreamento(self):
        self.rastreamento_ativo = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
        try:
            self._label_link.configure(text="🛰️  SINAL CESSADO", text_color=RED_TEXT)
            self._btn_start.configure(state="normal", fg_color=NEON_GREEN)
        except Exception:
            pass

    def _simular_rastreamento(self):
        if not self.rastreamento_ativo:
            return
        try:
            lat, lon, nome = random.choice(COORDS)
            self._label_coords.configure(text=f"{lat:.4f} , {lon:.4f}")
            self._label_cidade.configure(
                text=f"Localização: {nome} - Região Metropolitana de Belém")
            self._label_velocidade.configure(
                text=f"Velocidade: {random.randint(20, 65)} km/h")
            self._atualizar_mini_mapa(lat, lon)
        except Exception:
            self.rastreamento_ativo = False
            return
        self._after_id = self.after(1500, self._simular_rastreamento)

    def _atualizar_timer(self):
        if not self.rastreamento_ativo:
            return
        try:
            decorrido = int(time.time() - self._tempo_inicio)
            mins, secs = divmod(decorrido, 60)
            self._label_tempo.configure(text=f"Tempo ativo: {mins:02d}:{secs:02d}")
        except Exception:
            pass
        if self.rastreamento_ativo:
            self._timer_id = self.after(1000, self._atualizar_timer)

    def _atualizar_mini_mapa(self, lat_atual, lon_atual):
        c = self._mini_canvas
        c.delete("mini")
        w = c.winfo_width() or 400
        h = 90
        c.create_rectangle(0, 0, w, h, fill=BG_DARK, outline="")

        min_lat, max_lat = -1.48, -1.15
        min_lon, max_lon = -48.55, -48.25

        def to_screen(lat, lon):
            margem = 12
            x = margem + (lon - min_lon) / (max_lon - min_lon) * (w - 2 * margem)
            y = h - margem - (lat - min_lat) / (max_lat - min_lat) * (h - 2 * margem)
            return x, y

        for lat, lon, _ in COORDS:
            x, y = to_screen(lat, lon)
            radius = 3 if (lat, lon) != (lat_atual, lon_atual) else 6
            cor = BORDER_COLOR if (lat, lon) != (lat_atual, lon_atual) else NEON_GREEN
            c.create_oval(x - radius, y - radius, x + radius, y + radius,
                          fill=cor, outline=cor, tags="mini")

        x, y = to_screen(lat_atual, lon_atual)
        for r2 in [8, 14, 20]:
            c.create_oval(x - r2, y - r2, x + r2, y + r2,
                          outline=CYAN_GREEN, width=1, tags="mini")

    # ============================================================
    # DESTRUIR
    # ============================================================
    def destroy(self):
        self._parar_rastreamento()
        super().destroy()


if __name__ == "__main__":
    app = EcopaFusionApp()
    app.after(100, lambda: app.focus_force())
    app.mainloop()
