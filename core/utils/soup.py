import logging
import aiohttp
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept-Language": "uk-UA,uk;q=0.9",
}


async def fetch(url: str) -> str | None:
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Bad status {response.status} for {url}")
                    return None
                html = await response.text()
                logger.info("Fetched HTML successfully.")
                return html
    except Exception as e:
        logger.error(f"Error fetching URL: {e}")
        return None


async def parse_page(url: str) -> str:
    html = await fetch(url)
    if html is None:
        return "Не вдалося завантажити сторінку.\n"

    soup = BeautifulSoup(html, "html.parser")

    # Новий формат: картки плагіна holiday-hub
    links = soup.select("article.hh-card h3.hh-card__title a")

    # Запасний варіант на випадок, якщо повернуть старий формат
    if not links:
        logger.warning("hh-card not found, trying old selector")
        links = soup.select("a._self.cvplbd")

    titles = []
    for a in links:
        title = a.get_text(strip=True)
        if title and title != "Детальніше" and title not in titles:
            titles.append(title)

    if not titles:
        logger.warning("No holidays found on the page")
        return "Свят не знайдено.\n"

    logger.info(f"Found {len(titles)} holidays")
    return "".join(f"{t}\n" for t in titles)
