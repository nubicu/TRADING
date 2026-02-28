import requests
import os
import time
import importlib
import feedparser # type: ignore
from datetime import datetime, timezone

try:
    dotenv = importlib.import_module("dotenv")
    dotenv.load_dotenv()  # reads .env file if python-dotenv is installed
except Exception:
    # python-dotenv not available; environment variables will be used directly
    pass
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")         # pulls the key from it
GUARDIAN_BASE_URL = "https://content.guardianapis.com"
CACHE_DURATION = 60 * 60        # 1 hour in seconds

# Cache per category
_cache = {}

# ─────────────────────────────────────────
# FETCHERS
# ─────────────────────────────────────────

def fetch_hackernews(limit=10):
    try:
        headers = {"User-Agent": "news-dashboard/1.0"}

        # Step 1 — get the list of top story IDs
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers=headers
        )
        response.raise_for_status()
        story_ids = response.json()[:30]        # fetch top 30, we'll sort and trim to 10

        # Step 2 — fetch details for each story
        articles = []
        for story_id in story_ids:
            story_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                headers=headers
            )
            story_response.raise_for_status()
            story = story_response.json()

            if not story or story.get("type") != "story":
                continue
            if not story.get("url") or not story.get("title"):
                continue

            # convert Unix timestamp to readable string
            utc_time = datetime.fromtimestamp(
                story["time"],
                tz=timezone.utc
            )
            published = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            articles.append({
                "title": story["title"],
                "url": story["url"],
                "source": {"name": "Hacker News"},
                "publishedAt": published,
                "points": story.get("score", 0)
            })

        # sort by points and return top results
        articles.sort(key=lambda x: x["points"], reverse=True)
        return articles[:limit]
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
        return []

def fetch_reddit(subreddit="technology", limit=10):
    try:
        headers = {"User-Agent": "news-dashboard/1.0"}
        response = requests.get(
            f"https://www.reddit.com/r/{subreddit}/hot.json",
            headers=headers,
            params={"limit": limit}
        )
        response.raise_for_status()
        posts = response.json()["data"]["children"]

        articles = []
        for p in posts:
            if p["data"].get("stickied"):
                continue
            
            # convert Unix timestamp to readable string
            utc_time = datetime.fromtimestamp(
                p["data"]["created_utc"], 
                tz=timezone.utc
            )
            published = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")  # same format as NewsAPI

            articles.append({
                "title": p["data"]["title"],
                "url": p["data"]["url"],
                "source": {"name": f"r/{subreddit}"},
                "publishedAt": published,
                "points": p["data"]["score"]
            })

        return articles
    except Exception as e:
        print(f"Error fetching r/{subreddit}: {e}")
        return []
    
def fetch_guardian(section, limit=10):
    """Fetch articles from The Guardian by section."""
    try:
        response = requests.get(
            f"{GUARDIAN_BASE_URL}/{section}",
            params={
                "api-key": GUARDIAN_API_KEY,
                "page-size": limit,
                "order-by": "newest",
                "show-fields": "trailText"
            }
        )
        response.raise_for_status()
        results = response.json()["response"]["results"]

        return [{
            "title": a["webTitle"],
            "url": a["webUrl"],
            "source": {"name": "The Guardian"},
            "publishedAt": a["webPublicationDate"].replace("Z", ":00Z") if a.get("webPublicationDate") else None,
            "points": 0
        } for a in results]
    except Exception as e:
        print(f"Error fetching Guardian {section}: {e}")
        return []

def fetch_devto(tag="python", limit=10):
    """Fetch articles from Dev.to by tag."""
    try:
        response = requests.get(
            "https://dev.to/api/articles",
            params={"tag": tag, "per_page": limit},
            headers={"User-Agent": "news-dashboard/1.0"}
        )
        response.raise_for_status()
        articles = response.json()

        return [{
            "title": a["title"],
            "url": a["url"],
            "source": {"name": "Dev.to"},
            "publishedAt": a.get("published_at"),
            "points": a.get("positive_reactions_count", 0)
        } for a in articles]
    except Exception as e:
        print(f"Error fetching Dev.to: {e}")
        return []


