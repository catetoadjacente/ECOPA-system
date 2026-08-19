import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("ecopa.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

from views.login import App
import pywinstyles

if __name__ == "__main__":
    app = App()
    try:
        pywinstyles.apply_style(app, "mica")
        pywinstyles.change_header_color(app, color="#004d0e")
        pywinstyles.change_border_color(app, color="#006d12")
    except Exception:
        pass
    app.mainloop()
