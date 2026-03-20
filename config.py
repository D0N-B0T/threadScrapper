"""
config.py — Carga toda la configuración desde variables de entorno.
Nunca pongas credenciales directamente aquí.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Variable de entorno requerida no encontrada: '{key}'. "
            f"Copia .env.example a .env y rellena tus valores."
        )
    return value


# ── Telegram ──────────────────────────────────────────────────────────────────
BOT_TOKEN: str = _require("BOT_TOKEN")
CHAT_ID: str = _require("CHAT_ID")

# ── Comportamiento del scraper ────────────────────────────────────────────────
SCRAPE_INTERVAL: int = int(os.getenv("SCRAPE_INTERVAL", "60"))
FLOOD_RETRY_BASE: int = int(os.getenv("FLOOD_RETRY_BASE", "19"))
MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "5"))

# ── URLs de los foros ─────────────────────────────────────────────────────────
FORUMS_URLS: dict[str, str] = {
    "general_y_actualidad":       "https://www.antronio.cl/foros/general-y-actualidad.12/",
    "lum":                        "https://www.antronio.cl/foros/lum.188/",
    "politica_y_debates":         "https://www.antronio.cl/foros/politica-debates.22/",
    "el_muro":                    "https://www.antronio.cl/foros/el-muro.131/",
    "tech_ai":                    "https://www.antronio.cl/foros/ciencia-y-tecnologia.141/",
    "debate_noticias_actualidad":  "https://www.capa9.net/foro/debate-noticias-actualidad.87/",
    "fpdctm":                     "https://www.antronio.cl/temas/fotos-para-decir-conchetumadre.1289265/page-4647",
}

# ── IDs de threads en Telegram ────────────────────────────────────────────────
THREAD_IDS: dict[str, str] = {
    "general_y_actualidad":      "115",
    "debate_noticias_actualidad": "115",
    "lum":                       "119",
    "politica_y_debates":        "117",
    "el_muro":                   "153",
    "tech_ai":                   "879",
    "fpdctm":                    "5776",
}

# ── Filtros de imágenes ───────────────────────────────────────────────────────
EXCLUDED_URL_STARTS: list[str] = [
    "https://www.antronio.cl/data/avatars/",
    "https://www.antronio.cl/styles/elantro/",
]
