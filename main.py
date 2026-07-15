from views.login import App
import pywinstyles

if __name__ == "__main__":
    app = App()
    # Efeito visual na janela principal
    try:
        pywinstyles.apply_style(app, "mica")
        pywinstyles.change_header_color(app, color="#004d0e")
        pywinstyles.change_border_color(app, color="#006d12")
    except Exception:
        pass
    app.mainloop()