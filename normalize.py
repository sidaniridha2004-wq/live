import re

TEAM_ALIASES = {
    'psg': 'paris saint-germain',
    'paris sg': 'paris saint-germain',
    'man utd': 'manchester united',
    'man city': 'manchester city',
    'inter': 'inter milan',
}

def normalize_text(value: str) -> str:
    value = (value or '').strip().lower()
    value = re.sub(r'\s+', ' ', value)
    return TEAM_ALIASES.get(value, value)
