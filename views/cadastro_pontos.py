import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController

DIAS_SEMANA = [
    (1, "Dom"), (2, "Seg"), (3, "Ter"), (4, "Qua"),
    (5, "Qui"), (6, "Sex"), (7, "Sáb")
]

class CadastroPonto(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.content, width=500, height=500)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            frame, text="Novo Ponto de Coleta",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=(20, 15))

        campos = [
            ("Endereco", "endereco"),
            ("Email", "email"),
            ("Estabelecimento", "estabelecimento"),
            ("Telefone", "telefone"),
            ("Proprietario", "proprietario"),
        ]

        self.entries = {}

        for label_text, key in campos:
            lbl = ctk.CTkLabel(frame, text=label_text + ":")
            lbl.pack(anchor="w", padx=20)
            entry = ctk.CTkEntry(frame, width=350)
            entry.pack(padx=20, pady=(0, 10))
            self.entries[key] = entry
            lbl_horarios = ctk.CTkLabel(frame, text="Horário de Funcionamento:")
            lbl_horarios.pack(anchor="w", padx=20, pady=(15, 5))

            self.chk_vars = {}
            self.entry_abertura = {}
            self.entry_fechamento = {}

            for dia_num, dia_nome in DIAS_SEMANA:
                linha = ctk.CTkFrame(frame, fg_color="transparent")
                linha.pack(fill="x", padx=20, pady=1)

                var = ctk.BooleanVar(value=True)
                chk = ctk.CTkCheckBox(linha, text=dia_nome, variable=var, width=50)
                chk.pack(side="left")

                lbl_a = ctk.CTkLabel(linha, text="Abre:", width=40)
                lbl_a.pack(side="left", padx=(10, 0))
                ent_a = ctk.CTkEntry(linha, width=70, placeholder_text="08:00")
                ent_a.pack(side="left", padx=(0, 5))
                ent_a.insert(0, "08:00")

                lbl_f = ctk.CTkLabel(linha, text="Fecha:", width=45)
                lbl_f.pack(side="left")
                ent_f = ctk.CTkEntry(linha, width=70, placeholder_text="17:00")
                ent_f.pack(side="left")
                ent_f.insert(0, "17:00")

                self.chk_vars[dia_num] = var
                self.entry_abertura[dia_num] = ent_a
                self.entry_fechamento[dia_num] = ent_f

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
        dados = {key: entry.get().strip() for key, entry in self.entries.items()}
        horarios = []
        for dia_num, _ in DIAS_SEMANA:
            if self.chk_vars[dia_num].get():
                horarios.append({
                    "dia_semana": dia_num,
                    "abertura": self.entry_abertura[dia_num].get().strip(),
                    "fechamento": self.entry_fechamento[dia_num].get().strip(),
                    "ativo": 1,
                })
        ok, msg = PontoController.cadastrar(dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
