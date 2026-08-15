import customtkinter as ctk
from tkinter import messagebox
from controllers.ponto_controller import PontoController
from utils.horas import DIAS_SEMANA, validar_hora, formatar_hora
from utils.theme import font, font_small, font_small_bold, ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE


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

        # Card principal
        card = ctk.CTkFrame(
            self.content, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER
        )
        card.pack(fill="x", padx=40, pady=(25, 20))

        # Header
        ctk.CTkLabel(
            card, text="📍",
            font=font(36), text_color=ECOPA_GREEN
        ).pack(pady=(28, 0))

        ctk.CTkLabel(
            card, text="Editar Ponto de Coleta",
            font=font(22, "bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(8, 0))

        # Separador
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(16, 12))

        # Info read-only
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=55, pady=(0, 8))

        ctk.CTkLabel(
            info_frame, text="ID:",
            font=font_small(11), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left")
        ctk.CTkLabel(
            info_frame, text=str(self.ponto.get("id_ponto", "")),
            font=font_small_bold(12), text_color=ECOPA_TEXT
        ).pack(side="left", padx=(4, 20))

        ctk.CTkLabel(
            info_frame, text="Estabelecimento:",
            font=font_small(11), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left")
        ctk.CTkLabel(
            info_frame, text=self.ponto.get("estabelecimento", "") or "",
            font=font_small_bold(12), text_color=ECOPA_GREEN_DARK
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
                font=font_small_bold(12), text_color=ECOPA_TEXT,
                anchor="w"
            )
            lbl.pack(fill="x", padx=55, pady=(0, 3))
            entry = ctk.CTkEntry(
                card, height=38,
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=10, font=font(13), border_width=1
            )
            entry.pack(fill="x", padx=55, pady=(0, 8))
            entry.insert(0, self.ponto.get(db_key, "") or "")
            self.entries[db_key] = entry

        # Horarios
        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(8, 10))

        ctk.CTkLabel(
            card, text="Horário de Funcionamento",
            font=font(14, "bold"), text_color=ECOPA_GREEN_DARK,
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

            ctk.CTkLabel(linha, text="Abre:", width=38, font=font_small(11),
                         text_color=ECOPA_TEXT_LIGHT).pack(side="left", padx=(8, 0))
            ent_a = ctk.CTkEntry(
                linha, width=68, placeholder_text="08:00",
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=8, font=font_small(11), border_width=1
            )
            ent_a.pack(side="left", padx=(0, 5))

            ctk.CTkLabel(linha, text="Fecha:", width=42, font=font_small(11),
                         text_color=ECOPA_TEXT_LIGHT).pack(side="left")
            ent_f = ctk.CTkEntry(
                linha, width=68, placeholder_text="17:00",
                fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
                corner_radius=8, font=font_small(11), border_width=1
            )
            ent_f.pack(side="left")

            self.chk_vars[dia_num] = var
            self.entry_abertura[dia_num] = ent_a
            self.entry_fechamento[dia_num] = ent_f

            # Preencher valores existentes
            if dia_num in horarios_map:
                h = horarios_map[dia_num]
                ent_a.delete(0, ctk.END)
                ent_a.insert(0, formatar_hora(h["abertura"]))
                ent_f.delete(0, ctk.END)
                ent_f.insert(0, formatar_hora(h["fechamento"]))

            def _copiar_hora_anterior(dn=dia_num, v=var, ea=ent_a, ef=ent_f):
                if not v.get():
                    return
                if ea.get().strip() and ef.get().strip():
                    return
                for prev_dnum, _ in reversed(DIAS_SEMANA):
                    if prev_dnum >= dn:
                        continue
                    if prev_dnum in self.chk_vars and self.chk_vars[prev_dnum].get():
                        prev_a = self.entry_abertura[prev_dnum].get().strip()
                        prev_f = self.entry_fechamento[prev_dnum].get().strip()
                        if prev_a and prev_f:
                            if not ea.get().strip():
                                ea.delete(0, ctk.END)
                                ea.insert(0, prev_a)
                            if not ef.get().strip():
                                ef.delete(0, ctk.END)
                                ef.insert(0, prev_f)
                            return

            var.trace_add("write", lambda *args, dn=dia_num, v=var, ea=ent_a, ef=ent_f: _copiar_hora_anterior(dn, v, ea, ef))

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(16, 24))

        ctk.CTkButton(
            btn_frame, text="Salvar", width=140, height=40,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font(13, "bold"),
            command=self._on_salvar
        ).pack(side="right", padx=8)

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=40,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=font(13, "bold"),
            command=self.on_voltar
        ).pack(side="left", padx=8)

    def _on_salvar(self):
        dados = {campo: entry.get().strip() for campo, entry in self.entries.items()}

        horarios = []
        erros_hora = []
        for dia_num, dia_nome in DIAS_SEMANA:
            if self.chk_vars[dia_num].get():
                abertura = self.entry_abertura[dia_num].get().strip()
                fechamento = self.entry_fechamento[dia_num].get().strip()
                for campo, valor in [("abertura", abertura), ("fechamento", fechamento)]:
                    if valor and not validar_hora(valor):
                        erros_hora.append(f"{dia_nome} {campo}: '{valor}'")
                horarios.append({
                    "dia_semana": dia_num,
                    "abertura": abertura,
                    "fechamento": fechamento,
                    "ativo": 1,
                })
        if erros_hora:
            messagebox.showerror(
                "Erro",
                "Horários inválidos (use HH:MM, ex: 08:00, 17:30):\n\n" +
                "\n".join(erros_hora))
            return

        ok, msg = PontoController.atualizar(self.idponto, dados, horarios=horarios if horarios else None)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.on_voltar()
        else:
            messagebox.showerror("Erro", msg)
