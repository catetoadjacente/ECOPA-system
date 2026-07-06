import customtkinter as ctk
from tkinter import messagebox
from controllers.cliente_controller import ClienteController


class EdicaoCliente(ctk.CTkFrame):
    def __init__(self, master, content, idponto, on_voltar):
        super().__init__(master)
        self.content = content
        self.idponto = idponto
        self.on_voltar = on_voltar
        self.cliente = ClienteController.buscar_por_idponto(idponto)
        if not self.cliente:
            messagebox.showerror("Erro", "Ponto de coleta nao encontrado")
            self.on_voltar()
            return
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content, width=500, height=550)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            frame, text="Editar Ponto de Coleta",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=(20, 15))

        lbl_id = ctk.CTkLabel(frame, text="ID Ponto:")
        lbl_id.pack(anchor="w", padx=20)
        lbl_id_valor = ctk.CTkLabel(
            frame, text=str(self.cliente.get("id_ponto", "")),
            font=ctk.CTkFont(size=14), width=350, anchor="w"
        )
        lbl_id_valor.pack(padx=20, pady=(0, 10))

        lbl_est = ctk.CTkLabel(frame, text="Estabelecimento:")
        lbl_est.pack(anchor="w", padx=20)
        lbl_est_valor = ctk.CTkLabel(
            frame, text=self.cliente.get("estabelecimento", "") or "",
            font=ctk.CTkFont(size=14), width=350, anchor="w"
        )
        lbl_est_valor.pack(padx=20, pady=(0, 10))

        campos = {
            "Endereco": "endereco",
            "Email": "email",
            "Telefone": "telefone",
            "Proprietario": "proprietario",
            "CNPJ": "cnpj",
        }
        self.entries = {}

        for campo, db_key in campos.items():
            lbl = ctk.CTkLabel(frame, text=campo + ":")
            lbl.pack(anchor="w", padx=20)
            entry = ctk.CTkEntry(frame, width=350)
            entry.pack(padx=20, pady=(0, 10))
            entry.insert(0, self.cliente.get(db_key, "") or "")
            self.entries[campo] = entry

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        btn_salvar = ctk.CTkButton(
            btn_frame, text="Salvar", width=120,
            fg_color="#27ae60", hover_color="#2ecc71",
            command=self._on_salvar
        )
        btn_salvar.pack(side="left", padx=10)

        btn_voltar = ctk.CTkButton(
            btn_frame, text="Voltar", width=120,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            command=self.on_voltar
        )
        btn_voltar.pack(side="left", padx=10)

    def _on_salvar(self):
        dados = {campo: entry.get().strip() for campo, entry in self.entries.items()}
        ok, msg = ClienteController.atualizar(self.idponto, dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
