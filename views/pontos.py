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
ECOPA_ORANGE = "#f39c12"
ECOPA_LEAF = "#27ae60"
ECOPA_BLUE = "#3498db"


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
            font=ctk.CTkFont(size=30, weight="bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencie todos os pontos de coleta do sistema",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
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

        # Posições relativas (0.0 a 1.0) para cada coluna — escala com a janela
        COL_RELX = [0.01, 0.05, 0.16, 0.31, 0.46, 0.61, 0.74]

        cabecalhos = ["ID", "Estabelecimento", "Endereço", "Email", "Proprietário", "Telefone", "Ações"]

        # Cabeçalho
        header_frame = ctk.CTkFrame(frame_tabela, fg_color=ECOPA_GREEN, corner_radius=12, height=40)
        header_frame.pack(fill="x", padx=16, pady=(16, 4))
        header_frame.pack_propagate(False)

        for coluna, texto in enumerate(cabecalhos):
            ctk.CTkLabel(
                header_frame, text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=ECOPA_WHITE, anchor="w"
            ).place(relx=COL_RELX[coluna], rely=0.5, anchor="w", y=0)

        # Linhas de dados
        pontos = PontoController.listar()

        if not pontos:
            ctk.CTkLabel(
                frame_tabela, text="Nenhum ponto de coleta cadastrado",
                font=ctk.CTkFont(size=13), text_color=ECOPA_TEXT_LIGHT
            ).pack(pady=40)
            return

        for linha, p in enumerate(pontos):
            bg = ECOPA_BG if linha % 2 == 0 else ECOPA_WHITE
            row_frame = ctk.CTkFrame(frame_tabela, fg_color=bg, corner_radius=0, height=36)
            row_frame.pack(fill="x", padx=16, pady=0)
            row_frame.pack_propagate(False)

            valores = [
                str(p.get("id_ponto", "")),
                p.get("estabelecimento", "") or "",
                p.get("endereco", "") or "",
                p.get("email", "") or "",
                p.get("proprietario", "") or "",
                p.get("telefone", "") or "",
            ]
            for coluna, valor in enumerate(valores):
                ctk.CTkLabel(
                    row_frame, text=str(valor),
                    font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT,
                    anchor="w"
                ).place(relx=COL_RELX[coluna], rely=0.5, anchor="w", y=0)

            idponto = p["id_ponto"]

            acoes_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            acoes_frame.place(relx=COL_RELX[6], rely=0.5, anchor="w", y=0)

            ctk.CTkButton(
                acoes_frame, text="Horários", width=72, height=28,
                fg_color=ECOPA_BLUE, hover_color="#2980b9",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda idp=idponto: self._ver_horarios(idp)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes_frame, text="Editar", width=60, height=28,
                fg_color=ECOPA_ORANGE, hover_color="#e67e22",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda idp=idponto: self.editar_ponto(idp)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                acoes_frame, text="Excluir", width=60, height=28,
                fg_color="#e74c3c", hover_color="#c0392b",
                corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda idp=idponto: self.excluir_ponto(idp)
            ).pack(side="left", padx=2)

    def editar_ponto(self, idponto):
        from views.edicao_ponto import EdicaoPonto
        EdicaoPonto(self, self.content, idponto, on_voltar=self.montar_tela)

    def excluir_ponto(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja excluir este ponto de coleta?"):
            PontoController.deletar(idponto)
            self.montar_tela()

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
