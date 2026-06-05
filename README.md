# Flashscore + LiveScore combo backend

This starter backend uses:
- Flashscore as the main source for football match listings and future commentary parsing
- LiveScore TV guide as the source for channels / where-to-watch

## Endpoints

- `GET /matches/today`

## Notes

- This is a starter scraper backend, not an official API.
- Flashscore selectors may need updates because the site can change HTML structure.
- LiveScore channel extraction is heuristic and should be refined with real test cases.
- Best use: run this as your backend, then let your Android app call your backend only.

## Run

```bash
pip install -r requirements.txt
python app.py
```