def fetch_lobsters(limit=10):
    """Fetch hottest stories from Lobste.rs."""
    try:
        response = requests.get(
            "https://lobste.rs/hottest.json",
            headers={"User-Agent": "news-dashboard/1.0"}
        )
        response.raise_for_status()
        stories = response.json()[:limit]

        return [{
            "title": s["title"],
            "url": s["url"],
            "source": {"name": "Lobste.rs"},
            "publishedAt": s.get("created_at", "")[:19] + "Z" if s.get("created_at") else None,
            "points": s.get("score", 0)
        } for s in stories]
    except Exception as e:
        print(f"Error fetching Lobste.rs: {e}")
        return []

def fetch_rss(url, source_name, limit=10):
    """Fetch articles from any RSS feed."""
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:limit]:
            articles.append({
                "title": entry.get("title"),
                "url": entry.get("link"),
                "source": {"name": source_name},
                "publishedAt": entry.get("published", "")[:20] + "Z" if entry.get("published") else None,
                "points": 0
            })
        return articles
    except Exception as e:
        print(f"Error fetching RSS {source_name}: {e}")
        return []
    
# ─────────────────────────────────────────
# SINGLE SOURCE OF TRUTH — all fetchers
# ─────────────────────────────────────────

ALL_FETCHERS = {
    # Romania
    "romania libera":           lambda: fetch_rss("https://romanialibera.ro/feed", "România Liberă"),
    "jurnalul":                 lambda: fetch_rss("https://jurnalul.ro/rss", "Jurnalul.ro"),
    "cotidianul":               lambda: fetch_rss("https://cotidianul.ro/feed", "Cotidianul"),
    "mediafax":                 lambda: fetch_rss("https://www.mediafax.ro/rss", "Mediafax"),
    "hotnews":                  lambda: fetch_rss("https://www.hotnews.ro/rss", "HotNews.ro"),
    "digi24":                   lambda: fetch_rss("https://www.digi24.ro/rss", "Digi24"),
    "g4media":                  lambda: fetch_rss("https://www.g4media.ro/feed", "G4Media.ro"),
    "agerpres":                 lambda: fetch_rss("https://www.agerpres.ro/home.rss", "Agerpres"),

    # Finance RO
    "profit.ro":                lambda: fetch_rss("https://www.profit.ro/rss", "Profit.ro"),
    "capital.ro":               lambda: fetch_rss("https://www.capital.ro/feed", "Capital.ro"),
    "finante.ro":               lambda: fetch_rss("https://www.finante.ro/rss", "Finante.ro"),
    "economica":                lambda: fetch_rss("https://economica.net/feed", "Economica"),
    "ziarul financiar":         lambda: fetch_rss("https://www.zf.ro/rss", "Ziarul Financiar"),
    "zf companii":              lambda: fetch_rss("https://www.zf.ro/rss/companii", "ZF - Companii"),
    "zf fonduri mutuale":       lambda: fetch_rss("https://www.zf.ro/rss/burse-fonduri-mutuale", "ZF - Fonduri Mutuale"),
    "zf banci":                 lambda: fetch_rss("https://www.zf.ro/rss/banci-si-asigurari", "ZF - Banci si Asigurari"),
    "curs de guvernare":        lambda: fetch_rss("https://cursdeguvernare.ro/feed", "Curs de Guvernare"),
    "mediafax economic":        lambda: fetch_rss("https://www.mediafax.ro/rss/economic", "Mediafax Economic"),
    "bnr":                      lambda: fetch_rss("https://news.google.com/rss/search?q=BNR+banca+nationala+romania&hl=ro&gl=RO&ceid=RO:ro", "BNR"),
    "ing bank romania":         lambda: fetch_rss("https://news.google.com/rss/search?q=ING+bank+romania&hl=ro&gl=RO&ceid=RO:ro", "ING Bank România"),

    # Finance Intl
    "cnbc finance":             lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664", "CNBC Finance"),
    "cnbc markets":             lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069", "CNBC Markets"),
    "cnbc economy":             lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258", "CNBC Economy"),
    "cnbc earnings":            lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135", "CNBC Earnings"),
    "cnbc wealth":              lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001054", "CNBC Wealth"),
    "cnbc investing":           lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069", "CNBC Investing"),
    "yahoo finance":            lambda: fetch_rss("https://finance.yahoo.com/news/rssindex", "Yahoo Finance"),
    "marketwatch":              lambda: fetch_rss("https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines", "MarketWatch"),
    "investing.com":            lambda: fetch_rss("https://www.investing.com/rss/news.rss", "Investing.com"),
    "financial times":          lambda: fetch_rss("https://news.google.com/rss/search?q=when:24h+allinurl:ft.com&ceid=US:en&hl=en-US&gl=US", "Financial Times"),
    "seeking alpha":            lambda: fetch_rss("https://seekingalpha.com/feed.xml", "Seeking Alpha"),
    "kiplinger":                lambda: fetch_rss("https://www.kiplinger.com/feed/all", "Kiplinger"),
    "cbs moneywatch":           lambda: fetch_rss("https://www.cbsnews.com/latest/rss/moneywatch", "CBS Moneywatch"),
    "marketbeat":               lambda: fetch_rss("https://www.marketbeat.com/feed", "MarketBeat"),
    "daily reckoning":          lambda: fetch_rss("https://dailyreckoning.com/feed", "Daily Reckoning"),
    "federal reserve":          lambda: fetch_rss("https://www.federalreserve.gov/feeds/press_monetary.xml", "Federal Reserve"),
    "naked capitalism":         lambda: fetch_rss("https://www.nakedcapitalism.com/feed", "Naked Capitalism"),
    "politico morning money":   lambda: fetch_rss("https://rss.politico.com/morningmoney.xml", "Politico Morning Money"),
    "politico economy":         lambda: fetch_rss("https://rss.politico.com/economy.xml", "Politico Economy"),
    "romania insider":          lambda: fetch_rss("https://www.romania-insider.com/feed", "Romania Insider"),
    "nine o clock":             lambda: fetch_rss("https://nineoclock.ro/feed", "Nine O'Clock"),
    "diplomat bucharest":       lambda: fetch_rss("https://thediplomat.ro/feed", "Diplomat Bucharest"),

    # Forex - Trading
    "fxstreet":                 lambda: fetch_rss("https://www.fxstreet.com/rss/news", "FXStreet"),
    "fxstreet analysis":        lambda: fetch_rss("https://www.fxstreet.com/rss/analysis", "FXStreet Analysis"),
    "dailyforex news":          lambda: fetch_rss("https://www.dailyforex.com/rss/forexnews.xml", "DailyForex News"),
    "dailyforex analysis":      lambda: fetch_rss("https://www.dailyforex.com/rss/fundamentalanalysis.xml", "DailyForex Analysis"),
    "myfxbook":                 lambda: fetch_rss("https://www.myfxbook.com/rss/latest-forex-news", "MyFxBook"),
    "forexlive":                lambda: fetch_rss("https://www.forexlive.com/feed", "ForexLive"),
    "politico morning trade":   lambda: fetch_rss("https://rss.politico.com/morningtrade.xml", "Politico Morning Trade"),

    # Nasdaq
    "nasdaq markets":           lambda: fetch_rss("https://www.nasdaq.com/feed/rssoutbound?category=Market+News",  "Nasdaq Markets"),
    "nasdaq stocks":            lambda: fetch_rss("https://www.nasdaq.com/feed/rssoutbound?category=Stock+News",  "Nasdaq Stocks"),
    "nasdaq etfs":              lambda: fetch_rss("https://www.nasdaq.com/feed/rssoutbound?category=ETF+News",       "Nasdaq ETFs"),
    "nasdaq earnings":          lambda: fetch_rss("https://www.nasdaq.com/feed/rssoutbound?category=Earnings+News",     "Nasdaq Earnings"),
    "nasdaq commodities":       lambda: fetch_rss("https://www.nasdaq.com/feed/rssoutbound?category=Commodities+News",  "Nasdaq Commodities"),
    "nasdaq crypto":            lambda: fetch_rss("https://www.nasdaq.com/feed/rssoutbound?category=Crypto+News",  "Nasdaq Crypto"),

    # Technology
    "hacker news":              lambda: fetch_hackernews(),
    "dev.to":                   lambda: fetch_devto(tag="python"),
    "lobste.rs":                lambda: fetch_lobsters(),
    "cnbc tech":                lambda: fetch_rss("https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910", "CNBC Tech"),
    "guardian: technology":     lambda: fetch_guardian("technology"),
    "techcrunch":               lambda: fetch_rss("https://techcrunch.com/feed/", "TechCrunch"),
    "mit tech review":          lambda: fetch_rss("https://www.technologyreview.com/feed/", "MIT Tech Review"),
    "venture beat":             lambda: fetch_rss("https://venturebeat.com/feed/", "Venture Beat"),

    # Programming
    "freecodecamp":             lambda: fetch_rss("https://freecodecamp.org/news/rss/", "freeCodeCamp"),
    "dev.to python":            lambda: fetch_rss("https://dev.to/feed/tag/python", "Dev.to Python"),
    "real python":              lambda: fetch_rss("https://realpython.com/atom.xml", "Real Python"),
    "planet python":            lambda: fetch_rss("https://planetpython.org/rss20.xml", "Planet Python"),
    "dev.to webdev":            lambda: fetch_rss("https://dev.to/feed/tag/webdev", "Dev.to WebDev"),
    "dev.to javascript":        lambda: fetch_rss("https://dev.to/feed/tag/javascript", "Dev.to JavaScript"),
    "javascript weekly":        lambda: fetch_rss("https://javascriptweekly.com/rss/", "JavaScript Weekly"),
    "css tricks":               lambda: fetch_rss("https://css-tricks.com/feed/", "CSS Tricks"),
    "golang weekly":            lambda: fetch_rss("https://golangweekly.com/rss/", "Golang Weekly"),
    "rust blog":                lambda: fetch_rss("https://blog.rust-lang.org/feed.xml", "Rust Blog"),
    "smashing magazine":        lambda: fetch_rss("https://www.smashingmagazine.com/feed/", "Smashing Magazine"),
    "a list apart":             lambda: fetch_rss("https://alistapart.com/main/feed/", "A List Apart"),
    "codrops":                  lambda: fetch_rss("https://tympanus.net/codrops/feed/", "Codrops"),
    "martin fowler":            lambda: fetch_rss("https://martinfowler.com/feed.atom", "Martin Fowler"),
    "infoq":                    lambda: fetch_rss("https://feed.infoq.com/", "InfoQ"),
    "dzone":                    lambda: fetch_rss("https://feeds.dzone.com/home", "DZone"),

    # Engineering Blogs
    "airbnb tech":              lambda: fetch_rss("https://medium.com/feed/airbnb-engineering", "Airbnb Tech"),
    "meta engineering":         lambda: fetch_rss("https://engineering.fb.com/feed/", "Meta Engineering"),
    "github blog":              lambda: fetch_rss("https://github.blog/feed/", "GitHub Blog"),
    "stack overflow blog":      lambda: fetch_rss("https://stackoverflow.blog/feed/", "Stack Overflow Blog"),
    "docker blog":              lambda: fetch_rss("https://www.docker.com/blog/feed/", "Docker Blog"),
    "devops.com":               lambda: fetch_rss("https://devops.com/feed/", "DevOps.com"),
    "opensource.com":           lambda: fetch_rss("https://opensource.com/feed", "Opensource.com"),

    # Security
    "krebs on security":        lambda: fetch_rss("https://krebsonsecurity.com/feed/", "Krebs on Security"),
    "schneier on security":     lambda: fetch_rss("https://www.schneier.com/feed/atom/", "Schneier on Security"),
    "zdnet":                    lambda: fetch_rss("https://www.zdnet.com/news/rss.xml", "ZDNet"),
    "wired":                    lambda: fetch_rss("https://www.wired.com/feed/rss", "Wired"),
    "ars technica":             lambda: fetch_rss("https://feeds.arstechnica.com/arstechnica/index", "Ars Technica"),

    # Business
    "guardian: business":       lambda: fetch_guardian("business"),
    "economist":                lambda: fetch_rss("https://www.economist.com/business/rss.xml", "The Economist"),
    "wallstreet journal":       lambda: fetch_rss("https://news.google.com/rss/search?q=when:24h+site:wsj.com&ceid=US:en&hl=en-US&gl=US", "Wall Street Journal"),
    "euronews":                 lambda: fetch_rss("http://feeds.feedburner.com/euronews/en/home/", "Euronews"),

    # Reddits
    "r/investing":              lambda: fetch_reddit("investing"),
    "r/wallstreetbets":         lambda: fetch_reddit("wallstreetbets"),
    "r/stocks":                 lambda: fetch_reddit("stocks"),
    "r/economics":              lambda: fetch_reddit("economics"),
    "r/finance":                lambda: fetch_reddit("finance"),
    "r/cryptocurrency":         lambda: fetch_reddit("CryptoCurrency"),
    "r/algotrading":            lambda: fetch_reddit("algotrading"),
    "r/tech":                   lambda: fetch_reddit("technology"),
    "r/programming":            lambda: fetch_reddit("programming"),
    "r/artificial":             lambda: fetch_reddit("artificial"),
    "r/machinelearning":        lambda: fetch_reddit("MachineLearning"),
    "r/datascience":            lambda: fetch_reddit("datascience"),
    "r/python":                 lambda: fetch_reddit("python"),
    "r/cybersecurity":          lambda: fetch_reddit("cybersecurity"),
    "r/startups":               lambda: fetch_reddit("startups"),
    "r/futurology":             lambda: fetch_reddit("Futurology"),
    "r/worldnews":              lambda: fetch_reddit("worldnews"),
    "r/europe":                 lambda: fetch_reddit("europe"),
    "r/geopolitics":            lambda: fetch_reddit("geopolitics"),
    "r/romania":                lambda: fetch_reddit("Romania"),

    # EU
    "eu parliament":            lambda: fetch_rss("https://www.europarl.europa.eu/rss/doc/press-releases/en.xml", "EU Parliament"),
    "eu economy":               lambda: fetch_rss("https://www.europarl.europa.eu/rss/topic/907/en.xml", "EU Economy"),
    "politico europe":          lambda: fetch_rss("https://www.politico.eu/feed/", "Politico Europe"),
    "france 24":                lambda: fetch_rss("https://www.france24.com/en/rss", "France 24"),
    "dw europe":                lambda: fetch_rss("https://rss.dw.com/rdf/rss-en-eu", "DW Europe"),
}

