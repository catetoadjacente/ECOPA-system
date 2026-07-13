import customtkinter as ctk
from tkinter import messagebox
from controllers.coleta_controller import ColetaController


class ColetasView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 5))

        titulo = ctk.CTkLabel(
            header, text="Coletas",
            font=ctk.CTkFont(size=36, weight="bold"), anchor="w"
        )
        titulo.pack(side="left")

        subtitulo = ctk.CTkLabel(
            self.content, text="Gerencia todas as coletas do sistema", anchor="w"
        )
        subtitulo.pack(anchor="w", padx=30)

        # Filtros
        filtros = ctk.CTkFrame(self.content, fg_color="transparent")
        filtros.pack(fill="x", padx=30, pady=20)

        filtro_status = ctk.CTkComboBox(
            filtros, values=["TODOS", "Pendente", "Realizada"],
            width=140, command=self._filtrar
        )
        filtro_status.pack(side="left", padx=5, pady=15)
        self.filtro_status = filtro_status

        btn_limpar = ctk.CTkButton(
            filtros, text="Limpar Filtros", width=120,
            fg_color="#006d12", hover_color="#0a8f2c",
            command=self.montar_tela
        )
        btn_limpar.pack(side="right", pady=15)

        self._montar_tabela()

    def _montar_tabela(self, filtro=None):
        for widget in self.content.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, '_is_tabela'):
                widget.destroy()

        frame_tabela = ctk.CTkFrame(self.content)
        frame_tabela._is_tabela = True
        frame_tabela.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        cabecalhos = ["ID Coleta", "Ponto", "Observação", "Quantidade", "Data", "Status", "Ações"]
        for coluna, texto in enumerate(cabecalhos):
            lbl = ctk.CTkLabel(
                frame_tabela, text=texto,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=coluna, padx=15, pady=10, sticky="w")

        status_cores = {
            "Realizada": "#3adb63",
            "Pendente":  "#ffd657",
        }

        coletas = ColetaController.listar()
        if filtro and filtro != "TODOS":
            coletas = [c for c in coletas if c["status"] == filtro]

        for linha, c in enumerate(coletas, start=1):
            id_str = f"#{int(c['id'])}"
            data_str = c["data_coleta"].strftime("%d/%m/%Y") if c["data_coleta"] else ""
            qtd_str = f"{float(c['quantidade']):.1f}Kg" if c["quantidade"] else ""
            registro = [id_str, c["ponto"], c["observacao"], qtd_str, data_str, c["status"]]

            for coluna, valor in enumerate(registro):
                cor = "white"
                if coluna == 5:
                    cor = status_cores.get(valor, "white")

                lbl = ctk.CTkLabel(
                    frame_tabela, text=valor,
                    fg_color=cor, corner_radius=8,
                    width=130 if coluna != 1 else 200, anchor="w"
                )
                lbl.grid(row=linha, column=coluna, padx=8, pady=5, sticky="w")

            id_coleta = c["id"]
            if c["status"] == "Pendente":
                btn = ctk.CTkButton(
                    frame_tabela, text="Realizar", width=80,
                    fg_color="#27ae60", hover_color="#2ecc71",
                    command=lambda idc=id_coleta: self._marcar_realizada(idc)
                )
                btn.grid(row=linha, column=6, padx=5, pady=4)

    def _filtrar(self, valor):
        self._montar_tabela(filtro=valor)

    def _marcar_realizada(self, id_coleta):
        if messagebox.askyesno("Confirmar", "Marcar esta coleta como realizada?"):
            if ColetaController.atualizar_status(id_coleta, "Realizada"):
                self.montar_tela()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar status!")
