# Forum Monitor Bot 🤖

Bot de Telegram que monitorea antronio.cl y notifica nuevos posts e imágenes en un grupo con tópicos en Telegram.

## Estructura

```
.
├── main.py           # Punto de entrada
├── config.py         # Configuración desde variables de entorno
├── database.py       # Acceso a SQLite
├── scraper.py        # Lógica de scraping
├── notifier.py       # Envío a Telegram
├── requirements.txt
├── .env.example      # Plantilla de variables de entorno
└── .gitignore
```

## Configuración

1. Clona el repositorio
2. Crea el archivo `.env` a partir de la plantilla:
   ```bash
   cp .env.example .env
   ```
3. Edita `.env` con tus credenciales reales:
   ```
   BOT_TOKEN=tu_token_aqui
   CHAT_ID=tu_chat_id_aqui
   ```
4. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

```bash
python main.py
```

Los logs se escriben en `logs/scraper.log` y `logs/scraper_errors.log`.

## Variables de entorno

| Variable           | Requerida | Descripción                              | Default |
|--------------------|-----------|------------------------------------------|---------|
| `BOT_TOKEN`        | ✅        | Token del bot de Telegram                | —       |
| `CHAT_ID`          | ✅        | ID del grupo/canal de Telegram           | —       |
| `SCRAPE_INTERVAL`  | ❌        | Segundos entre ciclos de monitoreo       | `60`    |
| `FLOOD_RETRY_BASE` | ❌        | Segundos base para reintentos flood      | `19`    |
| `MAX_RETRIES`      | ❌        | Intentos máximos al enviar mensajes      | `5`     |



Este proyecto fue refactorizado por Claude para mejorar la legibilidad, la estructura y la mantenibilidad del código. Usado por mi para monitorear antronio.cl y notificar nuevos posts e imágenes en un grupo de Telegram que ya no existe. No me interesa para que lo uses, pero espero que te sirva de base para algo.


