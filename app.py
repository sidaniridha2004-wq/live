from flask import Flask, jsonify
from flashscore_combo.combined_service import CombinedMatchService

app = Flask(__name__)
service = CombinedMatchService()

@app.get('/matches/today')
def matches_today():
    return jsonify({"matches": service.get_matches()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
