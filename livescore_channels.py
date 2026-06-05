import re
from .utils import get_html

class LiveScoreChannelService:
    TV_GUIDE_URL = "https://www.livescore.com/en/tv-guide/football-on-tv/"

    def __init__(self, timeout=20):
        self.timeout = timeout

    def fetch_tv_guide_html(self):
        return get_html(self.TV_GUIDE_URL, timeout=self.timeout)

    def get_channels_for_match(self, home: str, away: str, html: str | None = None):
        html = html or self.fetch_tv_guide_html()
        if not home or not away:
            return []
        block_hit = re.search(re.escape(home) + r".*?" + re.escape(away), html, re.I | re.S)
        if not block_hit:
            block_hit = re.search(re.escape(away) + r".*?" + re.escape(home), html, re.I | re.S)
            if not block_hit:
                return []
        known = [
            "beIN Sports", "Sky Sports", "BT Sport", "TNT Sports", "Amazon Prime", "BBC", "ITV",
            "Canal+", "SuperSport", "ESPN", "DAZN", "FIFA+", "Premier Sports", "LaLigaSportsTV"
        ]
        found = []
        for name in known:
            if re.search(re.escape(name), html, re.I) and name not in found:
                found.append(name)
        return found
