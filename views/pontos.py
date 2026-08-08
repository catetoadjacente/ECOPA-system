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
        self._mostrar_inativos = ctk.BooleanVar(value=False)
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

        ctk.CTkSwitch(
            header, text="Mostrar inativos", variable=self._mostrar_inativos,
            font=font_small(12), text_color=ECOPA_TEXT,
            button_color=ECOPA_GREEN, progress_color=ECOPA_GREEN_LIGHT,
            command=self.montar_tela
        ).pack(side="right", pady=(8, 0))

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
            if item["ativo"]:
                ctk.CTkButton(acoes_frame, text="Desativar", width=70, height=28,
                               fg_color="#e74c3c", hover_color="#c0392b",
                               corner_radius=8, font=font_small_bold(10),
                               command=lambda idp=idponto: self.desativar_ponto(idp)).pack(side="left", padx=2)
            else:
                ctk.CTkButton(acoes_frame, text="Reativar", width=70, height=28,
                               fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
                               corner_radius=8, font=font_small_bold(10),
                               command=lambda idp=idponto: self.reativar_ponto(idp)).pack(side="left", padx=2)

        self._tabela = TabelaPaginada(frame_tabela, colunas=colunas, relx=relx, on_render=_render_row)
        self._tabela.pack(fill="both", expand=True)

        overlay = LoadingOverlay(frame_tabela, text="Carregando pontos...")
        overlay.start()

        def _carregar():
            if self._mostrar_inativos.get():
                return PontoController.listar_todos()
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
                    "ativo": p.get("ativo", 1) == 1,
                })

            self._tabela.carregar(items)

        carregar_em_bg(frame_tabela, _carregar, _montar)

    def editar_ponto(self, idponto):
        from views.edicao_ponto import EdicaoPonto
        EdicaoPonto(self, self.content, idponto, on_voltar=self.montar_tela)

    def desativar_ponto(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja desativar este ponto de coleta?"):
            ok, msg = PontoController.desativar(idponto)
            if ok:
                self.montar_tela()
            else:
                messagebox.showerror("Erro", msg)

    def reativar_ponto(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja reativar este ponto de coleta?"):
            ok, msg = PontoController.reativar(idponto)
            if ok:
                self.montar_tela()
            else:
                messagebox.showerror("Erro", msg)

    def _ver_horarios(self, idponto):
        horarios = PontoController.buscar_horarios(idponto)
        ponto = PontoController.buscar_por_idponto(idponto)
        nome = ponto.get("estabelecimento", "") if ponto else ""

        if not horarios:
            messagebox.showinfo("Horários", f"{nome}\n\nNenhum horário cadastrado.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Horários de Funcionamento")
        dialog.geometry("420x380")
        dialog.resizable(False, False)
        dialog.grab_set()

        header_frame = ctk.CTkFrame(dialog, fg_color=ECOPA_GREEN, corner_radius=0)
        header_frame.pack(fill="x")

        ctk.CTkLabel(
            header_frame, text=f"📍 {nome}",
            font=font(16, "bold"), text_color=ECOPA_WHITE
        ).pack(pady=(16, 12))

        table_frame = ctk.CTkFrame(dialog, fg_color=ECOPA_WHITE, corner_radius=0)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        dias = {1: "Dom", 2: "Seg", 3: "Ter", 4: "Qua", 5: "Qui", 6: "Sex", 7: "Sáb"}

        header_row = ctk.CTkFrame(table_frame, fg_color=ECOPA_GREEN, corner_radius=6)
        header_row.pack(fill="x", padx=8, pady=(8, 4))

        ctk.CTkLabel(header_row, text="Dia", font=font_small_bold(12),
                     text_color=ECOPA_WHITE, width=60).pack(side="left", padx=(12, 0))
        ctk.CTkLabel(header_row, text="Abertura", font=font_small_bold(12),
                     text_color=ECOPA_WHITE, width=80).pack(side="left", padx=8)
        ctk.CTkLabel(header_row, text="Fechamento", font=font_small_bold(12),
                     text_color=ECOPA_WHITE, width=80).pack(side="left", padx=8)
        ctk.CTkLabel(header_row, text="Status", font=font_small_bold(12),
                     text_color=ECOPA_WHITE, width=60).pack(side="left", padx=(0, 12))

        for i, h in enumerate(sorted(horarios, key=lambda x: x["dia_semana"])):
            dia = dias.get(h["dia_semana"], "?")
            bg = "#f8faf8" if i % 2 == 0 else ECOPA_WHITE
            row = ctk.CTkFrame(table_frame, fg_color=bg, corner_radius=0)
            row.pack(fill="x", padx=8, pady=1)

            ctk.CTkLabel(row, text=dia, font=font_small(12),
                         text_color=ECOPA_TEXT, width=60).pack(side="left", padx=(12, 0))
            ctk.CTkLabel(row, text=formatar_hora(h["abertura"]), font=font_small(12),
                         text_color=ECOPA_TEXT, width=80).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=formatar_hora(h["fechamento"]), font=font_small(12),
                         text_color=ECOPA_TEXT, width=80).pack(side="left", padx=8)

            status_text = "Ativo" if h["ativo"] else "Inativo"
            status_color = ECOPA_GREEN if h["ativo"] else "#e74c3c"
            ctk.CTkLabel(row, text=status_text, font=font_small_bold(11),
                         text_color=status_color, width=60).pack(side="left", padx=(0, 12))

        btn_frame = ctk.CTkFrame(dialog, fg_color=ECOPA_WHITE)
        btn_frame.pack(fill="x", padx=16, pady=12)

        ctk.CTkButton(
            btn_frame, text="Fechar", width=120, height=36,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=8, font=font(12, "bold"),
            command=dialog.destroy
        ).pack()
