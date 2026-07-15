import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter
import os
from controllers.gerente_controller import GerenteController
from views.dashboard import MainView
from tkinter import messagebox
import pywinstyles


ctk.set_appearance_mode("light")

BG_IMAGE = r"fundo_login.png"
IMG_W, IMG_H = 1280, 832

# Paleta ECOPA
ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_LEAF = "#27ae60"
ECOPA_BG = "#f0f7f0"
ECOPA_WHITE = "#ffffff"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#555555"
ECOPA_BORDER = "#d0e8d0"
ECOPA_SHADOW = "#004d0e20"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECOPA System")
        self.geometry(f"{IMG_W}x{IMG_H}")
        self.after(0, lambda: self.state("zoomed"))
        self.configure(fg_color=ECOPA_BG)

        # Efeito visual na janela
        try:
            pywinstyles.apply_style(self, "mica")
            pywinstyles.change_header_color(self, color=ECOPA_GREEN_DARK)
            pywinstyles.change_border_color(self, color=ECOPA_GREEN)
        except Exception:
            pass

        self._pil_image = None
        self.bg_photo = None
        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", BG_IMAGE)
        if os.path.exists(img_path):
            self._pil_image = Image.open(img_path)
        else:
            self._pil_image = None

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._update_bg_image()
        self.bind("<Configure>", self._on_resize)

        # Container centralizado para os campos de login
        self.login_container = ctk.CTkFrame(
            self,
            fg_color=ECOPA_WHITE,
            corner_radius=24,
            border_width=1,
            border_color=ECOPA_BORDER,
            width=480,
            height=480,
        )
        self.login_container.place(relx=0.76, rely=0.5, anchor="center")
        self.login_container.pack_propagate(False)

        # Logo ECOPA no topo do container
        logo_frame = ctk.CTkFrame(self.login_container, fg_color="transparent")
        logo_frame.pack(fill="x", padx=40, pady=(35, 0))

        # Icon de folha (emoji como placeholder do logo)
        leaf_label = ctk.CTkLabel(
            logo_frame, text="🌿",
            font=ctk.CTkFont(size=40), text_color=ECOPA_GREEN
        )
        leaf_label.pack(side="left", padx=(0, 10))

        ecopa_title = ctk.CTkLabel(
            logo_frame, text="ECOPA",
            font=ctk.CTkFont(size=28, weight="bold"), text_color=ECOPA_GREEN_DARK
        )
        ecopa_title.pack(side="left")

        subtitle = ctk.CTkLabel(
            self.login_container,
            text="Tecnologia · Sustentabilidade · Futuro",
            font=ctk.CTkFont(size=11), text_color=ECOPA_TEXT_LIGHT
        )
        subtitle.pack(pady=(5, 0))

        # Separador
        ctk.CTkFrame(self.login_container, fg_color=ECOPA_BORDER, height=1).pack(
            fill="x", padx=40, pady=(20, 25)
        )

        # Usuario
        user_label = ctk.CTkLabel(
            self.login_container, text="Usuário",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        )
        user_label.pack(fill="x", padx=55, pady=(0, 4))

        self.entry_user = ctk.CTkEntry(
            self.login_container,
            placeholder_text="Digite seu nome de usuário",
            fg_color=ECOPA_BG,
            text_color=ECOPA_TEXT,
            border_width=2,
            border_color=ECOPA_BORDER,
            bg_color=ECOPA_WHITE,
            height=42,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
        )
        self.entry_user.pack(fill="x", padx=55, pady=(0, 16))

        # Senha
        pass_label = ctk.CTkLabel(
            self.login_container, text="Senha",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ECOPA_TEXT,
            anchor="w"
        )
        pass_label.pack(fill="x", padx=55, pady=(0, 4))

        self.entry_pass = ctk.CTkEntry(
            self.login_container,
            placeholder_text="Digite sua senha",
            fg_color=ECOPA_BG,
            text_color=ECOPA_TEXT,
            border_width=2,
            border_color=ECOPA_BORDER,
            show="*",
            bg_color=ECOPA_WHITE,
            height=42,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
        )
        self.entry_pass.pack(fill="x", padx=55, pady=(0, 24))
        self.bind("<Return>", self._on_login)

        # Botao Entrar
        self.btn_login = ctk.CTkButton(
            self.login_container,
            text="Entrar",
            fg_color=ECOPA_GREEN,
            bg_color=ECOPA_WHITE,
            hover_color=ECOPA_GREEN_LIGHT,
            border_width=0,
            height=46,
            corner_radius=12,
            text_color=ECOPA_WHITE,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._on_login,
        )
        self.btn_login.pack(fill="x", padx=55, pady=(0, 10))

        # Link esqueci senha
        forgot = ctk.CTkLabel(
            self.login_container,
            text="Esqueceu a senha?",
            font=ctk.CTkFont(size=11), text_color=ECOPA_GREEN,
            cursor="hand2"
        )
        forgot.pack(pady=(0, 30))

    def _on_login(self, event=None):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        info, erro = GerenteController.login(user, password)
        if erro:
            messagebox.showerror("Erro", erro)
            self.entry_pass.delete(0, ctk.END)
            return
        # Destroi os widgets da tela de login
        self.entry_user.destroy()
        self.entry_pass.destroy()
        self.btn_login.destroy()
        self.bg_label.destroy()
        self.login_container.destroy()
        self.unbind("<Configure>")

        # Cria o dashboard
        dashboard = MainView(self, nome_usuario=info['nome'])
        dashboard.pack(fill="both", expand=True)
        self.title(f"ECOPA System - {info['nome']}")

    def _on_resize(self, event):
        if event.widget is self:
            self._update_bg_image()

    def _update_bg_image(self):
        if self._pil_image is None:
            return
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            return
        resized = self._pil_image.resize((w, h), Image.LANCZOS)
        self.bg_photo = ctk.CTkImage(resized, size=(w, h))
        self.bg_label.configure(image=self.bg_photo)


if __name__ == "__main__":
    app = App()
    app.mainloop()
