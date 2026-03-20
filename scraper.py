"""
scraper.py — Lógica de scraping de foros e imágenes.
"""
from urllib.parse import urljoin

import cloudscraper
from bs4 import BeautifulSoup
from loguru import logger

from config import EXCLUDED_URL_STARTS

_scraper = cloudscraper.create_scraper()

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean_url(url: str | None, base_url: str | None = None) -> str | None:
    if not url:
        return None
    if url.startswith("//"):
        return "https:" + url
    if base_url and (url.startswith("/") or not url.startswith(("http://", "https://"))):
        return urljoin(base_url, url)
    return url


def _is_valid_image(url: str | None) -> bool:
    if not url:
        return False
    return not any(url.startswith(exc) for exc in EXCLUDED_URL_STARTS)


# ── Scraping de foros ─────────────────────────────────────────────────────────

def scrape_forum_topics(url: str) -> list[tuple[str, str, str, str]]:
    """
    Devuelve una lista de (title, link, fecha, autor) para la página dada.
    """
    try:
        response = _scraper.get(url, headers=_HEADERS, timeout=20)
    except Exception as e:
        logger.error(f"Error de red al acceder a {url}: {e}")
        return []

    if response.status_code != 200:
        logger.critical(f"Error HTTP {response.status_code} en {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    raw_posts = soup.find_all("div", class_="structItem-cell structItem-cell--main")

    if not raw_posts:
        logger.critical(f"Sin posts en {url}. Posible bloqueo de Cloudflare.")
        return []

    results: list[tuple[str, str, str, str]] = []
    for post in raw_posts:
        try:
            title_elem = post.find("div", class_="structItem-title").find("a")
            title = title_elem.text.strip()
            link = title_elem["href"]
            autor = (
                post.find("a", class_="username").text.strip()
                if post.find("a", class_="username")
                else "Desconocido"
            )
            fecha_tag = post.find("time")
            fecha = fecha_tag["datetime"] if fecha_tag else "Desconocida"
            results.append((title, link, fecha, autor))
            logger.info(f"Post encontrado: {title} | {autor} | {fecha}")
        except AttributeError as e:
            logger.error(f"Error al parsear post: {e}")

    return results


# ── Scraping de imágenes (fpdctm) ─────────────────────────────────────────────

def get_last_page_number(base_url: str) -> int:
    """Devuelve el número de la última página del hilo."""
    try:
        probe_url = base_url.rstrip("/") + "/page-1"
        response = _scraper.get(probe_url, timeout=20)
        if response.status_code != 200:
            return 1
        soup = BeautifulSoup(response.text, "html.parser")
        page_links = soup.select(".pageNav-page")
        if page_links:
            numbers = [int(a.text.replace(",", "")) for a in page_links if a.text.replace(",", "").isdigit()]
            return max(numbers) if numbers else 1
    except Exception as e:
        logger.error(f"Error al obtener última página: {e}")
    return 1


def scrape_images_from_page(base_url: str, page_num: int) -> list[tuple[str, str]]:
    """
    Extrae imágenes de una página del hilo fpdctm.
    Devuelve lista de (post_id, image_url).
    """
    url = f"{base_url}page-{page_num}" if page_num > 1 else base_url.rstrip("/")
    try:
        response = _scraper.get(url, timeout=20)
        if response.status_code != 200:
            logger.error(f"Error HTTP {response.status_code} en {url}")
            return []
    except Exception as e:
        logger.error(f"Error de red en {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    images: list[tuple[str, str]] = []

    for post in soup.find_all(class_="message-cell--main"):
        content = post.find("div", class_="message-userContent")
        if not content:
            continue
        post_id = content.get("data-lb-id", "")
        for img in content.find_all("img", class_="bbImage"):
            img_url = _clean_url(img.get("src"), base_url)
            if img_url and _is_valid_image(img_url):
                images.append((post_id, img_url))

    return images
