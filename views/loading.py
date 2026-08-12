import customtkinter as ctk
import threading
import queue
from utils.theme import (
    ECOPA_GREEN,
    ECOPA_GREEN_LIGHT,
)


class LoadingOverlay(ctk.CTkFrame):
    """Overlay de carregamento reutilizável."""

    def __init__(self, master, text="Carregando..."):
        super().__init__(master, fg_color="#ffffff", corner_radius=0)
        self._animando = False
        self._progresso = 0.0

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        self._label_texto = ctk.CTkLabel(
            container,
            text=text,
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            text_color=ECOPA_GREEN,
        )
        self._label_texto.pack(pady=(0, 16))

        self._barra = ctk.CTkProgressBar(
            container,
            width=190,
            height=7,
            corner_radius=4,
            fg_color="#E3F1E6",
            progress_color=ECOPA_GREEN_LIGHT,
        )
        self._barra.pack()
        self._barra.set(0)

    def start(self):
        if self._animando:
            return
        self._animando = True
        self.lift()
        self.pack(fill="both", expand=True)
        self._animar()

    def stop(self):
        self._animando = False
        try:
            if self.winfo_exists():
                self.pack_forget()
        except Exception:
            pass

    def _animar(self):
        if not self._animando:
            return
        try:
            if not self.winfo_exists():
                self._animando = False
                return
        except Exception:
            self._animando = False
            return
        self._progresso += 0.018
        if self._progresso > 1:
            self._progresso = 0
        self._barra.set(self._progresso)
        try:
            self.after(28, self._animar)
        except Exception:
            self._animando = False


def executar_com_loading(parent, funcao_dados, callback_sucesso, texto="Carregando..."):
    """Executa uma funcao de dados em background com loading visual."""
    overlay = LoadingOverlay(parent, text=texto)

    def _tarefa():
        try:
            dados = funcao_dados()
            parent.after(0, lambda: _finalizar(dados))
        except Exception as e:
            parent.after(0, lambda: _erro(str(e)))

    def _finalizar(dados):
        overlay.stop()
        callback_sucesso(dados)

    def _erro(msg):
        overlay.stop()
        from tkinter import messagebox
        messagebox.showerror("Erro", f"Falha ao carregar dados:\n{msg}")

    overlay.start()
    threading.Thread(target=_tarefa, daemon=True).start()


def carregar_em_bg(parent, funcao_dados, callback_sucesso, callback_erro=None):
    """Carrega dados em background usando queue + polling (thread-safe).

    - parent: widget pai (vivo durante a operação)
    - funcao_dados: callable que retorna dados
    - callback_sucesso: chamado na main thread com os dados
    - callback_erro: chamado na main thread com a mensagem de erro (opcional)
    """
    fila = queue.Queue()

    def _tarefa():
        try:
            dados = funcao_dados()
            fila.put(("ok", dados))
        except Exception as e:
            fila.put(("erro", str(e)))

    def _poll():
        try:
            if not parent.winfo_exists():
                return
            status, payload = fila.get_nowait()
        except queue.Empty:
            try:
                parent.after(100, _poll)
            except Exception:
                pass
            return
        except Exception:
            return
        if status == "ok":
            callback_sucesso(payload)
        else:
            if callback_erro:
                callback_erro(payload)
            else:
                from tkinter import messagebox
                messagebox.showerror("Erro", f"Falha ao carregar dados:\n{payload}")

    threading.Thread(target=_tarefa, daemon=True).start()
    try:
        parent.after(100, _poll)
    except Exception:
        pass
