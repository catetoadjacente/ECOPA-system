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
            messagebox.showerror("Erro", "Ponto de coleta não encontrado")
            self.on_voltar()
            return
        self._montar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        # Card principal
        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=40, pady=(25, 20))

        # Header
        ctk.CTkLabel(
            card, text="📍",
            font=ctk.CTkFont(size=36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Editar Ponto de Coleta",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        # Separador
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(16, 12))

        # Info read-only
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=55, pady=(0, 8))

        ctk.CTkLabel(
            info_frame, text="ID:",
            font=ctk.CTkFont(size=11), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left")
        ctk.CTkLabel(
            info_frame, text=str(self.ponto.get("id_ponto", "")),
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT
        ).pack(side="left", padx=(4, 20))

        ctk.CTkLabel(
            info_frame, text="Estabelecimento:",
            font=ctk.CTkFont(size=11), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left")
        ctk.CTkLabel(
            info_frame, text=self.ponto.get("estabelecimento", "") or "",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(side="left", padx=(4, 0))

        # Campos editaveis
        campos = {
            "Endereço": "endereco",
            "Email": "email",
            "Telefone": "telefone",
            "Proprietário": "proprietario",
        }
        self.entries = {}

        for campo, db_key in campos.items():
            lbl = ctk.CTkLabel(
                card, text=campo,
                font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
                anchor="w"
            )
            lbl.pack(fill="x", padx=55, pady=(0, 3))
            entry = ctk.CTkEntry(
                card, height=38,
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=10, font=ctk.CTkFont(size=13), border_width=1
            )
            entry.pack(fill="x", padx=55, pady=(0, 8))
            entry.insert(0, self.ponto.get(db_key, "") or "")
            self.entries[campo] = entry

        # Horarios
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(8, 10))

        ctk.CTkLabel(
            card, text="Horário de Funcionamento",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=ECOPA_GREEN_DARK,
            anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 8))

        self.chk_vars = {}
        self.entry_abertura = {}
        self.entry_fechamento = {}

        horarios_existentes = PontoController.buscar_horarios(self.idponto)
        horarios_map = {h["dia_semana"]: h for h in horarios_existentes}

        for dia_num, dia_nome in DIAS_SEMANA:
            linha = ctk.CTkFrame(card, fg_color="transparent")
            linha.pack(fill="x", padx=55, pady=1)

            var = ctk.BooleanVar(value=(dia_num in horarios_map and horarios_map[dia_num].get("ativo", 1) == 1))
            chk = ctk.CTkCheckBox(
                linha, text=dia_nome, variable=var, width=55,
                fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT
            )
            chk.pack(side="left")

            ctk.CTkLabel(linha, text="Abre:", width=38, font=ctk.CTkFont(size=11),
                         text_color=ECOPA_TEXT_LIGHT).pack(side="left", padx=(8, 0))
            ent_a = ctk.CTkEntry(
                linha, width=68, placeholder_text="08:00",
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=8, font=ctk.CTkFont(size=11), border_width=1
            )
            ent_a.pack(side="left", padx=(0, 5))

            ctk.CTkLabel(linha, text="Fecha:", width=42, font=ctk.CTkFont(size=11),
                         text_color=ECOPA_TEXT_LIGHT).pack(side="left")
            ent_f = ctk.CTkEntry(
                linha, width=68, placeholder_text="17:00",
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=8, font=ctk.CTkFont(size=11), border_width=1
            )
            ent_f.pack(side="left")

            self.chk_vars[dia_num] = var
            self.entry_abertura[dia_num] = ent_a
            self.entry_fechamento[dia_num] = ent_f

            # Preencher valores existentes
            if dia_num in horarios_map:
                h = horarios_map[dia_num]
                ent_a.delete(0, ctk.END)
                ent_a.insert(0, str(h["abertura"]))
                ent_f.delete(0, ctk.END)
                ent_f.insert(0, str(h["fechamento"]))

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(16, 24))

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_salvar
        ).pack(side="right", padx=8)

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left", padx=8)

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
