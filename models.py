from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Score:
    home: Optional[str] = None
    away: Optional[str] = None

@dataclass
class MatchEvent:
    minute: Optional[str] = None
    team: Optional[str] = None
    type: Optional[str] = None
    player: Optional[str] = None
    description: Optional[str] = None

@dataclass
class MatchItem:
    match_id: Optional[str] = None
    source: str = "flashscore"
    competition: Optional[str] = None
    country: Optional[str] = None
    home: Optional[str] = None
    away: Optional[str] = None
    kickoff: Optional[str] = None
    status: Optional[str] = None
    score: Score = field(default_factory=Score)
    commentary: List[str] = field(default_factory=list)
    events: List[MatchEvent] = field(default_factory=list)
    channels: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
