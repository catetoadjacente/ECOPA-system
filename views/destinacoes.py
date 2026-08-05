import customtkinter as ctk
from tkinter import messagebox
from controllers.destinacao_controller import DestinacaoController
from views.loading import LoadingOverlay, carregar_em_bg
from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE,
    ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE, ECOPA_LEAF,
    ECOPA_BLUE, ECOPA_RED, font, font_title, font_small, font_small_bold,
)
from utils.widgets import TabelaPaginada

TIPO_CORES = {
    "Reciclagem": (ECOPA_BLUE, "#e8f0f8"),
    "Biomassa": (ECOPA_GREEN, "#e8f5e8"),
    "Compostagem": (ECOPA_LEAF, "#e8f8e8"),
    "Aterro": (ECOPA_ORANGE, "#fdf5e8"),
    "Outro": (ECOPA_TEXT_LIGHT, "#f0f0f0"),
}


class DestinacoesView(ctk.CTkFrame):
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
            left, text="Destinações",
            font=font_title(30), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Locais de destino dos materiais coletados",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkButton(
            right, text="+ Nova Destinacao", width=180, height=38,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font_small_bold(12),
            command=self._cadastrar
        ).pack(anchor="e")

        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0))

        self._montar_tabela(container)

    def _montar_tabela(self, parent):
        frame_tabela = ctk.CTkFrame(
            parent, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        colunas = ["ID", "Nome", "Tipo", "Endereco", "CNPJ", "Telefone", "Acoes"]
        relx = [0.01, 0.06, 0.18, 0.28, 0.48, 0.62, 0.75]

        def _render_row(frame, item, rlx):
            ctk.CTkLabel(frame, text=item["id"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[0], rely=0.5, anchor="w")
            ctk.CTkLabel(frame, text=item["nome"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[1], rely=0.5, anchor="w")

            ctk.CTkLabel(frame, text=item["tipo"], font=font_small_bold(11),
                         fg_color=item["badge_bg"], text_color=item["badge_cor"],
                         corner_radius=8, height=26).place(relx=rlx[2], rely=0.5, anchor="w")

            ctk.CTkLabel(frame, text=item["endereco"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[3], rely=0.5, anchor="w")
            ctk.CTkLabel(frame, text=item["cnpj"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[4], rely=0.5, anchor="w")
            ctk.CTkLabel(frame, text=item["telefone"], font=font_small(12),
                         text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[5], rely=0.5, anchor="w")

            acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
            acoes_frame.place(relx=rlx[6], rely=0.5, anchor="w")

            id_dest = item["id_num"]
            ctk.CTkButton(acoes_frame, text="Editar", width=60, height=28,
                           fg_color=ECOPA_ORANGE, hover_color="#e67e22",
                           corner_radius=8, font=font_small_bold(10),
                           command=lambda ide=id_dest: self._editar(ide)).pack(side="left", padx=2)
            ctk.CTkButton(acoes_frame, text="Excluir", width=60, height=28,
                           fg_color=ECOPA_RED, hover_color="#c0392b",
                           corner_radius=8, font=font_small_bold(10),
                           command=lambda ide=id_dest: self._excluir(ide)).pack(side="left", padx=2)

        self._tabela = TabelaPaginada(frame_tabela, colunas=colunas, relx=relx, on_render=_render_row)
        self._tabela.pack(fill="both", expand=True)

        overlay = LoadingOverlay(frame_tabela, text="Carregando destinações...")
        overlay.start()

        def _carregar():
            return DestinacaoController.listar()

        def _montar(dados):
            overlay.stop()
            if not dados:
                ctk.CTkLabel(frame_tabela, text="Nenhuma destinacao cadastrada",
                             font=font(13), text_color=ECOPA_TEXT_LIGHT).pack(pady=40)
                return

            items = []
            for d in dados:
                tipo = d.get("tipo", "Outro")
                badge_cor, badge_bg = TIPO_CORES.get(tipo, (ECOPA_TEXT_LIGHT, "#f0f0f0"))
                items.append({
                    "id": str(d["id"]),
                    "id_num": d["id"],
                    "nome": d["nome"],
                    "tipo": tipo,
                    "badge_cor": badge_cor,
                    "badge_bg": badge_bg,
                    "endereco": d.get("endereco", ""),
                    "cnpj": d.get("cnpj", "") or "",
                    "telefone": d.get("telefone", "") or "",
                })

            self._tabela.carregar(items)

        carregar_em_bg(frame_tabela, _carregar, _montar)

    def _cadastrar(self):
        from views.cadastro_destinacao import CadastroDestinacao
        CadastroDestinacao(self, self.content, on_voltar=self.montar_tela)

    def _editar(self, id_dest):
        from views.edicao_destinacao import EdicaoDestinacao
        EdicaoDestinacao(self, self.content, id_dest, on_voltar=self.montar_tela)

    def _excluir(self, id_dest):
        if messagebox.askyesno("Confirmar", "Deseja excluir esta destinacao?"):
            DestinacaoController.deletar(id_dest)
            self.montar_tela()
