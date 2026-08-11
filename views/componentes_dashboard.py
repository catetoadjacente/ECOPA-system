import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK,
    ECOPA_LEAF, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER,
    ECOPA_ORANGE, ECOPA_BLUE,
    font, font_small, font_small_bold,
)

plt.rcParams["font.family"] = "sans-serif"


class KPICard(ctk.CTkFrame):
    """Card de metrica (KPI) para o dashboard."""

    def __init__(self, master, emoji, titulo, valor, cor, bg_cor, **kwargs):
        super().__init__(
            master, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER, height=100,
            **kwargs
        )
        self.grid_propagate(False)

        ctk.CTkFrame(self, fg_color=cor, height=4, corner_radius=2).pack(fill="x")

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=(10, 12))

        icon_frame = ctk.CTkFrame(inner, fg_color=bg_cor, corner_radius=10, width=44, height=44)
        icon_frame.pack(anchor="w", pady=(0, 8))
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(icon_frame, text=emoji, font=font(22)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inner, text=titulo,
            font=font_small_bold(10), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner, text=valor,
            font=font(28, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(anchor="w")


class GraficoPizza(ctk.CTkFrame):
    """Grafico de pizza para distribuicao de status."""

    def __init__(self, master, titulo, status_count, **kwargs):
        super().__init__(
            master, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER,
            **kwargs
        )

        ctk.CTkLabel(
            self, text=titulo,
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        fig, ax = plt.subplots(figsize=(4.5, 3.2))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        if status_count:
            cores_pizza = {"Pendente": ECOPA_ORANGE, "Realizada": ECOPA_LEAF}
            labels = list(status_count.keys())
            sizes = list(status_count.values())
            colors = [cores_pizza.get(l, "#999") for l in labels]
            ax.pie(
                sizes, labels=labels, autopct="%1.0f%%",
                colors=colors, startangle=90,
                textprops={"fontsize": 10},
                wedgeprops={"linewidth": 2, "edgecolor": ECOPA_WHITE}
            )
            for t in ax.texts:
                t.set_fontweight("bold")
        else:
            ax.text(0.5, 0.5, "Sem dados", ha="center", va="center", fontsize=12)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))
        plt.close(fig)


class GraficoBarras(ctk.CTkFrame):
    """Grafico de barras horizontais para top itens."""

    def __init__(self, master, titulo, dados, **kwargs):
        super().__init__(
            master, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER,
            **kwargs
        )

        ctk.CTkLabel(
            self, text=titulo,
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        fig, ax = plt.subplots(figsize=(4.5, 3.2))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        if dados:
            nomes, qtds = zip(*dados)
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
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))
        plt.close(fig)


class GraficoLinha(ctk.CTkFrame):
    """Grafico de linha para series temporais."""

    def __init__(self, master, titulo, labels, valores, **kwargs):
        super().__init__(
            master, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER,
            **kwargs
        )

        ctk.CTkLabel(
            self, text=titulo,
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        fig, ax = plt.subplots(figsize=(4.5, 3.2))
        fig.patch.set_facecolor(ECOPA_WHITE)
        ax.set_facecolor(ECOPA_WHITE)

        ax.plot(labels, valores, marker="o", color=ECOPA_GREEN, linewidth=2.5,
                markersize=7, markerfacecolor=ECOPA_WHITE, markeredgecolor=ECOPA_GREEN, markeredgewidth=2)
        ax.fill_between(range(len(labels)), valores, alpha=0.12, color=ECOPA_GREEN)
        ax.set_ylim(0, max(valores) + 2 if max(valores) > 0 else 5)
        ax.tick_params(labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(ECOPA_BORDER)
        ax.spines["left"].set_color(ECOPA_BORDER)
        ax.grid(axis="y", alpha=0.3, color=ECOPA_BORDER)

        plt.tight_layout(pad=1)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))
        plt.close(fig)


class CardMetricas(ctk.CTkFrame):
    """Card com lista de metricas resumidas."""

    def __init__(self, master, titulo, metricas, **kwargs):
        super().__init__(
            master, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER,
            **kwargs
        )

        ctk.CTkLabel(
            self, text=titulo,
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 0))

        for titulo_met, valor_met, cor in metricas:
            met_frame = ctk.CTkFrame(self, fg_color="transparent")
            met_frame.pack(fill="x", padx=20, pady=8)

            ctk.CTkFrame(met_frame, fg_color=cor, width=4, corner_radius=2).pack(
                side="left", fill="y", padx=(0, 12), pady=2
            )

            left_met = ctk.CTkFrame(met_frame, fg_color="transparent")
            left_met.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                left_met, text=titulo_met,
                font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                left_met, text=valor_met,
                font=font(18, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
            ).pack(anchor="w")
