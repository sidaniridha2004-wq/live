from pydantic import BaseModel
from typing import List, Optional

class StreamCandidate(BaseModel):
    site: str
    match_page: Optional[str] = None
    embed_page: Optional[str] = None
    confidence: float = 0.0

class BroadcastInfo(BaseModel):
    channels: List[str] = []
    commentator: Optional[str] = None
    official_source: Optional[str] = None

class MatchRecord(BaseModel):
    id: str
    home_team: str
    away_team: str
    competition: Optional[str] = None
    kickoff: Optional[str] = None
    status: str = "UPCOMING"
    source_sites: List[str] = []
    broadcast: BroadcastInfo = BroadcastInfo()
    stream_candidates: List[StreamCandidate] = []
    confidence: float = 0.0
