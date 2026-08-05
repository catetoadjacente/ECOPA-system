import customtkinter as ctk
from tkinter import messagebox
from controllers.gerente_controller import GerenteController
from utils.theme import font, font_small, font_small_bold, ECOPA_GREEN, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE
from utils.widgets import TabelaPaginada


class ListaGerentes(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self._montar()

    def _montar(self):
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
            left, text="Gerentes Cadastrados",
            font=font(30, "bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencie os gerentes do sistema",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        btn_voltar = ctk.CTkButton(
            header, text="← Voltar", width=110, height=36,
            fg_color=ECOPA_TEXT_LIGHT, hover_color="#888888",
            corner_radius=10, font=font_small_bold(12),
            command=self.on_voltar
        )
        btn_voltar.pack(side="right")

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

        colunas = ["CPF", "Nome", "Celular", "Email", "Setor", "Ações"]
        relx = [0.01, 0.12, 0.28, 0.44, 0.60, 0.75]

        def _render_row(frame, item, rlx):
            valores = [item["cpf"], item["nome"], item["celular"], item["email"], item["setor"]]
            for i, v in enumerate(valores):
                ctk.CTkLabel(frame, text=v, font=font_small(12),
                             text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[i], rely=0.5, anchor="w")

            acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
            acoes_frame.place(relx=rlx[5], rely=0.5, anchor="w")

            cpf = item["cpf"]
            ctk.CTkButton(acoes_frame, text="Editar", width=70, height=28,
                           fg_color=ECOPA_ORANGE, hover_color="#e67e22",
                           corner_radius=8, font=font(10, "bold"),
                           command=lambda c=cpf: self._editar(c)).pack(side="left", padx=2)
            ctk.CTkButton(acoes_frame, text="Excluir", width=70, height=28,
                           fg_color="#e74c3c", hover_color="#c0392b",
                           corner_radius=8, font=font(10, "bold"),
                           command=lambda c=cpf: self._excluir(c)).pack(side="left", padx=2)

        tabela = TabelaPaginada(frame_tabela, colunas=colunas, relx=relx, on_render=_render_row)
        tabela.pack(fill="both", expand=True)

        gerentes = GerenteController.listar()

        if not gerentes:
            ctk.CTkLabel(frame_tabela, text="Nenhum gerente cadastrado",
                         font=font(13), text_color=ECOPA_TEXT_LIGHT).pack(pady=40)
            return

        items = [{"cpf": g["cpf"], "nome": g["nome"], "celular": g["celular"],
                  "email": g["email"], "setor": g["setor"]} for g in gerentes]
        tabela.carregar(items)

    def _editar(self, cpf):
        from views.edicao_gerente import EdicaoGerente
        EdicaoGerente(self, self.content, cpf, on_voltar=self._montar)

    def _excluir(self, cpf):
        if messagebox.askyesno("Confirmar", "Deseja excluir este gerente?"):
            ok, msg = GerenteController.deletar(cpf)
            if ok:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)
            self._montar()
