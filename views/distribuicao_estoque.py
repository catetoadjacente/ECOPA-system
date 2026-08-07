import customtkinter as ctk
from tkinter import messagebox
from controllers.pedido_controller import PedidoController
from controllers.lote_controller import LoteController
from utils.theme import font, font_small, font_small_bold
from views.loading import LoadingOverlay, carregar_em_bg

ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"
ECOPA_ORANGE = "#f39c12"
ECOPA_LEAF = "#27ae60"
ECOPA_BLUE = "#3498db"


class DistribuicaoEstoque(ctk.CTkFrame):
    def __init__(self, master, content, id_pedido, on_voltar):
        super().__init__(master)
        self.content = content
        self.id_pedido = id_pedido
        self.on_voltar = on_voltar
        self.pedido = PedidoController.obter_por_id(id_pedido)
        if not self.pedido:
            messagebox.showerror("Erro", "Pedido nao encontrado!")
            self.on_voltar()
            return
        self.estoque_total = 0
        self.lotes_alocados = []
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(container, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text=f"Distribuir Estoque - Pedido #{self.id_pedido}",
            font=font(26, "bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Confirme a distribuicao deste pedido",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(scroll, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0))

        # Card de info do pedido
        info_card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        info_card.pack(fill="x", padx=32, pady=(20, 0))

        ctk.CTkLabel(info_card, text=f"Destino: {self.pedido['destinacao']}",
            font=font(14, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(14, 4))

        ctk.CTkLabel(info_card,
            text=f"Tipo: {self.pedido.get('tipo_destinacao', '-')}",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(fill="x", padx=20, pady=(0, 10))

        # Valores
        solicitada = float(self.pedido["quantidade_solicitada"])
        atendida = float(self.pedido["quantidade_atendida"])
        falta = solicitada - atendida

        valores_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        valores_frame.pack(fill="x", padx=20, pady=(0, 14))
        valores_frame.grid_columnconfigure(0, weight=1)
        valores_frame.grid_columnconfigure(1, weight=1)
        valores_frame.grid_columnconfigure(2, weight=1)

        self._criar_info_valor(valores_frame, "Solicitado", f"{solicitada:.1f} Kg", 0, 0)
        self._criar_info_valor(valores_frame, "Ja Atendido", f"{atendida:.1f} Kg", 0, 1)
        self._criar_info_valor(valores_frame, "Falta", f"{falta:.1f} Kg", 0, 2, destaque=falta > 0)

        # Card de lotes que serao utilizados
        self._lotes_card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER)
        self._lotes_card.pack(fill="x", padx=32, pady=(16, 0))

        ctk.CTkLabel(self._lotes_card, text="Lotes que serao utilizados",
            font=font(15, "bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 4))

        self._lotes_container = ctk.CTkFrame(self._lotes_card, fg_color="transparent")
        self._lotes_container.pack(fill="x", padx=16, pady=(0, 8))

        overlay = LoadingOverlay(self._lotes_container, text="Calculando distribuicao...")
        overlay.start()

        def _carregar_lotes():
            lotes = LoteController.listar_disponiveis()
            total_estoque = sum(float(l["quantidade_restante"]) for l in lotes)

            solicitada = float(self.pedido["quantidade_solicitada"])
            atendida = float(self.pedido["quantidade_atendida"])
            falta = solicitada - atendida

            parciais = [l for l in lotes if l["status"] == "Parcialmente Consumido"]
            novos = [l for l in lotes if l["status"] != "Parcialmente Consumido"]
            parciais.sort(key=lambda l: l["data_criacao"])
            novos.sort(key=lambda l: l["data_criacao"])
            lotes_ordenados = parciais + novos

            alocados = []
            restante = falta
            for lote in lotes_ordenados:
                if restante <= 0:
                    break
                disp = float(lote["quantidade_restante"])
                if disp <= 0:
                    continue
                qtd = min(disp, restante)
                alocados.append({
                    "id": lote["id"],
                    "ponto": lote["ponto"],
                    "data": lote["data_criacao"],
                    "status": lote["status"],
                    "disponivel": disp,
                    "alocado": qtd,
                })
                restante -= qtd

            return {"total_estoque": total_estoque, "alocados": alocados, "falta": falta}

        def _mostrar_lotes(dados):
            overlay.stop()
            overlay.destroy()
            self.estoque_total = dados["total_estoque"]
            self.lotes_alocados = dados["alocados"]
            falta = dados["falta"]

            if not self.lotes_alocados:
                ctk.CTkLabel(self._lotes_container,
                    text="Nenhum lote disponivel no estoque",
                    font=font(13), text_color=ECOPA_TEXT_LIGHT
                ).pack(pady=20)
                return

            # Cabecalho verde
            header_frame = ctk.CTkFrame(self._lotes_container, fg_color=ECOPA_GREEN, corner_radius=8)
            header_frame.pack(fill="x", pady=(0, 4))

            cabecalhos = ["Lote", "Fonte", "Data", "Status", "Disponivel", "Sera Retirado"]
            larguras = [60, 160, 90, 80, 90, 110]
            for col, texto in enumerate(cabecalhos):
                ctk.CTkLabel(
                    header_frame, text=texto,
                    font=font_small_bold(12),
                    text_color=ECOPA_WHITE, width=larguras[col]
                ).grid(row=0, column=col, padx=8, pady=8, sticky="w")

            total_alocado = 0
            for lote in self.lotes_alocados:
                row = ctk.CTkFrame(self._lotes_container, fg_color="transparent")
                row.pack(fill="x", pady=2)

                data = lote["data"]
                if hasattr(data, "strftime"):
                    data_str = data.strftime("%d/%m/%Y")
                elif data:
                    data_str = str(data)[:10]
                else:
                    data_str = ""

                status = lote.get("status", "")
                status_cor = ECOPA_ORANGE if status == "Parcialmente Consumido" else ECOPA_GREEN

                ctk.CTkLabel(row, text=f"#{lote['id']}",
                    font=font_small(12), text_color=ECOPA_TEXT,
                    width=larguras[0], anchor="w").grid(row=0, column=0, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=lote["ponto"],
                    font=font_small(12), text_color=ECOPA_TEXT,
                    width=larguras[1], anchor="w").grid(row=0, column=1, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=data_str,
                    font=font_small(12), text_color=ECOPA_TEXT,
                    width=larguras[2], anchor="w").grid(row=0, column=2, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=status,
                    font=font_small(11), text_color=status_cor,
                    width=larguras[3], anchor="w").grid(row=0, column=3, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=f"{lote['disponivel']:.1f} Kg",
                    font=font_small(12), text_color=ECOPA_TEXT_LIGHT,
                    width=larguras[4], anchor="w").grid(row=0, column=4, padx=8, pady=4, sticky="w")
                ctk.CTkLabel(row, text=f"{lote['alocado']:.1f} Kg",
                    font=font(12, "bold"), text_color=ECOPA_GREEN,
                    width=larguras[5], anchor="w").grid(row=0, column=5, padx=8, pady=4, sticky="w")

                total_alocado += lote["alocado"]

            # Total
            total_frame = ctk.CTkFrame(self._lotes_container, fg_color="transparent")
            total_frame.pack(fill="x", pady=(8, 0))

            ctk.CTkFrame(total_frame, fg_color=ECOPA_GREEN, height=2, corner_radius=1).pack(fill="x")

            ctk.CTkLabel(total_frame,
                text=f"Total a distribuir: {total_alocado:.1f} Kg",
                font=font(14, "bold"), text_color=ECOPA_GREEN_DARK, anchor="e"
            ).pack(fill="x", pady=(8, 0))

            if total_alocado < falta:
                ctk.CTkLabel(total_frame,
                    text=f"Estoque insuficiente (faltam {falta - total_alocado:.1f} Kg)",
                    font=font_small(12), text_color=ECOPA_ORANGE, anchor="e"
                ).pack(fill="x")

        def _erro_lotes(msg):
            overlay.stop()
            overlay.destroy()
            ctk.CTkLabel(self._lotes_container,
                text=f"Erro ao carregar lotes: {msg}",
                font=font(13), text_color="#e74c3c"
            ).pack(pady=20)

        carregar_em_bg(self._lotes_container, _carregar_lotes, _mostrar_lotes, callback_erro=_erro_lotes)

        # Botoes
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(fill="x", padx=32, pady=(24, 20))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=42,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=font(13, "bold"),
            command=self.on_voltar
        ).pack(side="left")

        self._btn_confirmar = ctk.CTkButton(
            btn_frame, text="Confirmar Distribuicao", width=220, height=42,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font(13, "bold"),
            command=self._confirmar
        )
        self._btn_confirmar.pack(side="right")

    def _criar_info_valor(self, parent, titulo, valor, row, col, destaque=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, sticky="w", padx=(0, 20))

        ctk.CTkLabel(frame, text=titulo,
            font=font_small(11), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w")

        cor = ECOPA_ORANGE if destaque else ECOPA_GREEN_DARK
        ctk.CTkLabel(frame, text=valor,
            font=font(16, "bold"), text_color=cor, anchor="w"
        ).pack(anchor="w")

    def _confirmar(self):
        solicitada = float(self.pedido["quantidade_solicitada"])
        atendida = float(self.pedido["quantidade_atendida"])
        falta = solicitada - atendida

        if falta <= 0:
            messagebox.showinfo("Aviso", "Este pedido ja foi totalmente atendido!")
            return

        if not self.lotes_alocados:
            messagebox.showwarning("Aviso", "Nenhum lote disponivel no estoque!")
            return

        total_alocado = sum(l["alocado"] for l in self.lotes_alocados)

        if total_alocado < falta:
            resposta = messagebox.askyesno(
                "Estoque Insuficiente",
                f"O estoque distribuido ({total_alocado:.1f} Kg) e menor "
                f"que o necessario ({falta:.1f} Kg).\n\n"
                f"Deseja distribuir apenas o disponivel?"
            )
            if not resposta:
                return
        else:
            resposta = messagebox.askyesno(
                "Confirmar Distribuicao",
                f"Distribuir {total_alocado:.1f} Kg de {len(self.lotes_alocados)} lote(s) "
                f"para {self.pedido['destinacao']}?"
            )
            if not resposta:
                return

        self._btn_confirmar.configure(state="disabled", text="Distribuindo...")

        def _distribuir():
            return PedidoController.distribuir_automatico(self.id_pedido)

        def _resultado(dado):
            ok, msg = dado
            self._btn_confirmar.configure(state="normal", text="Confirmar Distribuicao")
            if ok:
                messagebox.showinfo("Sucesso", msg)
                self.on_voltar()
            else:
                messagebox.showerror("Erro", msg)

        def _erro_distribuir(msg):
            self._btn_confirmar.configure(state="normal", text="Confirmar Distribuicao")
            messagebox.showerror("Erro", f"Falha ao distribuir: {msg}")

        carregar_em_bg(self, _distribuir, _resultado, callback_erro=_erro_distribuir)
