import aiohttp
from bs4 import BeautifulSoup


async def fetch(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None


async def parse_page(url):
    html = await fetch(url)
    if html is None:
        return "Failed to fetch the page."
    soup = BeautifulSoup(html, "html.parser")
    elements_with_class = soup.find_all("a", class_="_self cvplbd")
    text = ""
    for element in elements_with_class:
        title_text = element.get_text(strip=True)
        text += f"{title_text}\n"
    return text
