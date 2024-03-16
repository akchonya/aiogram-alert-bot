import aiohttp
from bs4 import BeautifulSoup


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_page(url):
    html = await fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    elements_with_class = soup.find_all(class_="_self cvplbd")
    text = ""
    for element in elements_with_class:
        title_text = element.get_text(strip=True)
        text += f"{title_text}\n"
    return text
