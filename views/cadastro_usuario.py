import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from PIL import Image, ImageTk
import re
from database.database import register_user
from tkinter import messagebox

ctk.set_appearance_mode("dark")

BG_IMAGE = r"fundo_login.png"
IMG_W, IMG_H = 1043, 673


class CadastroUsuario(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("ECOPA System - Cadastro de Usuário")
        self.geometry(f"{IMG_W}x{IMG_H}")

        self.protocol("WM_DELETE_WINDOW", self.sair)

        self._pil_image = None
        self.bg_photo = None
        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", BG_IMAGE)
        if os.path.exists(img_path):
            self._pil_image = Image.open(img_path)

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._update_bg_image()
        self.bind("<Configure>", self._on_resize)

        self._criar_formulario()

    def _criar_formulario(self):
        frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.85)

        titulo = ctk.CTkLabel(
            frame,
            text="Cadastro de Usuário",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1a3d3b",
        )
        titulo.place(relx=0.5, rely=0.06, anchor="center")

        labels = ["Nome Completo", "CPF", "Email", "Telefone", "Senha", "Confirmar Senha"]
        self.entries = {}

        y_start = 0.16
        espacamento = 0.11

        for i, label in enumerate(labels):
            lbl = ctk.CTkLabel(
                frame,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#333333",
                anchor="w",
            )
            lbl.place(relx=0.07, rely=y_start + i * espacamento, relwidth=0.4, relheight=0.05)

            entry = ctk.CTkEntry(
                frame,
                placeholder_text=f"Digite {label.lower()}",
                fg_color="#f0f0f0",
                text_color="black",
                border_width=1,
                border_color="#cccccc",
                font=ctk.CTkFont(size=13),
            )
            entry.place(relx=0.52, rely=y_start + i * espacamento, relwidth=0.43, relheight=0.06)
            self.entries[label] = entry

            if "Senha" in label:
                entry.configure(show="*")

        btn_cadastrar = ctk.CTkButton(
            frame,
            text="Cadastrar",
            fg_color="#205b59",
            hover_color="#13403e",
            text_color="white",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            command=self.handle_cadastro,
        )
        btn_cadastrar.place(relx=0.5, rely=0.88, anchor="center", relwidth=0.3)

        btn_voltar = ctk.CTkButton(
            frame,
            text="Voltar",
            fg_color="#999999",
            hover_color="#777777",
            text_color="white",
            font=ctk.CTkFont(size=13),
            height=35,
            command=self.sair,
        )
        btn_voltar.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.15)

    def handle_cadastro(self):
        dados = {label: self.entries[label].get().strip() for label in self.entries}

        if not all([dados["Nome Completo"], dados["CPF"], dados["Email"], dados["Senha"], dados["Confirmar Senha"]]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        if not re.match(r"^\d{11}$", dados["CPF"]):
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos numéricos!")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", dados["Email"]):
            messagebox.showerror("Erro", "Email inválido!")
            return

        if dados["Senha"] != dados["Confirmar Senha"]:
            messagebox.showerror("Erro", "Senhas não conferem!")
            return

        if len(dados["Senha"]) < 6:
            messagebox.showerror("Erro", "Senha deve ter no mínimo 6 caracteres!")
            return

        sucesso, msg = register_user(
            nome=dados["Nome Completo"],
            cpf=dados["CPF"],
            email=dados["Email"],
            senha=dados["Senha"],
            telefone=dados["Telefone"],
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", msg)

    def limpar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, ctk.END)

    def sair(self):
        self.destroy()

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
    app = ctk.CTk()
    app.withdraw()
    CadastroUsuario(app)
    app.mainloop()
