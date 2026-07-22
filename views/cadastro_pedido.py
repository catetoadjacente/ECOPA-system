import customtkinter as ctk
from tkinter import messagebox
from controllers.pedido_controller import PedidoController
from controllers.destinacao_controller import DestinacaoController
from models.lote import Lote

ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"


class CadastroPedido(ctk.CTkFrame):
    def __init__(self, master, content, on_voltar):
        super().__init__(master)
        self.content = content
        self.on_voltar = on_voltar
        self.montar_formulario()

    def montar_formulario(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=ECOPA_BG)
        scroll.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            scroll, fg_color=ECOPA_WHITE, corner_radius=20,
            border_width=1, border_color=ECOPA_BORDER)
        card.pack(fill="x", padx=40, pady=(25, 20))

        ctk.CTkLabel(card, text="Novo Pedido",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ECOPA_GREEN_DARK
        ).pack(pady=(28, 0))

        ctk.CTkLabel(card, text="Solicitar material para destino",
            font=ctk.CTkFont(size=12), text_color=ECOPA_TEXT_LIGHT
        ).pack(pady=(0, 16))

        ctk.CTkFrame(card, fg_color=ECOPA_BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

        ctk.CTkLabel(card, text="Dados do Pedido",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=ECOPA_GREEN_DARK, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 10))

        # Destinacao
        ctk.CTkLabel(card, text="Destinacao",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))

        destinacoes = DestinacaoController.listar()
        self.destinacoes_lista = destinacoes
        self.nomes_lista = [f"{d['nome']} ({d['tipo']})" for d in destinacoes] if destinacoes else ["Nenhuma destinacao cadastrada"]

        self.combo_dest = ctk.CTkComboBox(
            card, values=self.nomes_lista, height=38, font=ctk.CTkFont(size=13), state="readonly",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            button_color=ECOPA_GREEN, button_hover_color=ECOPA_GREEN_LIGHT, corner_radius=10)
        if self.nomes_lista and self.nomes_lista[0] != "Nenhuma destinacao cadastrada":
            self.combo_dest.set(self.nomes_lista[0])
        self.combo_dest.pack(fill="x", padx=55, pady=(0, 12))

        # Quantidade
        ctk.CTkLabel(card, text="Quantidade solicitada (Kg)",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.entry_quantidade = ctk.CTkEntry(
            card, height=38, placeholder_text="Ex: 500.0",
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER,
            corner_radius=10, font=ctk.CTkFont(size=13), border_width=1)
        self.entry_quantidade.pack(fill="x", padx=55, pady=(0, 12))

        # Estoque disponivel
        lotes = Lote.listar_disponiveis()
        estoque_total = sum(float(l["quantidade_restante"]) for l in lotes)
        ctk.CTkLabel(card, text=f"Estoque disponivel: {estoque_total:.1f} Kg",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_GREEN, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 12))

        # Observacao
        ctk.CTkLabel(card, text="Observacao",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT, anchor="w"
        ).pack(fill="x", padx=55, pady=(0, 3))
        self.text_obs = ctk.CTkTextbox(
            card, height=80, font=ctk.CTkFont(size=13),
            fg_color=ECOPA_BG, border_color=ECOPA_BORDER, corner_radius=10, border_width=1)
        self.text_obs.pack(fill="x", padx=55, pady=(0, 16))

        # Botoes
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=55, pady=(5, 25))

        ctk.CTkButton(
            btn_frame, text="Voltar", width=140, height=42,
            fg_color="#7f8c8d", hover_color="#95a5a6",
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_voltar
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Criar Pedido", width=140, height=42,
            fg_color=ECOPA_GREEN, hover_color=ECOPA_GREEN_LIGHT,
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._salvar
        ).pack(side="right")

    def _salvar(self):
        valor_selecionado = self.combo_dest.get()
        idx = -1
        for i, nome in enumerate(self.nomes_lista):
            if nome == valor_selecionado:
                idx = i
                break

        if idx < 0 or idx >= len(self.destinacoes_lista):
            messagebox.showerror("Erro", "Selecione uma destinacao!")
            return

        quantidade = self.entry_quantidade.get().strip()
        if not quantidade:
            messagebox.showerror("Erro", "Preencha a quantidade!")
            return

        try:
            quantidade = float(quantidade)
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade invalida!")
            return

        observacao = self.text_obs.get("1.0", "end-1c").strip()

        dados = {
            "id_destinacao": self.destinacoes_lista[idx]["id"],
            "quantidade_solicitada": quantidade,
            "observacao": observacao,
        }

        ok, msg, pedido_id = PedidoController.cadastrar(dados)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            from views.distribuicao_estoque import DistribuicaoEstoque
            DistribuicaoEstoque(self, self.content, pedido_id, on_voltar=self.on_voltar)
        else:
            messagebox.showerror("Erro", msg)
