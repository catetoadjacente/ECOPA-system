import customtkinter as ctk
import threading
import queue
from utils.theme import font, ECOPA_GREEN, ECOPA_GREEN_LIGHT


class LoadingOverlay(ctk.CTkFrame):
    """Overlay de carregamento reutilizavel."""

    def __init__(self, master, text="Carregando..."):
        super().__init__(master, fg_color="#ffffff", corner_radius=0)
        self._animando = False
        self._frames = []
        self._idx = 0

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        self._label_texto = ctk.CTkLabel(
            container, text=text,
            font=font(14, "bold"),
            text_color=ECOPA_GREEN
        )
        self._label_texto.pack(pady=(0, 16))

        dots_frame = ctk.CTkFrame(container, fg_color="transparent")
        dots_frame.pack()

        for i in range(3):
            dot = ctk.CTkFrame(
                dots_frame, width=12, height=12,
                corner_radius=6, fg_color=ECOPA_GREEN_LIGHT
            )
            dot.pack(side="left", padx=6)
            self._frames.append(dot)

    def start(self):
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
        for i, frame in enumerate(self._frames):
            if i == self._idx:
                frame.configure(fg_color=ECOPA_GREEN, width=16, height=16)
            else:
                frame.configure(fg_color=ECOPA_GREEN_LIGHT, width=12, height=12)
        self._idx = (self._idx + 1) % 3
        try:
            self.after(400, self._animar)
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
