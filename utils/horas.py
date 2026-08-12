import re

HORA_RE = re.compile(r"^\d{2}:\d{2}$")

DIAS_SEMANA = [
    (1, "Dom"), (2, "Seg"), (3, "Ter"), (4, "Qua"),
    (5, "Qui"), (6, "Sex"), (7, "Sáb"),
]


def validar_hora(texto):
    """Valida se texto esta no formato HH:MM e horas 00-23, minutos 00-59."""
    if not texto or not HORA_RE.match(str(texto).strip()):
        return False
    h, m = str(texto).strip().split(":")
    return 0 <= int(h) <= 23 and 0 <= int(m) <= 59


def formatar_hora(valor):
    """Normaliza TIME do MySQL (timedelta/str) para HH:MM."""
    if valor is None:
        return ""
    texto = str(valor)
    partes = texto.split(":")
    if len(partes) >= 2:
        return f"{int(partes[0]):02d}:{int(partes[1]):02d}"
    return texto
