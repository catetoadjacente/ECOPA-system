import customtkinter as ctk
from tkinter import messagebox
from controllers.gerente_controller import GerenteController


class EdicaoGerente(ctk.CTkFrame):
    def __init__(self, master, content, cpf, on_voltar):
        super().__init__(master)
        self.content = content
        self.cpf = cpf
        self.on_voltar = on_voltar
        self.gerente = GerenteController.obter_por_cpf(cpf)
        if not self.gerente:
            messagebox.showerror("Erro", "Gerente nao encontrado")
            self.on_voltar()
            return
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content, width=500, height=450)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            frame, text="Editar Gerente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=(20, 15))

        lbl_nome = ctk.CTkLabel(frame, text="Nome:")
        lbl_nome.pack(anchor="w", padx=20)
        lbl_nome_valor = ctk.CTkLabel(
            frame, text=self.gerente["nome"],
            font=ctk.CTkFont(size=14), width=350, anchor="w"
        )
        lbl_nome_valor.pack(padx=20, pady=(0, 10))

        campos = {
            "Celular": "celular",
            "Email": "email",
            "Setor": "setor",
        }
        self.entries = {}

        for campo, db_key in campos.items():
            lbl = ctk.CTkLabel(frame, text=campo + ":")
            lbl.pack(anchor="w", padx=20)
            entry = ctk.CTkEntry(frame, width=350)
            entry.pack(padx=20, pady=(0, 10))
            entry.insert(0, self.gerente[db_key] or "")
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
        ok, msg = GerenteController.atualizar(self.cpf, dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
