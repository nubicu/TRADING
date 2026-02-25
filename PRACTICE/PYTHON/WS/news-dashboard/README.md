# ⚡ World News Dashboard

A personal news dashboard built with Python and Flask.
Aggregates top headlines across Business, Technology, Trading, and Romania
from sources around the world.

## Features
- Live headlines fetched from NewsAPI
- Four curated categories including Romania-specific news
- One-click refresh with loading state
- Clean, minimal dark UI

## Setup

1. Clone the repo
   git clone https://github.com/yourusername/news-dashboard.git
   cd news-dashboard

2. Install dependencies
   pip install -r requirements.txt

3. Add your API key
   Create a .env file in the root folder:
   NEWS_API_KEY=your_newsapi_key_here
   Get a free key at https://newsapi.org

4. Run the app
   python app.py

5. Open your browser
   http://127.0.0.1:5000

## Built With
- Python 3
- Flask
- NewsAPI
- Requests
```

---

**Your final file structure**
```
news-dashboard/
├── app.py
├── news.py
├── requirements.txt
├── README.md
├── .env              ← never uploaded to GitHub
├── .gitignore
└── templates/
    └── index.html