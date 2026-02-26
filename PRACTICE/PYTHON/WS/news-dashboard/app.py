from flask import Flask, render_template, redirect, url_for, make_response
import time
from news import _cache, CACHE_DURATION, get_all_news

app = Flask(__name__)

@app.route("/")
def index():
    # check cache age BEFORE fetching (fetching resets the timestamp)
    age = time.time() - _cache["last_fetched"]
    minutes_left = max(0, round((CACHE_DURATION - age) / 60))

    news = get_all_news()               # this may reset last_fetched

    response = make_response(render_template(
        "index.html",
        news=news,
        minutes_left=minutes_left
    ))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/refresh")
def refresh():
    get_all_news(force=True)            # force a fresh API call
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)