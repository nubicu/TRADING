import requests
import os
import importlib

try:
    dotenv = importlib.import_module("dotenv")
    dotenv.load_dotenv()  # reads .env file if python-dotenv is installed
except Exception:
    # python-dotenv not available; environment variables will be used directly
    pass
API_KEY = os.getenv("NEWS_API_KEY")         # pulls the key from it
BASE_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"

def fetch_headlines(category, page_size=6):
    """Fetch headlines in Romanian, fall back to English if too few results."""
    def _fetch(language):
        try:
            response = requests.get(BASE_URL, params={
                "category": category,
                "language": language,
                "pageSize": page_size,
                "apiKey": API_KEY
            })
            response.raise_for_status()
            articles = response.json().get("articles", [])
            return [a for a in articles if a.get("title") != "[Removed]"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {category} in {language}: {e}")
            return []

    articles = _fetch("ro")
    if len(articles) < 3:               # not enough Romanian results
        articles = _fetch("en")         # fall back to English
    return articles

def fetch_romania(page_size=6):
    """Fetch Romania-specific news."""
    try:
        response = requests.get(EVERYTHING_URL, params={
            "q": "Romania",
            "language": "ro",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": API_KEY
        })
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [a for a in articles if a.get("title") != "[Removed]"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Romania news: {e}")
        return []

def get_all_news():
    """Fetch all four categories at once."""
    return {
        "business": fetch_headlines("business"),
        "technology": fetch_headlines("technology"),
        "trading": fetch_headlines("general", page_size=6),  # NewsAPI has no trading category — general is closest
        "romania": fetch_romania()
    }