import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController
from models.ponto import Ponto

DIAS_SEMANA = [
    (1, "Dom"), (2, "Seg"), (3, "Ter"), (4, "Qua"),
    (5, "Qui"), (6, "Sex"), (7, "Sáb")
]


class EdicaoPonto(ctk.CTkFrame):
    def __init__(self, master, content, idponto, on_voltar):
        super().__init__(master)
        self.content = content
        self.idponto = idponto
        self.on_voltar = on_voltar
        self.ponto = PontoController.buscar_por_idponto(idponto)
        if not self.ponto:
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
            frame, text=str(self.ponto.get("id_ponto", "")),
            font=ctk.CTkFont(size=14), width=350, anchor="w"
        )
        lbl_id_valor.pack(padx=20, pady=(0, 10))

        lbl_est = ctk.CTkLabel(frame, text="Estabelecimento:")
        lbl_est.pack(anchor="w", padx=20)
        lbl_est_valor = ctk.CTkLabel(
            frame, text=self.ponto.get("estabelecimento", "") or "",
            font=ctk.CTkFont(size=14), width=350, anchor="w"
        )
        lbl_est_valor.pack(padx=20, pady=(0, 10))

        campos = {
            "Endereco": "endereco",
            "Email": "email",
            "Telefone": "telefone",
            "Proprietario": "proprietario",
        }
        self.entries = {}

        for campo, db_key in campos.items():
            lbl = ctk.CTkLabel(frame, text=campo + ":")
            lbl.pack(anchor="w", padx=20)
            entry = ctk.CTkEntry(frame, width=350)
            entry.pack(padx=20, pady=(0, 10))
            entry.insert(0, self.ponto.get(db_key, "") or "")
            self.entries[campo] = entry

        lbl_h = ctk.CTkLabel(frame, text="Horário de Funcionamento:")
        lbl_h.pack(anchor="w", padx=20, pady=(15, 5))

        self.chk_vars = {}
        self.entry_abertura = {}
        self.entry_fechamento = {}

        for dia_num, dia_nome in DIAS_SEMANA:
            linha = ctk.CTkFrame(frame, fg_color="transparent")
            linha.pack(fill="x", padx=20, pady=1)

            var = ctk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(linha, text=dia_nome, variable=var, width=50)
            chk.pack(side="left")

            ctk.CTkLabel(linha, text="Abre:", width=40).pack(side="left", padx=(10, 0))
            ent_a = ctk.CTkEntry(linha, width=70, placeholder_text="08:00")
            ent_a.pack(side="left", padx=(0, 5))
            ent_a.insert(0, "08:00")

            ctk.CTkLabel(linha, text="Fecha:", width=45).pack(side="left")
            ent_f = ctk.CTkEntry(linha, width=70, placeholder_text="17:00")
            ent_f.pack(side="left")
            ent_f.insert(0, "17:00")

            self.chk_vars[dia_num] = var
            self.entry_abertura[dia_num] = ent_a
            self.entry_fechamento[dia_num] = ent_f

        horarios_existentes = Ponto.buscar_horarios(self.idponto)
        horarios_map = {h["dia_semana"]: h for h in horarios_existentes}

        for dia_num, _ in DIAS_SEMANA:
            if dia_num in horarios_map:
                h = horarios_map[dia_num]
                self.chk_vars[dia_num].set(h["ativo"] == 1)
                self.entry_abertura[dia_num].delete(0, ctk.END)
                self.entry_abertura[dia_num].insert(0, str(h["abertura"]))
                self.entry_fechamento[dia_num].delete(0, ctk.END)
                self.entry_fechamento[dia_num].insert(0, str(h["fechamento"]))

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

        horarios = []
        for dia_num, _ in DIAS_SEMANA:
            if self.chk_vars[dia_num].get():
                horarios.append({
                    "dia_semana": dia_num,
                    "abertura": self.entry_abertura[dia_num].get().strip(),
                    "fechamento": self.entry_fechamento[dia_num].get().strip(),
                    "ativo": 1,
                })

        ok, msg = PontoController.atualizar(self.idponto, dados, horarios=horarios if horarios else None)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
