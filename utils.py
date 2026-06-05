import re
import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
}


def get_json(url, timeout=20, headers=None):
    r = requests.get(url, timeout=timeout, headers=headers or DEFAULT_HEADERS)
    r.raise_for_status()
    return r.json()


def get_html(url, timeout=20, headers=None):
    r = requests.get(url, timeout=timeout, headers=headers or DEFAULT_HEADERS)
    r.raise_for_status()
    return r.text


def soupify(html: str):
    return BeautifulSoup(html, "html.parser")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip().lower()
