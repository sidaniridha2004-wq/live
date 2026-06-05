__version__ = "0.1.0"
__program__ = "livescore-api"
__repo__ = "https://github.com/Simatwa/livescore-api"
__info__ = "Access and manipulate matches from livescore.com with enriched app-friendly endpoints"
__author__ = "Smartwa"

from .main import JsonFormatter, Livescore, Utils
from .enriched import EnrichedLivescore

__all__ = ["JsonFormatter", "Livescore", "Utils", "EnrichedLivescore"]
