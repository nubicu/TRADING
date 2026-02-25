from flask import Flask, render_template, redirect, url_for
from news import get_all_news

app = Flask(__name__)

@app.route("/")
def index():
    news = get_all_news()
    return render_template("index.html", news=news)

@app.route("/refresh")
def refresh():
    return redirect(url_for("index"))   # just sends user back to "/" which re-fetches everything

if __name__ == "__main__":
    app.run(debug=True)