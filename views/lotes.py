import customtkinter as ctk
from controllers.lote_controller import LoteController
from models.relatorio import Relatorio
from views.loading import LoadingOverlay, carregar_em_bg
from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE,
    ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE, ECOPA_LEAF,
    ECOPA_BLUE, font, font_title, font_small, font_small_bold,
)
from utils.widgets import TabelaPaginada


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
            font=font_title(30), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Material disponível para distribuição",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0))

        # KPIs placeholder
        self._kpi_frame = ctk.CTkFrame(container, fg_color="transparent")
        self._kpi_frame.pack(fill="x", padx=32, pady=(20, 0))

        # Tabela placeholder
        self._tabela_frame = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        self._tabela_frame.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        overlay = LoadingOverlay(self._tabela_frame, text="Carregando estoque...")
        overlay.start()

        def _carregar():
            resumo = Relatorio.resumo_estoque()
            lotes = LoteController.listar_todos()
            return resumo, lotes

        def _montar(resultado):
            overlay.stop()
            resumo, lotes = resultado
            self._montar_kpis(resumo)
            self._montar_tabela_lotes(lotes)

        carregar_em_bg(container, _carregar, _montar)

    def _montar_kpis(self, resumo):
        kpi_frame = self._kpi_frame
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
                font=font(10, "bold"),
                text_color=ECOPA_TEXT_LIGHT, anchor="w").pack(anchor="w")
            ctk.CTkLabel(inner, text=valor,
                font=font(22, "bold"),
                text_color=ECOPA_GREEN_DARK, anchor="w").pack(anchor="w")

    def _montar_tabela_lotes(self, lotes):
        for w in self._tabela_frame.winfo_children():
            w.destroy()

        colunas = ["ID", "Fonte", "Qtd Coletada", "Qtd Restante", "Status", "Data"]
        relx = [0.01, 0.08, 0.28, 0.45, 0.62, 0.78]

        def _render_row(frame, item, rlx):
            valores = [item["id"], item["ponto"], item["qtd_colet"], item["qtd_rest"]]
            for i, v in enumerate(valores):
                ctk.CTkLabel(frame, text=v, font=font_small(12),
                             text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[i], rely=0.5, anchor="w")

            ctk.CTkLabel(frame, text=item["status"], font=font_small_bold(11),
                         fg_color=item["badge_bg"], text_color=item["badge_cor"],
                         corner_radius=8, height=26).place(relx=rlx[4], rely=0.5, anchor="w")

            ctk.CTkLabel(frame, text=item["data"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[5], rely=0.5, anchor="w")

        self._tabela = TabelaPaginada(self._tabela_frame, colunas=colunas, relx=relx, on_render=_render_row)
        self._tabela.pack(fill="both", expand=True)

        dados = []
        for l in lotes:
            status = l["status"]
            if status == "Disponivel":
                badge_cor, badge_bg = ECOPA_LEAF, "#e8f8e8"
            elif status == "Parcialmente Consumido":
                badge_cor, badge_bg = ECOPA_ORANGE, "#fdf5e8"
            else:
                badge_cor, badge_bg = ECOPA_TEXT_LIGHT, "#f0f0f0"

            data_str = l["data_criacao"].strftime("%d/%m/%Y") if l["data_criacao"] else ""

            dados.append({
                "id": f"#{l['id']}",
                "ponto": l["ponto"],
                "qtd_colet": f"{float(l['quantidade_coletada']):.1f} Kg",
                "qtd_rest": f"{float(l['quantidade_restante']):.1f} Kg",
                "status": status,
                "badge_cor": badge_cor,
                "badge_bg": badge_bg,
                "data": data_str,
            })

        self._tabela.carregar(dados)
