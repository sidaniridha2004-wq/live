from .flashscore_service import FlashscoreService
from .livescore_channels import LiveScoreChannelService

class CombinedMatchService:
    def __init__(self, flashscore_base_url="https://www.flashscore.fr", timeout=20):
        self.flashscore = FlashscoreService(base_url=flashscore_base_url, timeout=timeout)
        self.channels = LiveScoreChannelService(timeout=timeout)

    def get_matches(self):
        matches = self.flashscore.fetch_today_matches()
        tv_html = self.channels.fetch_tv_guide_html()
        combined = []
        for match in matches:
            match.channels = self.channels.get_channels_for_match(match.home, match.away, html=tv_html)
            combined.append(match.to_dict())
        return combined
