import customtkinter as ctk
from views.cadastro_gerente import CadastroGerente
from views.cadastro_pontos import CadastroPonto
from views.cadastro_coleta import CadastroColeta

# Paleta ECOPA
ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"
ECOPA_BLUE = "#3498db"


class CadastrosHub(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.abrir_cadastros()

    def abrir_cadastros(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Cadastros",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Escolha o tipo de cadastro",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Linha verde
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Cards de cadastro
        cards_frame = ctk.CTkFrame(container, fg_color="transparent")
        cards_frame.pack(expand=True, fill="both", padx=32, pady=(30, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        cards_frame.grid_rowconfigure(0, weight=1)

        # Card Coleta
        card_coleta = ctk.CTkFrame(
            cards_frame, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER, cursor="hand2"
        )
        card_coleta.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            card_coleta, text="🚛",
            font=ctk.CTkFont(size=44), text_color=ECOPA_GREEN
        ).pack(pady=(40, 8))

        ctk.CTkLabel(
            card_coleta, text="Coleta",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack()

        ctk.CTkLabel(
            card_coleta, text="Cadastrar nova coleta de resíduos",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(4, 20))

        ctk.CTkButton(
            card_coleta, text="Novo Cadastro", width=150, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.nova_coleta
        ).pack(pady=(0, 30))

        # Card Gerente
        card_gerente = ctk.CTkFrame(
            cards_frame, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER, cursor="hand2"
        )
        card_gerente.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            card_gerente, text="👤",
            font=ctk.CTkFont(size=44), text_color=ECOPA_GREEN
        ).pack(pady=(40, 8))

        ctk.CTkLabel(
            card_gerente, text="Gerente",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack()

        ctk.CTkLabel(
            card_gerente, text="Cadastrar novo gerente do sistema",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(4, 20))

        ctk.CTkButton(
            card_gerente, text="Novo Cadastro", width=150, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.novo_gerente
        ).pack(pady=(0, 30))

        # Card Ponto
        card_ponto = ctk.CTkFrame(
            cards_frame, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER, cursor="hand2"
        )
        card_ponto.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            card_ponto, text="📍",
            font=ctk.CTkFont(size=44), text_color=ECOPA_GREEN
        ).pack(pady=(40, 8))

        ctk.CTkLabel(
            card_ponto, text="Ponto de Coleta",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack()

        ctk.CTkLabel(
            card_ponto, text="Cadastrar novo ponto de coleta",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(4, 20))

        ctk.CTkButton(
            card_ponto, text="Novo Cadastro", width=150, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.novo_ponto
        ).pack(pady=(0, 30))

    def novo_gerente(self):
        CadastroGerente(self, self.content, on_voltar=self.abrir_cadastros)

    def novo_ponto(self):
        CadastroPonto(self, self.content, on_voltar=self.abrir_cadastros)

    def nova_coleta(self):
        CadastroColeta(self, self.content, on_voltar=self.abrir_cadastros)
