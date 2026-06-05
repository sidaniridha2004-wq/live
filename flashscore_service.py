from typing import List
from .models import MatchItem, Score, MatchEvent
from .utils import get_html, soupify

class FlashscoreService:
    def __init__(self, base_url="https://www.flashscore.fr", timeout=20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch_homepage(self) -> str:
        return get_html(f"{self.base_url}/", timeout=self.timeout)

    def parse_matches(self, html: str) -> List[MatchItem]:
        soup = soupify(html)
        results = []

        cards = soup.select('[id^="g_"], .event__match, .eventRow, .sportName.soccer .event__match')
        seen = set()
        for card in cards:
            text = card.get_text(" ", strip=True)
            if not text:
                continue
            mid = card.get("id") or text[:80]
            if mid in seen:
                continue
            seen.add(mid)

            home = None
            away = None
            status = None
            score_home = None
            score_away = None

            home_el = card.select_one('.event__participant--home, .duelParticipant__home .participant__participantName')
            away_el = card.select_one('.event__participant--away, .duelParticipant__away .participant__participantName')
            status_el = card.select_one('.event__stage, .event__time, .event__status')
            sh = card.select_one('.event__score--home, .detailScore__wrapper span:nth-child(1)')
            sa = card.select_one('.event__score--away, .detailScore__wrapper span:nth-child(2)')

            if home_el: home = home_el.get_text(strip=True)
            if away_el: away = away_el.get_text(strip=True)
            if status_el: status = status_el.get_text(strip=True)
            if sh: score_home = sh.get_text(strip=True)
            if sa: score_away = sa.get_text(strip=True)

            if not home and not away:
                continue

            results.append(MatchItem(
                match_id=mid,
                competition=None,
                country=None,
                home=home,
                away=away,
                status=status,
                score=Score(home=score_home, away=score_away),
            ))
        return results

    def fetch_today_matches(self) -> List[MatchItem]:
        html = self.fetch_homepage()
        return self.parse_matches(html)

    def fetch_match_detail_html(self, match_path: str) -> str:
        if match_path.startswith("http"):
            url = match_path
        else:
            url = f"{self.base_url}/{match_path.lstrip('/')}"
        return get_html(url, timeout=self.timeout)

    def parse_match_detail(self, html: str) -> dict:
        soup = soupify(html)
        commentary = []
        events = []

        for row in soup.select('.liveCommentary__row, .commentary__row, .verticalSections .smv__incident'):
            txt = row.get_text(' ', strip=True)
            if txt:
                commentary.append(txt)

        for ev in soup.select('.smv__incident, .incident, .verticalSections .smv__participantRow'):
            txt = ev.get_text(' ', strip=True)
            if txt:
                events.append(MatchEvent(description=txt))

        return {
            "commentary": commentary[:100],
            "events": [e.__dict__ for e in events[:100]],
        }
