import os, httpx

DISCOVERY_QUERIES = [
    'koora live بث مباشر مباريات اليوم',
    'koora tv بث مباشر',
    'yalla shoot live today',
    'yalla koora live',
    'kora live beIN commentator',
]

KEYWORD_HINTS = ['koora', 'kora', 'yalla', 'live', 'tv', 'shoot']

class GoogleDiscovery:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CSE_KEY', '')
        self.cx = os.getenv('GOOGLE_CSE_CX', '')

    async def discover(self):
        if not self.api_key or not self.cx:
            return {
                'warning': 'Missing GOOGLE_CSE_KEY or GOOGLE_CSE_CX',
                'sites': []
            }
        out = []
        async with httpx.AsyncClient(timeout=20) as client:
            for q in DISCOVERY_QUERIES:
                r = await client.get('https://www.googleapis.com/customsearch/v1', params={
                    'key': self.api_key,
                    'cx': self.cx,
                    'q': q,
                })
                data = r.json()
                for item in data.get('items', []):
                    link = item.get('link', '')
                    title = item.get('title', '')
                    low = (link + ' ' + title).lower()
                    if any(k in low for k in KEYWORD_HINTS):
                        out.append({'url': link, 'title': title})
        uniq = []
        seen = set()
        for row in out:
            if row['url'] not in seen:
                uniq.append(row)
                seen.add(row['url'])
        return {'sites': uniq}
