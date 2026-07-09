import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController


class ListaPontos(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        label = ctk.CTkLabel(
            header, text="Pontos de Coleta Cadastrados",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(side="left")

        btn_voltar = ctk.CTkButton(
            header, text="Voltar", width=100,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            command=self.on_voltar
        )
        btn_voltar.pack(side="right")

        colunas = ["ID", "Estabelecimento", "Endereco", "Email", "Telefone", "Proprietario", "Acoes"]
        frame_tabela = ctk.CTkFrame(self.content)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        for i, col in enumerate(colunas):
            lbl = ctk.CTkLabel(
                frame_tabela, text=col,
                font=ctk.CTkFont(weight="bold"),
                width=120
            )
            lbl.grid(row=0, column=i, padx=5, pady=8, sticky="w")

        pontos = PontoController.listar()
        for row, ponto in enumerate(pontos, start=1):
            ctk.CTkLabel(frame_tabela, text=str(ponto.get("idponto", "")), width=80).grid(row=row, column=0, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=ponto.get("estabelecimento", "") or "", width=150).grid(row=row, column=1, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=ponto.get("endereco", "") or "", width=150).grid(row=row, column=2, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=ponto.get("email", "") or "", width=150).grid(row=row, column=3, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=ponto.get("telefone", "") or "", width=120).grid(row=row, column=4, padx=5, pady=4, sticky="w")
            ctk.CTkLabel(frame_tabela, text=ponto.get("proprietario", "") or "", width=120).grid(row=row, column=5, padx=5, pady=4, sticky="w")

            btn_editar = ctk.CTkButton(
                frame_tabela, text="Editar", width=70,
                fg_color="#f39c12", hover_color="#e67e22",
                command=lambda idp=ponto["idponto"]: self._editar(idp)
            )
            btn_editar.grid(row=row, column=6, padx=2)

            btn_excluir = ctk.CTkButton(
                frame_tabela, text="Excluir", width=70,
                fg_color="#e74c3c", hover_color="#c0392b",
                command=lambda idp=ponto["idponto"]: self._excluir(idp)
            )
            btn_excluir.grid(row=row, column=7, padx=2)

    def _editar(self, idponto):
        from views.edicao_ponto import EdicaoPonto
        EdicaoPonto(self, self.content, idponto, on_voltar=self._montar)

    def _excluir(self, idponto):
        if messagebox.askyesno("Confirmar", "Deseja excluir este ponto de coleta?"):
            ok, msg = PontoController.deletar(idponto)
            if ok:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)
            self._montar()
