import httpx
from bs4 import BeautifulSoup

BEIN_URL = 'https://www.beinsports.com/en-mena/tv-guide'

class BeinAdapter:
    async def fetch(self):
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            r = await client.get(BEIN_URL, headers={'User-Agent': 'Mozilla/5.0'})
            html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(' ', strip=True)
        return {
            'source': 'beIN SPORTS TV Guide',
            'url': BEIN_URL,
            'raw_excerpt': text[:2000]
        }
