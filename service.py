from app.adapters.discovery import GoogleDiscovery
from app.adapters.bein import BeinAdapter

class AggregationService:
    def __init__(self):
        self.discovery = GoogleDiscovery()
        self.bein = BeinAdapter()

    async def get_today_matches(self):
        discovered = await self.discovery.discover()
        bein = await self.bein.fetch()
        return {
            'strategy': {
                'discovery_queries': [
                    'koora live', 'koora tv', 'yalla shoot', 'yalla koora'
                ],
                'official_schedule': bein.get('url')
            },
            'discovered_sites': discovered.get('sites', []),
            'official_schedule_excerpt': bein.get('raw_excerpt', ''),
            'matches': [],
            'notes': [
                'Next step: parse official schedule into structured matches',
                'Next step: scrape healthy discovered sites into match candidates',
                'Next step: fuzzy merge and assign confidence'
            ]
        }
