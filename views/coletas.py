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

        # Cabeçalho com título e botão Nova Coleta
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 5))

        titulo = ctk.CTkLabel(
            header, text="Coletas",
            font=ctk.CTkFont(size=36, weight="bold"), anchor="w"
        )
        titulo.pack(side="left")

        btn_nova = ctk.CTkButton(
            header, text="+ Nova Coleta",
            fg_color="#006d12", hover_color="#0a8f2c",
            command=self.abrir_cadastro
        )
        btn_nova.pack(side="right")

        subtitulo = ctk.CTkLabel(
            self.content, text="Gerencia todas as coletas do sistema", anchor="w"
        )
        subtitulo.pack(anchor="w", padx=30)

        # Filtros
        filtros = ctk.CTkFrame(self.content, fg_color="transparent")
        filtros.pack(fill="x", padx=30, pady=20)

        busca = ctk.CTkEntry(
            filtros, placeholder_text="Buscar por ID..."
        )
        busca.pack(side="left", padx=(0, 10), pady=15)

        filtro_status = ctk.CTkComboBox(
            filtros, values=["TODOS", "Pendente", "Em andamento", "Finalizada"],
            width=140
        )
        filtro_status.pack(side="left", padx=5, pady=15)

        filtro_motorista = ctk.CTkComboBox(
            filtros, values=["TODOS", "João", "Maria", "Carlos"],
            width=140
        )
        filtro_motorista.pack(side="left", padx=5, pady=15)

        btn_limpar = ctk.CTkButton(
            filtros, text="Limpar Filtros", width=120,
            fg_color="#006d12", hover_color="#0a8f2c"
        )
        btn_limpar.pack(side="right", pady=15)

        # Tabela
        frame_tabela = ctk.CTkFrame(self.content)
        frame_tabela.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        cabecalhos = ["ID Coleta", "Ponto", "Motorista", "Quantidade", "Data", "Status", "Ações"]
        for coluna, texto in enumerate(cabecalhos):
            lbl = ctk.CTkLabel(
                frame_tabela, text=texto,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=coluna, padx=15, pady=10, sticky="w")

        status_cores = {
            "Finalizada":  "#3adb63",
            "Pendente":    "#ffd657",
            "Em andamento": "#ff9a50",
        }

        coletas = ColetaController.listar()
        for linha, c in enumerate(coletas, start=1):
            id_str = f"#{int(c['id']):06d}"
            data_str = c["data_coleta"].strftime("%d/%m/%Y") if c["data_coleta"] else ""
            qtd_str = f"{float(c['quantidade']):.1f}Kg" if c["quantidade"] else ""
            registro = [id_str, c["ponto"], c["motorista"], qtd_str, data_str, c["status"]]

            for coluna, valor in enumerate(registro):
                cor = "white"
                if coluna == 5:
                    cor = status_cores.get(valor, "white")

                lbl = ctk.CTkLabel(
                    frame_tabela, text=valor,
                    fg_color=cor, corner_radius=8,
                    width=120 if coluna != 1 else 180, anchor="w"
                )
                lbl.grid(row=linha, column=coluna, padx=8, pady=5, sticky="w")

            id_coleta = c["id"]
            btn_remover = ctk.CTkButton(
                frame_tabela, text="Remover", width=80,
                fg_color="#e74c3c", hover_color="#c0392b",
                command=lambda idc=id_coleta: self.remover_coleta(idc)
            )
            btn_remover.grid(row=linha, column=6, padx=5, pady=4)

    def abrir_cadastro(self):
        from views.cadastro_coleta import CadastroColeta
        CadastroColeta(self, self.content, on_voltar=self.montar_tela)

    def remover_coleta(self, id_coleta):
        if messagebox.askyesno("Confirmar", "Deseja remover esta coleta?"):
            if ColetaController.deletar(id_coleta):
                self.montar_tela()
            else:
                messagebox.showerror("Erro", "Falha ao remover coleta!")