# "bursa titluri",
# "bursa capital",
# "bloomberg",

# ─────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────

CATEGORIES = {
    "Romania": [
        "romania libera",
        "jurnalul",
        "cotidianul",
        "mediafax",
        "hotnews",
        "digi24",
        "g4media",
        "agerpres",
    ],
    "Finance — RO": [
        "profit.ro",
        "capital.ro",
        "finante.ro",
        "economica",
        "ziarul financiar",
        "zf companii",
        "zf fonduri mutuale",
        "zf banci",
        "curs de guvernare",
        "mediafax economic",
        "bnr",
        "ing bank romania",
    ],
    "Finance — Intl": [
        "cnbc finance",
        "cnbc markets",
        "cnbc economy",
        "cnbc earnings",
        "cnbc wealth",
        "cnbc investing",
        "yahoo finance",
        "marketwatch",
        "investing.com",
        "financial times",
        "seeking alpha",
        "kiplinger",
        "cbs moneywatch",
        "marketbeat",
        "daily reckoning",
        "federal reserve",
        "naked capitalism",
        "politico morning money",
        "politico economy",
        "romania insider",
        "nine o clock",
        "diplomat bucharest",
    ],
    "Forex - Trading": [
        "fxstreet",
        "fxstreet analysis",
        "dailyforex news",
        "dailyforex analysis",
        "myfxbook",
        "forexlive",
        "politico morning trade",
    ],
    "Nasdaq": [
        "nasdaq markets",
        "nasdaq stocks",
        "nasdaq etfs",
        "nasdaq earnings",
        "nasdaq commodities",
        "nasdaq crypto",
    ],
    "Technology": [
        "hacker news",
        "dev.to",
        "lobste.rs",
        "cnbc tech",
        "guardian: technology",
        "techcrunch",
        "mit tech review",
        "venture beat",
    ],
    "Programming": [
        "freecodecamp",
        "dev.to python",
        "real python",
        "planet python",
        "dev.to webdev",
        "dev.to javascript",
        "javascript weekly",
        "css tricks",
        "golang weekly",
        "rust blog",
        "smashing magazine",
        "a list apart",
        "codrops",
        "martin fowler",
        "infoq",
        "dzone",
    ],
    "Engineering Blogs": [
        "airbnb tech",
        "meta engineering",
        "github blog",
        "stack overflow blog",
        "docker blog",
        "devops.com",
        "opensource.com",
    ],
    "Security": [
        "krebs on security",
        "schneier on security",
        "zdnet",
        "wired",
        "ars technica",
    ],
    "Business": [
        "guardian: business",
        "economist",
        "wallstreet journal",
        "euronews",
    ],
    "Reddits": [
        "r/investing",
        "r/wallstreetbets",
        "r/stocks",
        "r/economics",
        "r/finance",
        "r/cryptocurrency",
        "r/algotrading",
        "r/tech",
        "r/programming",
        "r/artificial",
        "r/machinelearning",
        "r/datascience",
        "r/python",
        "r/cybersecurity",
        "r/startups",
        "r/futurology",
        "r/worldnews",
        "r/europe",
        "r/geopolitics",
        "r/romania",
    ],
    "EU": [
        "eu parliament",
        "eu economy",
        "politico europe",
        "france 24",
        "dw europe",
    ],
}

# ─────────────────────────────────────────
# STREAMING — yields one source at a time
# ─────────────────────────────────────────

def stream_news_for_category(category):
    """Generator that yields (key, articles) one source at a time."""
    keys_to_fetch = CATEGORIES.get(category, list(ALL_FETCHERS.keys()))

    for key in keys_to_fetch:
        if key in ALL_FETCHERS:
            articles = ALL_FETCHERS[key]()
            yield key, articles

# ─────────────────────────────────────────
# CACHE — for serving repeat visits instantly
# ─────────────────────────────────────────

def get_cached(category):
    """Return cached data for a category if still fresh, else None."""
    cached = _cache.get(category)
    if cached and (time.time() - cached["last_fetched"]) < CACHE_DURATION:
        return cached["data"]
    return None


def set_cache(category, data):
    """Store fetched data in cache."""
    _cache[category] = {
        "data": data,
        "last_fetched": time.time()
    }


def get_cache_minutes_left(category):
    """Return minutes until cache expires for a category."""
    cached = _cache.get(category)
    if not cached:
        return 0
    age = time.time() - cached["last_fetched"]
    return max(0, round((CACHE_DURATION - age) / 60))