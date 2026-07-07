import customtkinter as ctk
from tkinter import messagebox
from controllers.cliente_controller import ClienteController


class PontosView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 0))

        titulo = ctk.CTkLabel(
            header, text="Pontos de coleta",
            font=ctk.CTkFont(size=34, weight="bold"), anchor="w"
        )
        titulo.pack(side="left")

        btn_novo = ctk.CTkButton(
            header, text="+ Novo Ponto",
            fg_color="#006d12", hover_color="#0a8f2c",
            command=self.novo_ponto
        )
        btn_novo.pack(side="right")

        subtitulo = ctk.CTkLabel(
            self.content, text="Gerencie todos os pontos de coleta do sistema", anchor="w"
        )
        subtitulo.pack(anchor="w", padx=30)

        frame_tabela = ctk.CTkFrame(self.content)
        frame_tabela.pack(fill="both", expand=True, padx=30, pady=(20, 20))

        cabecalhos = ["ID Ponto", "Estabelecimento", "Endereço", "Email", "Proprietário", "Telefone"]
        for coluna, texto in enumerate(cabecalhos):
            lbl = ctk.CTkLabel(
                frame_tabela, text=texto,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=coluna, padx=10, pady=10)

        pontos = ClienteController.listar()
        for linha, p in enumerate(pontos, start=1):
            valores = [
                p.get("id_ponto", ""),
                p.get("estabelecimento", "") or "",
                p.get("endereco", "") or "",
                p.get("email", "") or "",
                p.get("proprietario", "") or "",
                p.get("telefone", "") or "",
            ]
            for coluna, valor in enumerate(valores):
                lbl = ctk.CTkLabel(
                    frame_tabela, text=str(valor),
                    width=120 if coluna != 2 else 200
                )
                lbl.grid(row=linha, column=coluna, padx=8, pady=4)

            idponto = p["id_ponto"]
            btn_editar = ctk.CTkButton(
                frame_tabela, text="Editar", width=70,
                fg_color="#f39c12", hover_color="#e67e22",
                command=lambda idp=idponto: self.editar_ponto(idp)
            )
            btn_editar.grid(row=linha, column=6, padx=2)

            btn_excluir = ctk.CTkButton(
                frame_tabela, text="Excluir", width=70,
                fg_color="#e74c3c", hover_color="#c0392b",
                command=lambda idp=idponto: self.excluir_ponto(idp)
            )
            btn_excluir.grid(row=linha, column=7, padx=2)

    def novo_ponto(self):
        from views.cadastro_clientes import CadastroCliente
        CadastroCliente(self, self.content, on_voltar=self.montar_tela)

    def editar_ponto(self, idponto):
        from views.edicao_cliente import EdicaoCliente
        EdicaoCliente(self, self.content, idponto, on_voltar=self.montar_tela)

    def excluir_ponto(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja excluir este ponto de coleta?"):
            ClienteController.deletar(idponto)
            self.montar_tela()