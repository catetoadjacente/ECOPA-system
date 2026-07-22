import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController

# Paleta ECOPA
ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"

DIAS_SEMANA = [
    (2, "SEG"), (5, "QUI"),
    (3, "TER"), (6, "SEX"),
    (4, "QUA"), (7, "SAB"),
    (1, "DOM"),
]


class CadastroPonto(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        # Card principal
        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=40, pady=(25, 20))

        # Header
        ctk.CTkLabel(
            card, text="📍",
            font=ctk.CTkFont(size=36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Novo Ponto de Coleta",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            card, text="Preencha os dados para cadastrar um novo ponto de coleta",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(0, 16))

        # Secao Dados
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

        ctk.CTkLabel(
            card, text="Dados do Estabelecimento",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=ECOPA_GREEN_DARK,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        campos = [
            ("Nome do estabelecimento", "estabelecimento", "Ex: Mercado Central"),
            ("Endereço", "endereco", "Rua, número, bairro"),
            ("Nome do responsável", "proprietario", "Nome completo"),
            ("Telefone do estabelecimento", "telefone", "Somente números"),
            ("Email", "email", "email@exemplo.com"),
        ]

        self.entries = {}

        for label_text, key, placeholder in campos:
            lbl = ctk.CTkLabel(
                card, text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
                anchor="w"
            )
            lbl.pack(fill="x", padx=55, pady=(0, 3))

            entry = ctk.CTkEntry(
                card, height=38, placeholder_text=placeholder,
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=10, font=ctk.CTkFont(size=13),
                border_width=1
            )
            entry.pack(fill="x", padx=55, pady=(0, 10))
            self.entries[key] = entry

        # Secao Horarios
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(12, 12))

        ctk.CTkLabel(
            card, text="Horários de Funcionamento",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=ECOPA_GREEN_DARK,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        self.chk_vars = {}
        self.entry_abertura = {}
        self.entry_fechamento = {}

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=55)

        for i, (dia_num, dia_nome) in enumerate(DIAS_SEMANA):
            row = i // 2
            col = i % 2

            linha = ctk.CTkFrame(grid_frame, fg_color="transparent")
            linha.grid(row=row, column=col, padx=(0, 30), pady=4, sticky="w")

            var = ctk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(
                linha, text="", variable=var, width=28,
                fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT
            )
            chk.pack(side="left")

            ctk.CTkLabel(
                linha, text=dia_nome, width=38,
                font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT
            ).pack(side="left")

            ent_a = ctk.CTkEntry(
                linha, width=72, placeholder_text="08:00",
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=8, font=ctk.CTkFont(size=12), border_width=1
            )
            ent_a.pack(side="left", padx=(5, 0))
            ent_a.insert(0, "08:00")

            ctk.CTkLabel(linha, text="—", width=16, text_color=ECOPA_TEXT_LIGHT).pack(side="left")

            ent_f = ctk.CTkEntry(
                linha, width=72, placeholder_text="14:00",
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=8, font=ctk.CTkFont(size=12), border_width=1
            )
            ent_f.pack(side="left")
            ent_f.insert(0, "14:00")

            self.chk_vars[dia_num] = var
            self.entry_abertura[dia_num] = ent_a
            self.entry_fechamento[dia_num] = ent_f

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(25, 25))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=42,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=42,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_salvar
        ).pack(side="right")

    def _on_salvar(self):
        dados = {key: entry.get().strip() for key, entry in self.entries.items()}
        horarios = []
        for dia_num, _ in DIAS_SEMANA:
            if self.chk_vars[dia_num].get():
                horarios.append({
                    "dia_semana": dia_num,
                    "abertura": self.entry_abertura[dia_num].get().strip(),
                    "fechamento": self.entry_fechamento[dia_num].get().strip(),
                    "ativo": 1,
                })
        ok, msg = PontoController.cadastrar(dados, horarios=horarios if horarios else None)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
