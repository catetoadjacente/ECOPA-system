import customtkinter as ctk
from tkinter import messagebox
from controllers.coleta_controller import ColetaController
from views.loading import LoadingOverlay
import threading
import queue
from utils.theme import font, font_small, font_small_bold, ECOPA_GREEN, ECOPA_GREEN_LIGHT, ECOPA_GREEN_DARK, ECOPA_BG, ECOPA_WHITE, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_BORDER, ECOPA_ORANGE, ECOPA_LEAF
from utils.widgets import TabelaPaginada, toast


class ColetasView(ctk.CTkFrame):
    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self.montar_tela()

    def montar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Container principal
        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="Coletas",
            font=font(30, "bold"), anchor="w",
            text_color=ECOPA_GREEN_DARK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Gerencia todas as coletas do sistema",
            font=font_small(12), text_color=ECOPA_TEXT_LIGHT, anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Linha verde
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(
            fill="x", padx=32, pady=(16, 0)
        )

        # Card de filtros
        card_filtros = ctk.CTkFrame(
            container, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        card_filtros.pack(fill="x", padx=32, pady=(20, 0))

        ctk.CTkLabel(
            card_filtros, text="🔍 Filtros",
            font=font(13, "bold"), text_color=ECOPA_TEXT,
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(14, 8))

        filtros = ctk.CTkFrame(card_filtros, fg_color="transparent")
        filtros.pack(fill="x", padx=20, pady=(0, 14))

        ctk.CTkLabel(
            filtros, text="Status:", font=font_small(12), text_color=ECOPA_TEXT_LIGHT
        ).pack(side="left", padx=(0, 8))

        filtro_status = ctk.CTkComboBox(
            filtros, values=["TODOS", "Pendente", "Realizada"],
            width=160, height=36, corner_radius=10,
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT,
            command=self._filtrar
        )
        filtro_status.pack(side="left")
        filtro_status.set("TODOS")
        self.filtro_status = filtro_status

        btn_limpar = ctk.CTkButton(
            filtros, text="Limpar Filtros", width=130, height=36,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=font_small_bold(12),
            command=self.montar_tela
        )
        btn_limpar.pack(side="right")

        self._montar_tabela()

    def _montar_tabela(self, filtro=None):
        for widget in self.content.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, '_is_tabela'):
                widget.destroy()

        frame_tabela = ctk.CTkFrame(
            self.content, fg_color=ECOPA_WHITE, corner_radius=16,
            border_width=1, border_color=ECOPA_BORDER
        )
        frame_tabela._is_tabela = True
        frame_tabela.pack(fill="both", expand=True, padx=32, pady=(20, 20))

        colunas = ["ID", "Ponto", "Observação", "Quantidade", "Data", "Status", "Ações"]
        relx = [0.01, 0.06, 0.20, 0.38, 0.50, 0.60, 0.72]

        def _render_row(frame, item, rlx):
            valores = [item["id_str"], item["ponto"], item["observacao"], item["qtd"], item["data"]]
            for i, v in enumerate(valores):
                ctk.CTkLabel(frame, text=v, font=font_small(12),
                             text_color=ECOPA_TEXT, anchor="w").place(relx=rlx[i], rely=0.5, anchor="w")

            badge_cor = ECOPA_LEAF if item["status"] == "Realizada" else ECOPA_ORANGE
            badge_bg = "#e8f8e8" if item["status"] == "Realizada" else "#fdf5e8"
            ctk.CTkLabel(frame, text=item["status"], font=font_small_bold(11),
                         fg_color=badge_bg, text_color=badge_cor,
                         corner_radius=8, height=26).place(relx=rlx[5], rely=0.5, anchor="w")

            if item["status"] == "Pendente":
                id_coleta = item["id_num"]
                ctk.CTkButton(frame, text="Realizar", width=80, height=28,
                               fg_color=ECOPA_LEAF, hover_color="#2ecc71",
                               corner_radius=8, font=font_small_bold(11),
                               command=lambda idc=id_coleta: self._marcar_realizada(idc)).place(relx=rlx[6], rely=0.5, anchor="w")

        self._tabela = TabelaPaginada(frame_tabela, colunas=colunas, relx=relx, on_render=_render_row)
        self._tabela.pack(fill="both", expand=True)

        overlay = LoadingOverlay(frame_tabela, text="Carregando coletas...")
        overlay.start()

        fila = queue.Queue()

        def _carregar_dados():
            try:
                dados = ColetaController.listar()
                fila.put(("ok", dados))
            except Exception as e:
                fila.put(("erro", str(e)))

        def _poll():
            try:
                if not frame_tabela.winfo_exists():
                    return
                status, payload = fila.get_nowait()
            except queue.Empty:
                try:
                    frame_tabela.after(100, _poll)
                except Exception:
                    pass
                return
            except Exception:
                return

            overlay.stop()
            if status == "erro":
                toast(f"Falha ao carregar coletas:\n{payload}", tipo="error")
                return

            dados = payload
            if filtro and filtro != "TODOS":
                dados = [c for c in dados if c["status"] == filtro]

            if not dados:
                ctk.CTkLabel(frame_tabela, text="Nenhuma coleta encontrada",
                             font=font(13), text_color=ECOPA_TEXT_LIGHT).pack(pady=40)
                return

            items = []
            for c in dados:
                items.append({
                    "id_num": c["id"],
                    "id_str": f"#{int(c['id'])}",
                    "ponto": c["ponto"],
                    "observacao": c["observacao"],
                    "qtd": f"{float(c['quantidade']):.1f} Kg" if c["quantidade"] else "",
                    "data": c["data_coleta"].strftime("%d/%m/%Y") if c["data_coleta"] else "",
                    "status": c["status"],
                })

            self._tabela.carregar(items)

        threading.Thread(target=_carregar_dados, daemon=True).start()
        try:
            frame_tabela.after(100, _poll)
        except Exception:
            pass

    def _filtrar(self, valor):
        self._montar_tabela(filtro=valor)

    def _marcar_realizada(self, id_coleta):
        if messagebox.askyesno("Confirmar", "Marcar esta coleta como realizada?"):
            if ColetaController.atualizar_status(id_coleta, "Realizada"):
                self.montar_tela()
            else:
                toast("Falha ao atualizar status!", tipo="error")
