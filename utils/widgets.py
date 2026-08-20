import customtkinter as ctk
from utils.theme import ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_RED, ECOPA_ORANGE, ECOPA_BLUE, font, font_small, font_small_bold

ITENS_POR_PAGINA = 15


# ── Toast ──────────────────────────────────────────────────────

_TOAST_COLORS = {
    "success": (ECOPA_GREEN, ECOPA_WHITE),
    "error":   (ECOPA_RED, ECOPA_WHITE),
    "warning": (ECOPA_ORANGE, ECOPA_WHITE),
    "info":    (ECOPA_BLUE, ECOPA_WHITE),
}


class Toast(ctk.CTkToplevel):
    """Notificação temporária que aparece no canto inferior direito."""

    def __init__(self, master, mensagem, tipo="success", duracao=2500):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        bg_color, text_color = _TOAST_COLORS.get(tipo, _TOAST_COLORS["info"])

        self.configure(fg_color=bg_color)

        label = ctk.CTkLabel(
            self, text=mensagem, font=font(13),
            text_color=text_color, wraplength=340, justify="left",
            padx=16, pady=12,
        )
        label.pack()

        self.update_idletasks()

        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        master_w = master.winfo_width()
        master_h = master.winfo_height()
        toast_w = self.winfo_reqwidth()
        toast_h = self.winfo_reqheight()
        margin = 16

        x = master_x + master_w - toast_w - margin
        y = master_y + master_h - toast_h - margin
        self.geometry(f"+{x}+{y}")

        self.after(duracao, self.destroy)


def toast(mensagem, tipo="success", duracao=2500):
    """Atalho rápido — passa a janela raiz automaticamente."""
    import inspect
    frame = inspect.currentframe().f_back
    self = frame.f_locals.get("self")
    root = None
    if self is not None:
        root = getattr(self, "winfo_toplevel", lambda: None)()
    if root is None:
        root = frame.f_locals.get("master") or frame.f_locals.get("parent")
    if root is None:
        root = ctk.CTk()
        root.withdraw()
    Toast(root, mensagem, tipo=tipo, duracao=duracao)


class TabelaPaginada(ctk.CTkFrame):
    """Tabela com cabeçalho fixo, corpo scrollável e paginação.

    Uso:
        def render_row(frame, item, relx):
            ctk.CTkLabel(frame, text=item["nome"], font=font_small(12)).place(relx=relx[0], rely=0.5, anchor="w")

        tabela = TabelaPaginada(parent, colunas=["ID", "Nome"], relx=[0.01, 0.15], on_render=render_row)
        tabela.carregar(dados)
    """

    def __init__(self, master, colunas, relx, on_render=None, **kwargs):
        super().__init__(master, fg_color=ECOPA_WHITE, corner_radius=16,
                         border_width=1, border_color=ECOPA_BORDER, **kwargs)
        self._colunas = colunas
        self._relx = relx
        self._on_render = on_render
        self._dados = []
        self._pagina = 0
        self._total_paginas = 0
        self._linhas_frame = None
        self._nav_frame = None

    def carregar(self, dados):
        self._dados = dados or []
        self._pagina = 0
        self._total_paginas = max(1, (len(self._dados) + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA)
        self._reconstruir()

    def _reconstruir(self):
        for w in self.winfo_children():
            w.destroy()

        cabecalho = ctk.CTkFrame(self, fg_color=ECOPA_GREEN, corner_radius=12, height=40)
        cabecalho.pack(fill="x", padx=16, pady=(16, 4))
        cabecalho.pack_propagate(False)

        for i, nome in enumerate(self._colunas):
            ctk.CTkLabel(
                cabecalho, text=nome,
                font=font_small_bold(12),
                text_color=ECOPA_WHITE, anchor="w"
            ).place(relx=self._relx[i], rely=0.5, anchor="w")

        self._linhas_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._linhas_frame.pack(fill="both", expand=True, padx=16, pady=(4, 0))

        self._nav_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self._nav_frame.pack(fill="x", padx=16, pady=(8, 12))
        self._nav_frame.pack_propagate(False)

        self._render_pagina()

    def _render_pagina(self):
        for w in self._linhas_frame.winfo_children():
            w.destroy()

        inicio = self._pagina * ITENS_POR_PAGINA
        fim = inicio + ITENS_POR_PAGINA
        pagina_dados = self._dados[inicio:fim]

        if not pagina_dados:
            ctk.CTkLabel(
                self._linhas_frame, text="Nenhum registro encontrado",
                font=font(13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            self._render_nav()
            return

        for linha_idx, item in enumerate(pagina_dados):
            bg = ECOPA_BG if linha_idx % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(self._linhas_frame, fg_color=bg, corner_radius=0, height=36)
            row_frame.pack(fill="x", pady=0)
            row_frame.pack_propagate(False)

            row_frame._dados_item = item
            row_frame._linha_abs = inicio + linha_idx

            self._render_linha(row_frame, item)

        self._render_nav()

    def _render_linha(self, row_frame, item):
        if self._on_render:
            self._on_render(row_frame, item, self._relx)
        else:
            for i, valor in enumerate(item.values()):
                ctk.CTkLabel(
                    row_frame, text=str(valor),
                    font=font_small(12), text_color=ECOPA_TEXT, anchor="w"
                ).place(relx=self._relx[i], rely=0.5, anchor="w")

    def _render_nav(self):
        for w in self._nav_frame.winfo_children():
            w.destroy()

        total = len(self._dados)
        inicio = self._pagina * ITENS_POR_PAGINA + 1
        fim = min((self._pagina + 1) * ITENS_POR_PAGINA, total)

        if total == 0:
            ctk.CTkLabel(self._nav_frame, text="0 registros",
                         font=font_small(11), text_color=ECOPA_TEXT_LIGHT).pack(side="left")
            return

        ctk.CTkButton(
            self._nav_frame, text="← Anterior", width=90, height=30,
            fg_color=ECOPA_GREEN_LIGHT if self._pagina > 0 else ECOPA_BORDER,
            hover_color=ECOPA_GREEN_DARK if self._pagina > 0 else ECOPA_BORDER,
            font=font_small_bold(11),
            state="normal" if self._pagina > 0 else "disabled",
            command=self._pagina_anterior
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            self._nav_frame,
            text=f"{inicio}–{fim} de {total}  |  Página {self._pagina + 1}/{self._total_paginas}",
            font=font_small(11), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", expand=True)

        ctk.CTkButton(
            self._nav_frame, text="Próxima →", width=90, height=30,
            fg_color=ECOPA_GREEN_LIGHT if self._pagina < self._total_paginas - 1 else ECOPA_BORDER,
            hover_color=ECOPA_GREEN_DARK if self._pagina < self._total_paginas - 1 else ECOPA_BORDER,
            font=font_small_bold(11),
            state="normal" if self._pagina < self._total_paginas - 1 else "disabled",
            command=self._proxima_pagina
        ).pack(side="left", padx=(8, 0))

    def _pagina_anterior(self):
        if self._pagina > 0:
            self._pagina -= 1
            self._render_pagina()

    def _proxima_pagina(self):
        if self._pagina < self._total_paginas - 1:
            self._pagina += 1
            self._render_pagina()
