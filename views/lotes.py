import customtkinter as ctk
from controllers.lote_controller import LoteController
from models.relatorio import Relatorio

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


class LotesView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Estoque (Lotes)",
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Material disponível para distribuição",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0))

        # KPIs
        resumo = Relatorio.resumo_estoque()
        kpi_frame = ctk.CTkFrame(container, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=32, pady=(20, 0))
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        kpis = [
            ("ESTOQUE TOTAL", f"{float(resumo.get('estoque_total', 0)):.1f} Kg", ECOPA_GREEN, "#e8f5e8"),
            ("LOTES DISPONIVEIS", str(resumo.get('lotes_disponiveis', 0)), ECOPA_BLUE, "#e8f0f8"),
            ("LOTES ESGOTADOS", str(resumo.get('lotes_esgotados', 0)), ECOPA_ORANGE, "#fdf5e8"),
        ]

        for i, (titulo, valor, cor, bg_cor) in enumerate(kpis):
            card = ctk.CTkFrame(
                kpi_frame, fg_color=ECOPA_WHITE, corner_radius=14,
                border_width=1, border_color=ECOPA_BORDER, height=80)
            card.grid(row=0, column=i, padx=6, pady=5, sticky="ew")
            card.grid_propagate(False)
            ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=2).pack(fill="x")
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=14, pady=(8, 10))
            ctk.CTkLabel(inner, text=titulo,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=ECOPA_TEXT_LIGHT, anchor="w").pack(anchor="w")
            ctk.CTkLabel(inner, text=valor,
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=ECOPA_GREEN_DARK, anchor="w").pack(anchor="w")

        # Tabela
        frame_tabela = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        cabecalhos = ["ID", "Fonte", "Qtd Coletada", "Qtd Restante", "Status", "Data"]
        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12)
        header_frame.pack(fill="x", padx=16, pady=(16, 0))

        for col, texto in enumerate(cabecalhos):
            w = 200 if col == 1 else 120
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, width=w
            ).grid(row=0, column=col, padx=8, pady=10, sticky="w")

        lotes = LoteController.listar_todos()

        if not lotes:
            ctk.CTkLabel(
                frame_tabela, text="Nenhum lote cadastrado",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for linha, l in enumerate(lotes, start=1):
            bg = ECOPA_BG if linha % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0)
            row_frame.pack(fill="x", padx=16)

            status = l["status"]
            if status == "Disponivel":
                badge_cor, badge_bg = ECOPA_LEAF, "#e8f8e8"
            elif status == "Parcialmente Consumido":
                badge_cor, badge_bg = ECOPA_ORANGE, "#fdf5e8"
            else:
                badge_cor, badge_bg = ECOPA_TEXT_LIGHT, "#f0f0f0"

            data_str = l["data_criacao"].strftime("%d/%m/%Y") if l["data_criacao"] else ""
            qtd_colet = f"{float(l['quantidade_coletada']):.1f} Kg"
            qtd_rest = f"{float(l['quantidade_restante']):.1f} Kg"

            valores = [f"#{l['id']}", l["ponto"], qtd_colet, qtd_rest]
            for col, valor in enumerate(valores):
                w = 200 if col == 1 else 120
                ctk.CTkLabel(
                    row_frame, text=valor,
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    width=w, anchor="w"
                ).grid(row=0, column=col, padx=8, pady=6, sticky="w")

            badge = ctk.CTkLabel(
                row_frame, text=status, font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=badge_bg, text_color=badge_cor,
                corner_radius=8, width=100, height=26)
            badge.grid(row=0, column=4, padx=6, pady=6, sticky="w")

            ctk.CTkLabel(
                row_frame, text=data_str,
                font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                width=120, anchor="w"
            ).grid(row=0, column=5, padx=8, pady=6, sticky="w")
