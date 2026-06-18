import customtkinter as ctk
from PIL import Image, ImageTk
import os
from database.database import verify_login, get_user_info
from tkinter import messagebox

ctk.set_appearance_mode("dark")

BG_IMAGE = r"C:\Users\62543886\Desktop\ECOPA.png"
IMG_W, IMG_H = 1043, 673


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECOPA System")
        self.geometry(f"{IMG_W}x{IMG_H}")

        self._pil_image = None
        self.bg_photo = None
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), BG_IMAGE)
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
            height=40,
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.handle_login
        )
        self.btn_login.place(relx=0.75, rely=0.8, anchor="center", relwidth=0.1)

    def handle_login(self):
        """Verifica as credenciais de login"""
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        
        if not user or not password:
            messagebox.showerror("Erro", "Por favor, preencha usuário e senha!")
            return
        
        if verify_login(user, password):
            user_info = get_user_info(user)
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user_info['nome']}!")
            self.entry_user.delete(0, ctk.END)
            self.entry_pass.delete(0, ctk.END)
            # Aqui você pode abrir a próxima tela do aplicativo
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
            self.entry_pass.delete(0, ctk.END)

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
