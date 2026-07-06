import customtkinter as ctk
from PIL import Image, ImageTk
import os
from controllers.gerente_controller import GerenteController
from views.dashboard import MainView
from tkinter import messagebox

ctk.set_appearance_mode("dark")

BG_IMAGE = r"fundo_login.png"
IMG_W, IMG_H = 1043, 673


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECOPA System")
        self.geometry(f"{IMG_W}x{IMG_H}")

        self._pil_image = None
        self.bg_photo = None
        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", BG_IMAGE)
        if os.path.exists(img_path):
            self._pil_image = Image.open(img_path)

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._update_bg_image()
        self.bind("<Configure>", self._on_resize)

        self.entry_user = ctk.CTkEntry(
            self,
            placeholder_text="",
            fg_color="white",
            text_color="black",
            border_width=0,
            bg_color="#ffffff",
            height=32,
            font=ctk.CTkFont(size=14),
        )
        self.entry_user.place(relx=0.75, rely=0.4, anchor="center", relwidth=0.28)

        self.entry_pass = ctk.CTkEntry(
            self,
            placeholder_text="",
            fg_color="white",
            text_color="black",
            border_width=0,
            bg_color="#ffffff",
            height=32,
            font=ctk.CTkFont(size=14),
        )
        self.entry_pass.place(relx=0.75, rely=0.545, anchor="center", relwidth=0.28)

        self.btn_login = ctk.CTkButton(
            self,
            text="Entrar",
            fg_color="#DDEEDD",
            border_width=0,
            bg_color="#DDEEDD",
            hover_color="#205b59",
            height=25,
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_login
        )
        self.btn_login.place(relx=0.75, rely=0.65, anchor="center", relwidth=0.1)

    def _on_login(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        info, erro = GerenteController.login(user, password)
        if erro:
            messagebox.showerror("Erro", erro)
            self.entry_pass.delete(0, ctk.END)
            return
        self.withdraw()
        dashboard = MainView(self)
        dashboard.pack(fill="both", expand=True)
        self.deiconify()
        self.geometry("1200x700")
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
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.bg_label.configure(image=self.bg_photo)


if __name__ == "__main__":
    app = App()
    app.mainloop()
