import customtkinter as ctk
from PIL import Image
import os
import threading
from controllers.gerente_controller import GerenteController
from views.dashboard import MainView
from views.loading import LoadingOverlay
from tkinter import messagebox
import pywinstyles
from utils.theme import font
from utils.sessao import iniciar


ctk.set_appearance_mode("light")

BG_IMAGE = r"fundo_login.png"
IMG_W, IMG_H = 1280, 832


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECOPA System")
        self.geometry(f"{IMG_W}x{IMG_H}")
        self.after(0, lambda: self.state("zoomed"))

        self._pil_image = None
        self.bg_photo = None
        self._resize_after_id = None
        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", BG_IMAGE)
        if os.path.exists(img_path):
            self._pil_image = Image.open(img_path)
        else:
            self._pil_image = None

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._update_bg_image()
        self.bind("<Configure>", self._on_resize)

        self.entry_user = ctk.CTkEntry(
            self,
            fg_color="white",
            text_color="black",
            border_width=0,
            bg_color="#ffffff",
            height=35,
            font=font(14),
        )
        self.entry_user.place(relx=0.762, rely=0.39, anchor="center", relwidth=0.34)

        self.entry_pass = ctk.CTkEntry(
            self,
            fg_color="white",
            text_color="black",
            border_width=0,
            bg_color="#ffffff",
            show="*",
            height=35,
            font=font(14),
        )
        self.entry_pass.place(relx=0.762, rely=0.545, anchor="center", relwidth=0.34)
        self.bind("<Return>", self._on_login)

        self.btn_login = ctk.CTkButton(
            self,
            text="Login",
            fg_color="#DDEEDD",
            bg_color="#000001",
            border_width=0,
            hover_color="#205b59",
            height=41,
            corner_radius=20,
            text_color="black",
            font=font(14, "bold"),
            command=self._on_login,
            hover=True
            
        )
        pywinstyles.set_opacity(self.btn_login, color="#000001")
        self.btn_login.place(relx=0.775, rely=0.65, anchor="center", relwidth=0.15)

    def _on_login(self, event=None):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get()

        if not user:
            messagebox.showwarning("Aviso", "Digite o nome de usuário.")
            return

        self.btn_login.configure(state="disabled")
        self.loading = LoadingOverlay(self, text="Autenticando...")
        self.loading.start()

        def _autenticar():
            try:
                info, erro = GerenteController.login(user, password)
            except Exception as e:
                info, erro = None, str(e)
            self.after(0, lambda: _resultado_login(info, erro))

        def _resultado_login(info, erro):
            self.loading.stop()
            self.btn_login.configure(state="normal")
            if erro:
                messagebox.showerror("Erro", erro)
                self.entry_pass.delete(0, ctk.END)
                return
            self.entry_user.destroy()
            self.entry_pass.destroy()
            self.btn_login.destroy()
            self.bg_label.destroy()
            self.unbind("<Configure>")

            iniciar(info)
            dashboard = MainView(self, nome_usuario=info['nome'])
            dashboard.pack(fill="both", expand=True)
            self.title(f"ECOPA System - {info['nome']}")

        threading.Thread(target=_autenticar, daemon=True).start()

    def _on_resize(self, event):
        if event.widget is self:
            # Debounce: cancela resize anterior e agenda novo em 50ms
            if self._resize_after_id is not None:
                self.after_cancel(self._resize_after_id)
            self._resize_after_id = self.after(50, self._update_bg_image)

    def _update_bg_image(self):
        if self._pil_image is None:
            return
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            return
        resized = self._pil_image.resize((w, h), Image.BILINEAR)
        self.bg_photo = ctk.CTkImage(resized, size=(w, h))
        self.bg_label.configure(image=self.bg_photo)


if __name__ == "__main__":
    app = App()
    app.mainloop()
