import customtkinter as ctk

# ── Paleta ECOPA ──────────────────────────────────────────────
ECOPA_GREEN = "#006d12"
ECOPA_GREEN_LIGHT = "#0a8f2c"
ECOPA_GREEN_DARK = "#004d0e"
ECOPA_GREEN_BG = "#f0f7f0"
ECOPA_LEAF = "#27ae60"
ECOPA_WHITE = "#ffffff"
ECOPA_CARD_BG = "#ffffff"
ECOPA_SIDEBAR_BG = "#ffffff"
ECOPA_SIDEBAR_ACTIVE = "#e8f5e8"
ECOPA_TEXT = "#1a1a1a"
ECOPA_TEXT_LIGHT = "#666666"
ECOPA_BORDER = "#e0e8e0"
ECOPA_SHADOW = "#00000010"
ECOPA_ORANGE = "#f39c12"
ECOPA_BLUE = "#3498db"
ECOPA_RED = "#e74c3c"
ECOPA_YELLOW = "#f1c40f"

# Aliases para compatibilidade com views que usam ECOPA_BG
ECOPA_BG = ECOPA_GREEN_BG


# ── Fontes CTkFont cacheadas ──────────────────────────────────
_font_cache = {}


def _get(size, weight="normal"):
    key = (size, weight)
    if key not in _font_cache:
        _font_cache[key] = ctk.CTkFont(size=size, weight=weight)
    return _font_cache[key]


# Fontes usadas com mais frequência (pré-cacheadas)
def font_title(size=30):
    return _get(size, "bold")

def font_section(size=22):
    return _get(size, "bold")

def font_subtitle(size=15):
    return _get(size, "bold")

def font_body(size=13):
    return _get(size, "normal")

def font_body_bold(size=13):
    return _get(size, "bold")

def font_small(size=12):
    return _get(size, "normal")

def font_small_bold(size=12):
    return _get(size, "bold")

def font_tiny(size=11):
    return _get(size, "bold")

def font_kpi(size=28):
    return _get(size, "bold")

def font_kpi_small(size=24):
    return _get(size, "bold")

def font_menu(size=14):
    return _get(size, "normal")

def font_menu_bold(size=14):
    return _get(size, "bold")

def font(size=14, weight="normal"):
    """Atalho genérico para qualquer tamanho/peso."""
    return _get(size, weight)


# ── Cache de ícones ──────────────────────────────────────────
import os
from PIL import Image

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons")
_icon_cache = {}


def carregar_icone(nome, tamanho=20):
    """Carrega icone de assets/icons/{nome}.png com cache em memória."""
    from PIL import Image as _Image
    key = (nome, tamanho)
    if key not in _icon_cache:
        caminho = os.path.join(ICONS_DIR, f"{nome}.png")
        if os.path.exists(caminho):
            img = _Image.open(caminho).resize((tamanho, tamanho), _Image.LANCZOS)
            _icon_cache[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(tamanho, tamanho))
        else:
            _icon_cache[key] = None
    return _icon_cache[key]
