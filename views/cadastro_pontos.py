import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController

DIAS_SEMANA = [
    (2, "SEG"), (5, "QUI"),
    (3, "TER"), (6, "SEX"),
    (4, "QUA"), (7, "SAB"),
    (1, "DOM"),
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

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="#dcebdc")
        scroll.pack(fill="both", expand=True)

        # Titulo
        ctk.CTkLabel(
            scroll, text="Ponto de Coleta",
            font=ctk.CTkFont(size=26, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(25, 0))

        ctk.CTkLabel(
            scroll, text="preencha os dados para cadastrar um novo ponto de coleta.",
            font=ctk.CTkFont(size=13), text_color="#555", anchor="w"
        ).pack(fill="x", padx=40, pady=(0, 15))

        # Secao Dados
        ctk.CTkLabel(
            scroll, text="Dados",
            font=ctk.CTkFont(size=20, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(10, 0))

        ctk.CTkFrame(scroll, fg_color="#ccc", height=1).pack(fill="x", padx=40, pady=(5, 15))

        campos = [
            ("Nome do estabelecimento", "estabelecimento"),
            ("Endereço", "endereco"),
            ("Nome do responsável", "proprietario"),
            ("Telefone do estabelecimento", "telefone"),
            ("Email", "email"),
        ]

        self.entries = {}

        for label_text, key in campos:
            ctk.CTkLabel(
                scroll, text=label_text,
                font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
            ).pack(fill="x", padx=40, pady=(0, 2))

            entry = ctk.CTkEntry(scroll, height=35, font=ctk.CTkFont(size=13))
            entry.pack(fill="x", padx=40, pady=(0, 12))
            self.entries[key] = entry

        # Secao Horarios
        ctk.CTkLabel(
            scroll, text="Horários de funcionamento",
            font=ctk.CTkFont(size=20, weight="bold"), anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 0))

        ctk.CTkFrame(scroll, fg_color="#ccc", height=1).pack(fill="x", padx=40, pady=(5, 15))

        self.chk_vars = {}
        self.entry_abertura = {}
        self.entry_fechamento = {}

        grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        grid_frame.pack(fill="x", padx=40)

        for i, (dia_num, dia_nome) in enumerate(DIAS_SEMANA):
            row = i // 2
            col = i % 2

            linha = ctk.CTkFrame(grid_frame, fg_color="transparent")
            linha.grid(row=row, column=col, padx=(0, 30), pady=4, sticky="w")

            var = ctk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(linha, text="", variable=var, width=30)
            chk.pack(side="left")

            ctk.CTkLabel(linha, text=dia_nome, width=35, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")

            ent_a = ctk.CTkEntry(linha, width=70, placeholder_text="08:00", font=ctk.CTkFont(size=13))
            ent_a.pack(side="left", padx=(5, 0))
            ent_a.insert(0, "08:00")

            ctk.CTkLabel(linha, text="—", width=20).pack(side="left")

            ent_f = ctk.CTkEntry(linha, width=70, placeholder_text="14:00", font=ctk.CTkFont(size=13))
            ent_f.pack(side="left")
            ent_f.insert(0, "14:00")

            self.chk_vars[dia_num] = var
            self.entry_abertura[dia_num] = ent_a
            self.entry_fechamento[dia_num] = ent_f

        # Botoes
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=(25, 20))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=120, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            font=ctk.CTkFont(size=14),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Salvar", width=120, height=40,
            fg_color="#006d12", hover_color="#0a8f2c",
            font=ctk.CTkFont(size=14),
            command=self._on_salvar
        ).pack(side="right")

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
        ok, msg = PontoController.cadastrar(dados, horarios=horarios if horarios else None)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
