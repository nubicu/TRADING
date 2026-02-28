import json
from flask import Flask, render_template, redirect, url_for, make_response, request, Response, stream_with_context
import requests
from news import fetch_rss, stream_news_for_category, CATEGORIES, _cache, CACHE_DURATION, get_cached, set_cache, get_cache_minutes_left
import time

app = Flask(__name__)

@app.route("/")
def index():
    # get selected category from URL parameter, default to "Romania"
    selected = request.args.get("category", "Romania")

    # get cache age for selected category
    cached = _cache.get(selected)
    if cached:
        age = time.time() - cached["last_fetched"]
        minutes_left = max(0, round((CACHE_DURATION - age) / 60))
    else:
        minutes_left = 0
    response = make_response(render_template(
        "index.html",
        categories=list(CATEGORIES.keys()),
        selected=selected,
        minutes_left=minutes_left
    ))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/stream")
def stream():
    category = request.args.get("category", "Romania")
    force = request.args.get("force", "false") == "true"

    # serve from cache if available and not forced
    cached = _cache.get(category)
    if not force and cached and (time.time() - cached["last_fetched"]) < CACHE_DURATION:
        def from_cache():
            for key, articles in cached["data"].items():
                data = json.dumps({"key": key, "articles": articles})
                yield f"data: {data}\n\n"
            yield "data: {\"done\": true}\n\n"
        return Response(stream_with_context(from_cache()), mimetype="text/event-stream")

    # fetch fresh and stream results
    def generate():
        fetched = {}
        for key, articles in stream_news_for_category(category):
            fetched[key] = articles
            data = json.dumps({"key": key, "articles": articles})
            yield f"data: {data}\n\n"

        # save to cache
        _cache[category] = {
            "data": fetched,
            "last_fetched": time.time()
        }
        yield "data: {\"done\": true}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route("/refresh")
def refresh():
    category = request.args.get("category", "Finance")
    return redirect(url_for("index", category=category) + "&force=true")

@app.route("/test-rss")
def test_rss():
    import feedparser
    import urllib.request

    feeds = {
        "venture beat":              "https://venturebeat.com/feed/",    
    }

    def test_feed(name, url):
        try:
            # fetch with 5 second timeout
            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            feed = feedparser.parse(response.text)
            count = len(feed.entries)
            if count > 0:
                title = feed.entries[0].get("title", "N/A")[:60]
                return f"✅ {name}: {count} articole — {title}"
            else:
                return f"❌ {name}: 0 articole"
        except requests.exceptions.Timeout:
            return f"⏱️ {name}: timeout"
        except Exception as e:
            return f"❌ {name}: eroare — {str(e)[:50]}"

    results = []
    for name, url in feeds.items():
        result = test_feed(name, url)
        print(result)
        results.append(result)

    return "<br>".join(results)

@app.route("/ping")
def ping():
    return "pong" 

if __name__ == "__main__":
    app.run(debug=True, threaded=True)