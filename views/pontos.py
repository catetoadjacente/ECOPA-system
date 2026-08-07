import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController
from utils.horas import formatar_hora
from views.loading import LoadingOverlay, carregar_em_bg
from utils.theme import (
    ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE,
    ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE, ECOPA_LEAF,
    ECOPA_BLUE, font, font_title, font_small, font_small_bold,
)
from utils.widgets import TabelaPaginada


class PontosView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
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
            left, text="Pontos de Coleta",
            font=font_title(30), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencie todos os pontos de coleta do sistema",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Linha verde
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Tabela
        frame_tabela = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        colunas = ["ID", "Estabelecimento", "Endereço", "Email", "Proprietário", "Telefone", "Ações"]
        relx = [0.01, 0.05, 0.16, 0.31, 0.46, 0.61, 0.74]

        def _render_row(frame, item, rlx):
            valores = [item["id"], item["estabelecimento"], item["endereco"],
                       item["email"], item["proprietario"], item["telefone"]]
            for i, v in enumerate(valores):
                ctk.CTkLabel(frame, text=str(v), font=font_small(12),
                             text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[i], rely=0.5, anchor="w")

            acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
            acoes_frame.place(relx=rlx[6], rely=0.5, anchor="w")

            idponto = item["id_ponto"]
            ctk.CTkButton(acoes_frame, text="Horários", width=72, height=28,
                           fg_color=ECOPA_BLUE, hover_color="#2980b9",
                           corner_radius=8, font=font_small_bold(10),
                           command=lambda idp=idponto: self._ver_horarios(idp)).pack(side="left", padx=2)
            ctk.CTkButton(acoes_frame, text="Editar", width=60, height=28,
                           fg_color=ECOPA_ORANGE, hover_color="#e67e22",
                           corner_radius=8, font=font_small_bold(10),
                           command=lambda idp=idponto: self.editar_ponto(idp)).pack(side="left", padx=2)
            ctk.CTkButton(acoes_frame, text="Excluir", width=60, height=28,
                           fg_color="#e74c3c", hover_color="#c0392b",
                           corner_radius=8, font=font_small_bold(10),
                           command=lambda idp=idponto: self.excluir_ponto(idp)).pack(side="left", padx=2)

        self._tabela = TabelaPaginada(frame_tabela, colunas=colunas, relx=relx, on_render=_render_row)
        self._tabela.pack(fill="both", expand=True)

        overlay = LoadingOverlay(frame_tabela, text="Carregando pontos...")
        overlay.start()

        def _carregar():
            return PontoController.listar()

        def _montar(pontos):
            overlay.stop()
            if not pontos:
                ctk.CTkLabel(frame_tabela, text="Nenhum ponto de coleta cadastrado",
                             font=font(13), text_color=ECOPA_TEXT_LIGHT).pack(pady=40)
                return

            items = []
            for p in pontos:
                items.append({
                    "id_ponto": p["id_ponto"],
                    "id": str(p.get("id_ponto", "")),
                    "estabelecimento": p.get("estabelecimento", "") or "",
                    "endereco": p.get("endereco", "") or "",
                    "email": p.get("email", "") or "",
                    "proprietario": p.get("proprietario", "") or "",
                    "telefone": p.get("telefone", "") or "",
                })

            self._tabela.carregar(items)

        carregar_em_bg(frame_tabela, _carregar, _montar)

    def editar_ponto(self, idponto):
        from views.edicao_ponto import EdicaoPonto
        EdicaoPonto(self, self.content, idponto, on_voltar=self.montar_tela)

    def excluir_ponto(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja excluir este ponto de coleta?"):
            ok, msg = PontoController.deletar(idponto)
            if ok:
                self.montar_tela()
            else:
                messagebox.showerror("Erro", msg)

    def _ver_horarios(self, idponto):
        horarios = PontoController.buscar_horarios(idponto)
        ponto = PontoController.buscar_por_idponto(idponto)
        nome = ponto.get("estabelecimento", "") if ponto else ""

        dias = {1: "Dom", 2: "Seg", 3: "Ter", 4: "Qua", 5: "Qui", 6: "Sex", 7: "Sáb"}

        if not horarios:
            messagebox.showinfo("Horários", f"{nome}\n\nNenhum horário cadastrado.")
            return

        texto = f"📍 {nome}\n{'─' * 30}\n\n"
        for h in sorted(horarios, key=lambda x: x["dia_semana"]):
            dia = dias.get(h["dia_semana"], "?")
            status = "✓" if h["ativo"] else "✗"
            texto += f"  {dia}:  {h['abertura']} — {h['fechamento']}  {status}\n"

        messagebox.showinfo("Horários de Funcionamento", texto)
