from rapidfuzz import fuzz
from app.core.normalize import normalize_text

def score_candidate(official: dict, candidate: dict) -> float:
    score = 0.0
    home_ratio = fuzz.ratio(normalize_text(official.get('home_team','')), normalize_text(candidate.get('home_team','')))
    away_ratio = fuzz.ratio(normalize_text(official.get('away_team','')), normalize_text(candidate.get('away_team','')))
    if home_ratio > 85 and away_ratio > 85:
        score += 0.35
    if candidate.get('channel') and official.get('channel') and normalize_text(candidate['channel']) == normalize_text(official['channel']):
        score += 0.20
    if candidate.get('commentator') and official.get('commentator') and normalize_text(candidate['commentator']) == normalize_text(official['commentator']):
        score += 0.10
    if candidate.get('source_site'):
        score += 0.10
    return min(score, 1.0)
