import customtkinter as ctk


_font_cache = {}


def get_font(size=14, weight="normal"):
    key = (size, weight)
    if key not in _font_cache:
        _font_cache[key] = ctk.CTkFont(size=size, weight=weight)
    return _font_cache[key]
