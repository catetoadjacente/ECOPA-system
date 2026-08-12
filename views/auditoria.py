import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from models.auditoria import Auditoria
from utils.theme import ECOPA_BG, ECOPA_BORDER, ECOPA_GREEN, ECOPA_GREEN_DARK, ECOPA_GREEN_LIGHT, ECOPA_TEXT, ECOPA_TEXT_LIGHT, ECOPA_WHITE, font, font_small, font_small_bold
from utils.widgets import TabelaPaginada
from views.loading import executar_com_loading


class AuditoriaView(ctk.CTkFrame):
    ACOES = ["TODAS", "CRIAR", "ATUALIZAR", "ATUALIZAR_STATUS", "EXCLUIR", "DESATIVAR", "REATIVAR", "CONSUMIR_ESTOQUE", "DISTRIBUIR_ESTOQUE"]
    ENTIDADES = ["TODAS", "gerente", "ponto_de_coleta", "coleta", "lote", "pedido", "destinacao"]

    def __init__(self, master, content):
        super().__init__(master)
        self.content = content
        self._montar()
        self._carregar()

    def _montar(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        container = ctk.CTkFrame(self.content, fg_color=ECOPA_BG, corner_radius=0)
        container.pack(fill="both", expand=True)
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))
        esquerda = ctk.CTkFrame(header, fg_color="transparent")
        esquerda.pack(side="left")
        ctk.CTkLabel(esquerda, text="Auditoria", font=font(30, "bold"), text_color=ECOPA_GREEN_DARK).pack(anchor="w")
        ctk.CTkLabel(esquerda, text="Histórico das ações realizadas no sistema", font=font_small(12), text_color=ECOPA_TEXT_LIGHT).pack(anchor="w", pady=(2, 0))
        ctk.CTkFrame(container, fg_color=ECOPA_GREEN, height=3, corner_radius=2).pack(fill="x", padx=32, pady=(16, 0))

        filtros = ctk.CTkFrame(container, fg_color=ECOPA_WHITE, corner_radius=16, border_width=1, border_color=ECOPA_BORDER)
        filtros.pack(fill="x", padx=32, pady=(20, 12))
        linha = ctk.CTkFrame(filtros, fg_color="transparent")
        linha.pack(fill="x", padx=20, pady=14)
        self.data_inicio = self._campo(linha, "De (DD/MM/AAAA)", 125)
        self.data_fim = self._campo(linha, "Até (DD/MM/AAAA)", 125)
        self.gerente = self._campo(linha, "Usuário", 150)
        self.acao = self._combo(linha, "Ação", self.ACOES, 170)
        self.entidade = self._combo(linha, "Registro", self.ENTIDADES, 170)
        ctk.CTkButton(linha, text="Filtrar", width=90, height=36, fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT, corner_radius=10, font=font_small_bold(12), command=self._aplicar).pack(side="left", padx=(0, 6), pady=(20, 0))
        ctk.CTkButton(linha, text="Limpar", width=80, height=36, fg_color="transparent", hover_color=ECOPA_BG, border_width=1, border_color=ECOPA_GREEN, text_color=ECOPA_GREEN, corner_radius=10, font=font_small(12), command=self._limpar).pack(side="left", pady=(20, 0))

        self.resumo = ctk.CTkLabel(container, text="Carregando histórico...", font=font_small(12), text_color=ECOPA_TEXT_LIGHT)
        self.resumo.pack(anchor="w", padx=36, pady=(0, 6))
        self.tabela = TabelaPaginada(container, colunas=["Data e hora", "Usuário", "Ação", "Registro", "ID", "Detalhes"], relx=[0.01, 0.20, 0.37, 0.52, 0.68, 0.76], on_render=self._renderizar_linha)
        self.tabela.pack(fill="both", expand=True, padx=32, pady=(0, 20))

    def _campo(self, parent, titulo, largura):
        bloco = ctk.CTkFrame(parent, fg_color="transparent")
        bloco.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(bloco, text=titulo, font=font_small(11), text_color=ECOPA_TEXT_LIGHT).pack(anchor="w")
        campo = ctk.CTkEntry(bloco, width=largura, height=36, corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER)
        campo.pack()
        return campo

    def _combo(self, parent, titulo, valores, largura):
        bloco = ctk.CTkFrame(parent, fg_color="transparent")
        bloco.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(bloco, text=titulo, font=font_small(11), text_color=ECOPA_TEXT_LIGHT).pack(anchor="w")
        combo = ctk.CTkComboBox(bloco, values=valores, width=largura, height=36, corner_radius=10, fg_color=ECOPA_BG, border_color=ECOPA_BORDER, button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT)
        combo.set("TODAS")
        combo.pack()
        return combo

    @staticmethod
    def _data(texto, fim=False):
        if not texto:
            return None
        data = datetime.strptime(texto, "%d/%m/%Y").strftime("%Y-%m-%d")
        return f"{data} 23:59:59" if fim else data

    def _aplicar(self):
        try:
            inicio = self._data(self.data_inicio.get().strip())
            fim = self._data(self.data_fim.get().strip(), fim=True)
        except ValueError:
            messagebox.showwarning("Data inválida", "Use o formato DD/MM/AAAA.")
            return
        if inicio and fim and inicio > fim:
            messagebox.showwarning("Período inválido", "A data inicial deve ser anterior à final.")
            return
        self._carregar(inicio, fim)

    def _limpar(self):
        for campo in (self.data_inicio, self.data_fim, self.gerente):
            campo.delete(0, "end")
        self.acao.set("TODAS")
        self.entidade.set("TODAS")
        self._carregar()

    def _carregar(self, inicio=None, fim=None):
        self.resumo.configure(text="Carregando histórico...")
        executar_com_loading(self.content, lambda: Auditoria.listar(data_inicio=inicio, data_fim=fim, gerente=self.gerente.get().strip() or None, acao=self.acao.get(), entidade=self.entidade.get()), self._exibir, texto="Carregando auditoria...")

    def _exibir(self, registros):
        self.resumo.configure(text=f"{len(registros)} registro(s) encontrado(s) — máximo de 500")
        self.tabela.carregar(registros)

    def _renderizar_linha(self, frame, item, relx):
        data = item["criado_em"]
        data = data.strftime("%d/%m/%Y %H:%M") if hasattr(data, "strftime") else str(data)
        valores = [data, item.get("gerente") or "Usuário removido", item["acao"], item["entidade"], item["registro_id"], item.get("detalhes") or "-"]
        for indice, valor in enumerate(valores):
            ctk.CTkLabel(frame, text=str(valor)[:42], font=font_small(11), text_color=ECOPA_TEXT, anchor="w").place(relx=relx[indice], rely=0.5, anchor="w")
