import re
from typing import Any, Dict, List
from .main import Livescore


class EnrichedLivescore:
    def __init__(self, date=None, month=None, year=None, country_code="KE", timeout=20):
        kwargs = {"country_code": country_code, "timeout": timeout}
        if date is not None:
            kwargs["date"] = date
        if month is not None:
            kwargs["month"] = month
        if year is not None:
            kwargs["year"] = year
        self.client = Livescore(**kwargs)

    def get_today_matches(self, max_matches: int = 100) -> List[Dict[str, Any]]:
        matches = self.client.matches(max=max_matches, raw=False) or []
        tv_html = self.client.fetch_tv_guide_html() or ""
        enriched = []
        for match in matches:
            match_id = match.get("match_id")
            detail = self.client.raw_match_data(match_id) if match_id else {}
            commentary = self.extract_commentary(detail)
            channels = self.extract_channels(tv_html, match)
            enriched.append(
                {
                    "matchId": str(match_id) if match_id is not None else None,
                    "competition": match.get("league"),
                    "country": match.get("country"),
                    "home": match.get("home"),
                    "away": match.get("away"),
                    "kickoff": match.get("kickoff"),
                    "status": match.get("status"),
                    "score": {
                        "home": match.get("home_scores"),
                        "away": match.get("away_scores"),
                    },
                    "commentary": commentary,
                    "channels": channels,
                    "rawDetail": detail,
                }
            )
        return enriched

    def extract_commentary(self, detail: Any) -> List[str]:
        results = []
        def walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    kl = str(k).lower()
                    if kl in {"commentary", "comments", "comment", "text", "description"} and isinstance(v, str):
                        txt = v.strip()
                        if len(txt) > 2 and txt not in results:
                            results.append(txt)
                    else:
                        walk(v)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        walk(detail)
        return results[:50]

    def extract_channels(self, html: str, match: Dict[str, Any]) -> List[str]:
        if not html:
            return []
        home = (match.get("home") or "").strip()
        away = (match.get("away") or "").strip()
        if not home or not away:
            return []
        pattern = re.compile(re.escape(home) + r".*?" + re.escape(away), re.I | re.S)
        if not pattern.search(html):
            alt = re.compile(re.escape(away) + r".*?" + re.escape(home), re.I | re.S)
            if not alt.search(html):
                return []
        known_channels = [
            "beIN Sports", "Sky Sports", "BT Sport", "TNT Sports", "Amazon Prime", "BBC", "ITV",
            "Canal+", "SuperSport", "ESPN", "DAZN", "FIFA+", "Premier Sports", "LaLigaSportsTV"
        ]
        found = []
        for name in known_channels:
            if re.search(re.escape(name), html, re.I) and name not in found:
                found.append(name)
        return found
