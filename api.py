from flask import Flask, jsonify, request
from .enriched import EnrichedLivescore

app = Flask(__name__)


@app.get("/matches/today")
def matches_today():
    date = request.args.get("date", type=int)
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    country_code = request.args.get("country_code", default="KE", type=str)
    timeout = request.args.get("timeout", default=20, type=int)
    max_matches = request.args.get("max", default=100, type=int)
    service = EnrichedLivescore(date=date, month=month, year=year, country_code=country_code, timeout=timeout)
    return jsonify({"matches": service.get_today_matches(max_matches=max_matches)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
