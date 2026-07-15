import customtkinter as ctk
import random
import time
import pywinstyles
import tkinter as tk

# ============================================================
# PALETA VERDE FUTURISTA
# ============================================================
VERDE_ESCURO    = "#0A1A10"
VERDE_CARD      = "#0F2E1D"
VERDE_MEDIO     = "#1A5C3A"
VERDE_CLARO     = "#2ECC71"
VERDE_NEON      = "#00FF88"
VERDE_LIMAO     = "#39FF14"
VERDE_AGUA      = "#1ABC9C"
VERDE_GRADIENTE = "#0D2818"
TEXTO_PRINCIPAL  = "#E8F5E9"
TEXTO_SECUNDARIO = "#A5D6A7"
CINZA_VERDE     = "#1A3A28"

COORDS = [
    (-1.4558, -48.4902, "Belém"),
    (-1.3617, -48.3725, "Ananindeua"),
    (-1.3000, -48.3333, "Marituba"),
    (-1.2000, -48.3000, "Benevides"),
    (-1.4500, -48.4667, "Icoaraci"),
]

class FuturisticApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECOPA Rastreamento - Região Metropolitana de Belém")
        self.geometry("1000x650")
        self.minsize(900, 600)

        # --- pywinstyles: efeito mica/acrylic no Windows 11 ---
        try:
            pywinstyles.apply_style(self, "mica")
            pywinstyles.change_header_color(self, title_bar_color=VERDE_ESCURO)
        except Exception:
            pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.rastreamento_ativo = False
        self._after_id = None
        self._indice_atual = 0

        self._configurar_grid()
        self._criar_menu_lateral()
        self._criar_area_principal()

        self.mostrar_acompanhamento()

    # ===========================================================
    # LAYOUT: GRID (menu | conteúdo) com fundo degradê
    # ===========================================================
    def _configurar_grid(self):
        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _criar_menu_lateral(self):
        self.menu_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=VERDE_CARD,
            border_width=0
        )
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.grid_rowconfigure(6, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.menu_frame, text="🌿 ECOPA",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=VERDE_NEON
        )
        self.logo_label.grid(row=0, column=0, pady=(30, 5), padx=20)

        ctk.CTkLabel(
            self.menu_frame, text="Rastreamento Inteligente",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXTO_SECUNDARIO
        ).grid(row=1, column=0, pady=(0, 25))

        # Separador
        self._desenhar_linha(self.menu_frame, row=2)

        botoes = [
            ("  Navegação",     self.mostrar_navegacao,      "🗺️"),
            ("  Acompanhamento", self.mostrar_acompanhamento, "📍"),
            ("  Busca de Coleta",self.mostrar_busca,         "📦"),
        ]

        self.botoes = {}
        for i, (texto, comando, icone) in enumerate(botoes):
            btn = ctk.CTkButton(
                self.menu_frame, text=f"{icone} {texto}",
                command=comando,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                fg_color="transparent",
                text_color=TEXTO_PRINCIPAL,
                hover_color=VERDE_MEDIO,
                anchor="w",
                corner_radius=8,
                height=40
            )
            btn.grid(row=3 + i, column=0, pady=4, padx=12, sticky="ew")
            self.botoes[texto.strip()] = btn

        # Status
        ctk.CTkLabel(
            self.menu_frame, text="● Online",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=VERDE_CLARO
        ).grid(row=7, column=0, pady=(0, 15))

    def _desenhar_linha(self, parent, row):
        frame = ctk.CTkFrame(parent, height=1, fg_color=VERDE_MEDIO, corner_radius=0)
        frame.grid(row=row, column=0, pady=5, padx=20, sticky="ew")

    def _criar_area_principal(self):
        self.main_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=VERDE_ESCURO
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Canvas para gradiente de fundo
        self.canvas = tk.Canvas(
            self.main_frame, highlightthickness=0, bd=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._redesenhar_gradiente)

        # Frame de conteúdo sobre o canvas
        self.content_frame = ctk.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=25)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _redesenhar_gradiente(self, event=None):
        LARGURA = self.canvas.winfo_width() or 1000
        ALTURA  = self.canvas.winfo_height() or 650
        self.canvas.delete("grad")
        faixas = 80
        for i in range(faixas):
            r = i / faixas
            cor = self._interpolar_cor(VERDE_ESCURO, "#0D2818", r)
            self.canvas.create_rectangle(
                0, ALTURA * i / faixas,
                LARGURA, ALTURA * (i + 1) / faixas,
                fill=cor, outline="", tags="grad"
            )

    @staticmethod
    def _interpolar_cor(c1, c2, t):
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ===========================================================
    # TELA DE NAVEGAÇÃO
    # ===========================================================
    def mostrar_navegacao(self):
        self._parar_rastreamento()
        self._limpar_content()
        self._destacar_botao("Navegação")

        titulo = ctk.CTkLabel(
            self.content_frame, text="🗺️  Navegação Inteligente",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=TEXTO_PRINCIPAL
        )
        titulo.grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(
            self.content_frame, text="Rotas otimizadas para a Região Metropolitana de Belém",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXTO_SECUNDARIO
        ).grid(row=1, column=0, sticky="w", pady=(0, 25))

        # Mapa estilizado
        mapa_frame = self._criar_card(self.content_frame, row=2)
        self._desenhar_mapa(mapa_frame)

        # Informações
        info_frame = ctk.CTkFrame(
            self.content_frame, fg_color="transparent"
        )
        info_frame.grid(row=3, column=0, pady=(20, 0), sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        cards_info = [
            ("🚚", "12 Entregas", "Hoje"),
            ("⏱️", "45 min médio", "Tempo de rota"),
            ("✅", "98%", "Taxa de sucesso"),
        ]
        for i, (ico, val, lbl) in enumerate(cards_info):
            c = self._criar_mini_card(info_frame, i, ico, val, lbl)

    def _desenhar_mapa(self, parent):
        # Canvas para simular mapa com pontos
        canvas = tk.Canvas(
            parent, height=220, highlightthickness=0, bd=0,
            bg=VERDE_CARD
        )
        canvas.pack(fill="x", pady=5)

        w = parent.winfo_width() or 700
        canvas.bind("<Configure>", lambda e: self._render_mapa(canvas, e.width, 220))

        if w > 100:
            self._render_mapa(canvas, w, 220)

    def _render_mapa(self, canvas, w, h):
        canvas.delete("mapa")
        if w < 50:
            return

        margem = 40
        min_lat, max_lat = -1.48, -1.15
        min_lon, max_lon = -48.55, -48.25

        def to_screen(lat, lon):
            x = margem + (lon - min_lon) / (max_lon - min_lon) * (w - 2 * margem)
            y = h - margem - (lat - min_lat) / (max_lat - min_lat) * (h - 2 * margem)
            return x, y

        canvas.create_rectangle(0, 0, w, h, fill=VERDE_CARD, outline="")

        # Grid
        for i in range(5):
            t = i / 4
            lat_ = min_lat + (max_lat - min_lat) * t
            lon_ = min_lon + (max_lon - min_lon) * t
            x, y = to_screen(lat_, lon_)
            canvas.create_line(margem, y, w - margem, y, fill=VERDE_MEDIO, width=1, tags="mapa")
            canvas.create_text(margem - 5, y, text=f"{lat_:.2f}", anchor="e",
                               fill=TEXTO_SECUNDARIO, font=("Segoe UI", 7), tags="mapa")
            canvas.create_line(x, margem, x, h - margem, fill=VERDE_MEDIO, width=1, tags="mapa")
            canvas.create_text(x, h - margem + 10, text=f"{lon_:.2f}", anchor="n",
                               fill=TEXTO_SECUNDARIO, font=("Segoe UI", 7), tags="mapa")

        # Cidades
        for lat, lon, nome in COORDS:
            x, y = to_screen(lat, lon)
            raio = 6
            canvas.create_oval(x - raio, y - raio, x + raio, y + raio,
                               fill=VERDE_NEON, outline=VERDE_LIMAO, width=1.5, tags="mapa")
            canvas.create_text(x, y - 14, text=nome, fill=TEXTO_PRINCIPAL,
                               font=("Segoe UI", 9, "bold"), tags="mapa")

        # Conexões
        for i in range(len(COORDS) - 1):
            x1, y1 = to_screen(COORDS[i][0], COORDS[i][1])
            x2, y2 = to_screen(COORDS[i + 1][0], COORDS[i + 1][1])
            canvas.create_line(x1, y1, x2, y2, fill=VERDE_AGUA, width=1.5,
                               dash=(4, 4), tags="mapa")

    # ===========================================================
    # TELA DE ACOMPANHAMENTO (TEMPO REAL)
    # ===========================================================
    def mostrar_acompanhamento(self):
        self._parar_rastreamento()
        self._limpar_content()
        self._destacar_botao("Acompanhamento")

        titulo = ctk.CTkLabel(
            self.content_frame, text="📍  Acompanhamento em Tempo Real",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=TEXTO_PRINCIPAL
        )
        titulo.grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(
            self.content_frame, text="Monitoramento ao vivo das entregas na região metropolitana",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXTO_SECUNDARIO
        ).grid(row=1, column=0, sticky="w", pady=(0, 25))

        # Card de status
        status_card = self._criar_card(self.content_frame, row=2)

        # Grid dentro do card
        status_card.grid_columnconfigure((0, 1), weight=1)

        # Indicador pulsante
        self.indicador_frame = ctk.CTkFrame(
            status_card, width=16, height=16,
            fg_color=VERDE_CLARO, corner_radius=8
        )
        self.indicador_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        ctk.CTkLabel(
            status_card, text="Rastreamento Ativo",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=VERDE_CLARO
        ).grid(row=0, column=1, sticky="w", pady=10)

        # Coordenadas
        self.label_coords = ctk.CTkLabel(
            status_card, text="Coordenadas: -- , --",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=VERDE_NEON
        )
        self.label_coords.grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 5))

        self.label_cidade = ctk.CTkLabel(
            status_card, text="Localização: ---",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXTO_SECUNDARIO
        )
        self.label_cidade.grid(row=2, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 5))

        self.label_velocidade = ctk.CTkLabel(
            status_card, text="Velocidade: -- km/h",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXTO_SECUNDARIO
        )
        self.label_velocidade.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 10))

        # Mini visualização do mapa
        self.mini_canvas = tk.Canvas(
            status_card, height=120, highlightthickness=0, bd=0,
            bg=VERDE_CARD
        )
        self.mini_canvas.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # Botões
        botoes_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        botoes_frame.grid(row=3, column=0, pady=20, sticky="ew")

        self.btn_iniciar = ctk.CTkButton(
            botoes_frame, text="▶  Iniciar Rastreamento",
            command=self.iniciar_rastreamento,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=VERDE_CLARO, text_color=VERDE_ESCURO,
            hover_color=VERDE_NEON, corner_radius=10,
            height=40, width=200
        )
        self.btn_iniciar.pack(side="left", padx=(0, 10))

        self.btn_parar = ctk.CTkButton(
            botoes_frame, text="⏹  Parar Rastreamento",
            command=self._parar_rastreamento,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=CINZA_VERDE, text_color=TEXTO_PRINCIPAL,
            hover_color=VERDE_MEDIO, corner_radius=10,
            height=40, width=200
        )
        self.btn_parar.pack(side="left")

        self.label_tempo = ctk.CTkLabel(
            self.content_frame, text="Tempo ativo: 00:00",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXTO_SECUNDARIO
        )
        self.label_tempo.grid(row=4, column=0, pady=(0, 10), sticky="w")

    # ===========================================================
    # TELA DE BUSCA DE COLETA
    # ===========================================================
    def mostrar_busca(self):
        self._parar_rastreamento()
        self._limpar_content()
        self._destacar_botao("Busca de Coleta")

        titulo = ctk.CTkLabel(
            self.content_frame, text="📦  Busca de Coleta",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=TEXTO_PRINCIPAL
        )
        titulo.grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(
            self.content_frame, text="Encontre pontos de coleta próximos em Belém e região",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXTO_SECUNDARIO
        ).grid(row=1, column=0, sticky="w", pady=(0, 25))

        # Busca
        busca_card = self._criar_card(self.content_frame, row=2)
        busca_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            busca_card, text="Digite o endereço:",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXTO_PRINCIPAL
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

        entrada_frame = ctk.CTkFrame(busca_card, fg_color="transparent")
        entrada_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        entrada_frame.grid_columnconfigure(0, weight=1)

        self.entry_busca = ctk.CTkEntry(
            entrada_frame,
            placeholder_text="Ex: Av. Nazaré, Belém - PA",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=VERDE_CARD, border_color=VERDE_MEDIO,
            text_color=TEXTO_PRINCIPAL, placeholder_text_color=TEXTO_SECUNDARIO,
            corner_radius=8, height=40
        )
        self.entry_busca.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        ctk.CTkButton(
            entrada_frame, text="🔍 Buscar",
            command=self._buscar_simulada,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=VERDE_CLARO, text_color=VERDE_ESCURO,
            hover_color=VERDE_NEON, corner_radius=8,
            height=40, width=120
        ).grid(row=0, column=1)

        # Resultados
        self.resultados_frame = ctk.CTkFrame(
            self.content_frame, fg_color="transparent"
        )
        self.resultados_frame.grid(row=3, column=0, pady=(20, 0), sticky="nsew")
        self.resultados_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(5, weight=1)

        # Resultados simulados iniciais
        self._mostrar_resultados_simulados()

    def _buscar_simulada(self):
        self._mostrar_resultados_simulados()

    def _mostrar_resultados_simulados(self):
        for w in self.resultados_frame.winfo_children():
            w.destroy()

        resultados = [
            ("🟢", "Ecoponto Belém Centro", "Av. Presidente Vargas, 500", "2.3 km"),
            ("🟢", "Coleta Ananindeua", "BR-316, Km 4", "5.1 km"),
            ("🟡", "Ponto Marituba", "Rua dos Maguary, 120", "8.7 km"),
            ("🔵", "Coleta Benevides", "Rod. BR-408, s/n", "15.2 km"),
        ]

        for i, (ico, nome, endereco, dist) in enumerate(resultados):
            card = self._criar_mini_card_resultado(self.resultados_frame, i, ico, nome, endereco, dist)

    # ===========================================================
    # RASTREAMENTO (TEMPO REAL via after)
    # ===========================================================
    def iniciar_rastreamento(self):
        if not self.rastreamento_ativo:
            self.rastreamento_ativo = True
            self._indice_atual = 0
            self._tempo_inicio = time.time()
            self._simular_rastreamento()
            self._atualizar_tempo()

    def _atualizar_tempo(self):
        if self.rastreamento_ativo:
            decorrido = int(time.time() - self._tempo_inicio)
            mins, secs = divmod(decorrido, 60)
            try:
                self.label_tempo.configure(text=f"Tempo ativo: {mins:02d}:{secs:02d}")
            except Exception:
                pass
            self.after(1000, self._atualizar_tempo)

    def _parar_rastreamento(self):
        self.rastreamento_ativo = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _simular_rastreamento(self):
        if not self.rastreamento_ativo:
            return
        try:
            lat, lon, nome = random.choice(COORDS)
            self.label_coords.configure(text=f"Coordenadas: {lat:.4f}, {lon:.4f}")
            self.label_cidade.configure(text=f"Localização: {nome} - Região Metropolitana de Belém")
            self.label_velocidade.configure(text=f"Velocidade: {random.randint(20, 65)} km/h")
            self._atualizar_mini_mapa(lat, lon)
        except Exception:
            self.rastreamento_ativo = False
            return
        self._after_id = self.after(2000, self._simular_rastreamento)

    def _atualizar_mini_mapa(self, lat_atual, lon_atual):
        w = self.mini_canvas.winfo_width() or 500
        h = 120
        self.mini_canvas.delete("mini")
        self.mini_canvas.create_rectangle(0, 0, w, h, fill=VERDE_CARD, outline="")

        min_lat, max_lat = -1.48, -1.15
        min_lon, max_lon = -48.55, -48.25

        def to_screen(lat, lon):
            margem = 15
            x = margem + (lon - min_lon) / (max_lon - min_lon) * (w - 2 * margem)
            y = h - margem - (lat - min_lat) / (max_lat - min_lat) * (h - 2 * margem)
            return x, y

        for lat, lon, nome in COORDS:
            x, y = to_screen(lat, lon)
            r = 3 if (lat, lon) != (lat_atual, lon_atual) else 7
            cor = VERDE_MEDIO if (lat, lon) != (lat_atual, lon_atual) else VERDE_NEON
            self.mini_canvas.create_oval(x - r, y - r, x + r, y + r,
                                         fill=cor, outline=cor, tags="mini")

        # Pulse no local atual
        x, y = to_screen(lat_atual, lon_atual)
        for r2 in [10, 16, 22]:
            self.mini_canvas.create_oval(x - r2, y - r2, x + r2, y + r2,
                                         outline=VERDE_LIMAO, width=1, tags="mini")

    # ===========================================================
    # UTILITÁRIOS DE UI
    # ===========================================================
    def _criar_card(self, parent, row):
        card = ctk.CTkFrame(
            parent, fg_color=VERDE_CARD,
            corner_radius=12, border_width=0
        )
        card.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        return card

    def _criar_mini_card(self, parent, col, icone, valor, label):
        card = ctk.CTkFrame(
            parent, fg_color=VERDE_CARD, corner_radius=10
        )
        card.grid(row=0, column=col, sticky="ew", padx=5)

        ctk.CTkLabel(
            card, text=icone, font=ctk.CTkFont(size=24), text_color=TEXTO_PRINCIPAL
        ).pack(pady=(10, 2))
        ctk.CTkLabel(
            card, text=valor, font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=VERDE_CLARO
        ).pack()
        ctk.CTkLabel(
            card, text=label, font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=TEXTO_SECUNDARIO
        ).pack(pady=(0, 10))
        return card

    def _criar_mini_card_resultado(self, parent, row, icone, nome, endereco, dist):
        card = ctk.CTkFrame(
            parent, fg_color=VERDE_CARD, corner_radius=10
        )
        card.grid(row=row, column=0, sticky="ew", pady=4)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card, text=icone, font=ctk.CTkFont(size=20)
        ).grid(row=0, column=0, rowspan=2, padx=(12, 8))

        ctk.CTkLabel(
            card, text=nome, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=TEXTO_PRINCIPAL
        ).grid(row=0, column=1, sticky="w", pady=(8, 0))

        ctk.CTkLabel(
            card, text=f"{endereco}  •  {dist}",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXTO_SECUNDARIO
        ).grid(row=1, column=1, sticky="w", pady=(0, 8))

        ctk.CTkButton(
            card, text="Rota", width=60, height=28,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=VERDE_MEDIO, hover_color=VERDE_CLARO,
            text_color=TEXTO_PRINCIPAL, corner_radius=6
        ).grid(row=0, column=2, rowspan=2, padx=(0, 10))
        return card

    def _limpar_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if hasattr(self, 'label_tempo'):
            try:
                self.label_tempo.destroy()
            except Exception:
                pass

    def _destacar_botao(self, ativo):
        for nome, btn in self.botoes.items():
            if nome == ativo:
                btn.configure(fg_color=VERDE_MEDIO, text_color=VERDE_NEON)
            else:
                btn.configure(fg_color="transparent", text_color=TEXTO_PRINCIPAL)

    def destroy(self):
        self._parar_rastreamento()
        super().destroy()


if __name__ == "__main__":
    app = FuturisticApp()
    app.mainloop()
