"""
database.py — Gestión de la base de datos SQLite.
"""
import sqlite3
from loguru import logger


def create_tables(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS posts (
            title TEXT,
            link  TEXT,
            UNIQUE(title, link) ON CONFLICT IGNORE
        );

        CREATE TABLE IF NOT EXISTS images (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id    TEXT,
            image_url  TEXT UNIQUE,
            posted     INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    logger.info("Base de datos lista.")


def post_exists(cursor: sqlite3.Cursor, title: str, link: str) -> bool:
    cursor.execute(
        "SELECT 1 FROM posts WHERE title = ? AND link = ?",
        (title, link),
    )
    return cursor.fetchone() is not None


def add_post(cursor: sqlite3.Cursor, conn: sqlite3.Connection, title: str, link: str) -> None:
    try:
        cursor.execute(
            "INSERT INTO posts (title, link) VALUES (?, ?)",
            (title, link),
        )
        conn.commit()
        logger.debug(f"Post guardado: {title}")
    except sqlite3.Error as e:
        logger.error(f"Error al insertar post en BD: {e}")


def image_exists(cursor: sqlite3.Cursor, image_url: str) -> bool:
    cursor.execute("SELECT 1 FROM images WHERE image_url = ?", (image_url,))
    return cursor.fetchone() is not None


def add_image(
    cursor: sqlite3.Cursor,
    conn: sqlite3.Connection,
    post_id: str,
    image_url: str,
    posted: bool,
) -> None:
    try:
        cursor.execute(
            "INSERT INTO images (post_id, image_url, posted) VALUES (?, ?, ?)",
            (post_id, image_url, int(posted)),
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error al insertar imagen en BD: {e}")
