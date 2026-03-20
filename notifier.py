"""
notifier.py — Envío de mensajes e imágenes a Telegram.
"""
import asyncio
import sqlite3

from loguru import logger
from telegram import Bot
from telegram.error import RetryAfter, TelegramError

from config import CHAT_ID, FLOOD_RETRY_BASE, MAX_RETRIES
import database as db
from scraper import get_last_page_number, scrape_images_from_page


# ── Mensajes de texto ─────────────────────────────────────────────────────────

def _build_post_url(link: str, forum_name: str) -> str:
    if forum_name == "debate_noticias_actualidad":
        return f"https://www.capa9.net{link}"
    return f"https://www.antronio.cl{link}"


async def send_post_notification(
    bot: Bot,
    title: str,
    link: str,
    thread_id: str,
    fecha: str,
    autor: str,
    forum_name: str,
) -> None:
    url = _build_post_url(link, forum_name)
    message = (
        f"📢 *{title}*\n"
        f"📅 Fecha: {fecha}\n"
        f"👤 Autor: {autor}\n"
        f"🔗 [Ver post]({url})"
    )

    for attempt in range(MAX_RETRIES):
        try:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                message_thread_id=thread_id,
                parse_mode="Markdown",
            )
            logger.info(f"Mensaje enviado: {title}")
            await asyncio.sleep(15)  # Margen anti-flood
            return
        except RetryAfter as e:
            wait = e.retry_after + (attempt * FLOOD_RETRY_BASE)
            logger.warning(f"Flood control: esperando {wait}s (intento {attempt + 1})")
            await asyncio.sleep(wait)
        except TelegramError as e:
            logger.error(f"Error de Telegram enviando '{title}': {e}")
            break
        except Exception as e:
            logger.error(f"Error inesperado enviando '{title}': {e}")
            break


# ── Imágenes (fpdctm) ─────────────────────────────────────────────────────────

async def send_images_from_fpdctm(
    bot: Bot,
    cursor: sqlite3.Cursor,
    conn: sqlite3.Connection,
    base_url: str,
    thread_id: str,
) -> None:
    logger.info("Revisando imágenes en fpdctm...")
    last_page = get_last_page_number(base_url)
    logger.info(f"Última página de fpdctm: {last_page}")

    images = scrape_images_from_page(base_url, last_page)

    for post_id, img_url in images:
        if db.image_exists(cursor, img_url):
            continue

        posted = False
        try:
            if img_url.lower().endswith((".gif", ".gifv")):
                await bot.send_document(
                    chat_id=CHAT_ID,
                    document=img_url,
                    caption="🖼️ Nueva imagen en fpdctm",
                    message_thread_id=thread_id,
                )
            else:
                await bot.send_photo(
                    chat_id=CHAT_ID,
                    photo=img_url,
                    caption="🖼️ Nueva imagen en fpdctm",
                    message_thread_id=thread_id,
                )
            logger.info(f"Imagen publicada: {img_url}")
            posted = True
            await asyncio.sleep(5)
        except TelegramError as e:
            logger.error(f"Error de Telegram con imagen {img_url}: {e}")
            await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Error inesperado con imagen {img_url}: {e}")
            await asyncio.sleep(10)
        finally:
            db.add_image(cursor, conn, post_id, img_url, posted)
