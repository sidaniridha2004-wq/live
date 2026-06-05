import httpx
from bs4 import BeautifulSoup

class GenericMatchSiteAdapter:
    async def scrape(self, url: str):
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            r = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(' ', strip=True)
        return {
            'site': url,
            'raw_excerpt': text[:3000],
            'match_candidates': []
        }
