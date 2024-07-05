import logging
from bs4 import BeautifulSoup
import aiohttp


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                logger.info("Fetched HTML successfully.")
                return html
    except Exception as e:
        logger.error(f"Error fetching URL: {e}")
        return None


async def parse_page(url):
    html = await fetch(url)
    if html is None:
        return "Failed to fetch the page."
    soup = BeautifulSoup(html, "html.parser")
    logger.info("Parsed HTML with BeautifulSoup.")

    elements_with_class = soup.find_all("a", class_="_self cvplbd")
    if not elements_with_class:
        logger.warning("No elements found with class '_self cvplbd'")
        return "No elements found."

    text = ""
    for element in elements_with_class:
        title_text = element.get_text(strip=True)
        logger.info(f"Found element: {title_text}")
        text += f"{title_text}\n"
    return text
