from fastapi import FastAPI
from app.core.service import AggregationService

app = FastAPI(title="Smart Football Backend")
service = AggregationService()

@app.get('/health')
def health():
    return {"ok": True}

@app.get('/matches/today')
async def matches_today():
    return await service.get_today_matches()

@app.get('/matches/live')
async def matches_live():
    data = await service.get_today_matches()
    items = data.get("matches", [])
    live = [m for m in items if m.get("status") in {"LIVE", "HT"}]
    return {"matches": live, "count": len(live)}
